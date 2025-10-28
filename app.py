from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime
import db
import connect

app = Flask(__name__)
app.secret_key = 'svs_secret_2025'  # Set a secret key for session/flash

# Initialize database connection
db.init_db(
    app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname, connect.dbport
)

# Home

@app.route("/")
def home():
    return render_template("home.html")

# Services

@app.route("/services", methods=["GET"])
def service_list():
    cursor = db.get_cursor()
    cursor.execute("SELECT service_name, price FROM services;")
    services = cursor.fetchall()
    cursor.close()
    # Example flash (you can remove if not needed)
    flash("Example of a flash message. Optional, but good for error or confirmation messages.", "info")
    return render_template("service_list.html", services=services)




# Customers 
@app.route("/customers", methods=["GET"])
def customer_list():
    cursor = db.get_cursor()
    q = request.args.get("q", "").strip()

    if q:
        like = f"%{q}%"
        cursor.execute("""
            SELECT customer_id, first_name, family_name, email, phone, date_joined
            FROM customers
            WHERE family_name LIKE %s
               OR first_name  LIKE %s
               OR IFNULL(email,'') LIKE %s
               OR phone LIKE %s
            ORDER BY family_name, first_name
        """, (like, like, like, like))
    else:
        cursor.execute("""
            SELECT customer_id, first_name, family_name, email, phone, date_joined
            FROM customers
            ORDER BY family_name, first_name
        """)
    customers = cursor.fetchall()
    cursor.close()
    return render_template("customer_list.html", customers=customers, q=q)




#Customer appointment 
@app.route("/customers/<int:customer_id>", methods=["GET"])
def customer_appointment(customer_id):
    cursor = db.get_cursor()

    # Header details for the page
    cursor.execute("""
        SELECT customer_id, first_name, family_name, email, phone, date_joined
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        cursor.close()
        flash(f"Customer #{customer_id} not found.", "danger")
        return redirect(url_for("customer_list"))

    # Appointments for this customer ONLY (oldest first), with costs and future highlight
    cursor.execute("""
        SELECT 
            a.appt_id,
            a.appt_datetime,
            GROUP_CONCAT(
                CONCAT(s.service_name, ' ($', FORMAT(s.price, 2), ')')
                ORDER BY s.service_name SEPARATOR ', '
            ) AS services_with_costs,
            IFNULL(SUM(s.price), 0) AS total_cost,
            CASE WHEN a.appt_datetime >= NOW() THEN 1 ELSE 0 END AS is_future
        FROM appointments a
        LEFT JOIN appointment_services asj ON asj.appt_id = a.appt_id
        LEFT JOIN services s ON s.service_id = asj.service_id
        WHERE a.customer_id = %s
        GROUP BY a.appt_id, a.appt_datetime
        ORDER BY a.appt_datetime ASC
    """, (customer_id,))
    appts = cursor.fetchall()

    cursor.close()
    return render_template("customer_appointment.html", customer=customer, appts=appts)




#Appointments
@app.route("/appointments", methods=["GET"])
def appointment_list():
    cursor = db.get_cursor()
    cursor.execute("""
        SELECT 
            a.appt_id,
            a.appt_datetime,
            c.customer_id,
            c.first_name,
            c.family_name,
            GROUP_CONCAT(
                CONCAT(s.service_name, ' ($', FORMAT(s.price, 2), ')')
                ORDER BY s.service_name SEPARATOR ', '
            ) AS services_with_costs,
            IFNULL(SUM(s.price), 0) AS total_cost,
            CASE WHEN a.appt_datetime >= NOW() THEN 1 ELSE 0 END AS is_future
        FROM appointments a
        JOIN customers c ON c.customer_id = a.customer_id
        LEFT JOIN appointment_services asj ON asj.appt_id = a.appt_id
        LEFT JOIN services s ON s.service_id = asj.service_id
        GROUP BY 
            a.appt_id, a.appt_datetime,
            c.customer_id, c.first_name, c.family_name
        ORDER BY a.appt_datetime ASC
    """)
    appts = cursor.fetchall()
    cursor.close()
    return render_template("appointment_list.html", appts=appts)




# Add Customer 
from flask import render_template, request, redirect, url_for, flash
from datetime import date, datetime
import db
@app.route("/customers/new", methods=["GET", "POST"])
def new_customer():
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")

    if request.method == "POST":
        first_name = (request.form.get("first_name") or "").strip()
        family_name = (request.form.get("family_name") or "").strip()
        email_raw   = (request.form.get("email") or "").strip()
        phone       = (request.form.get("phone") or "").strip()
        dj_str      = (request.form.get("date_joined") or "").strip()

        # Email optional (switch to "" if your DB column is NOT NULL)
        email = email_raw if email_raw else None

        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not family_name:
            errors.append("Family name is required.")

        # Date joined: default to today; if provided, must be <= today
        if dj_str:
            try:
                dj = datetime.strptime(dj_str, "%Y-%m-%d").date()
                if dj > today:
                    errors.append("Date joined cannot be in the future.")
            except ValueError:
                errors.append("Please provide a valid Date Joined (YYYY-MM-DD).")
        else:
            dj = today

        if email and "@" not in email:
            errors.append("Please provide a valid email address or leave it blank.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("new_customer.html", today_str=today_str, form_data={
                "first_name": first_name,
                "family_name": family_name,
                "email": email_raw,
                "phone": phone,
                "date_joined": dj_str or today_str,
            })

        # Insert: customer_id is auto by DB
        cursor = db.get_cursor()
        try:
            cursor.execute("""
                INSERT INTO customers (first_name, family_name, email, phone, date_joined)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, family_name, email, phone, dj))
            cursor.connection.commit()
            flash("Customer added successfully.", "success")
            return redirect(url_for("customer_list"))
        except Exception as e:
            flash(f"Could not add customer: {e}", "danger")
            return render_template("new_customer.html", today_str=today_str, form_data={
                "first_name": first_name,
                "family_name": family_name,
                "email": email_raw,
                "phone": phone,
                "date_joined": dj_str or today_str,
            })
        finally:
            cursor.close()

    # GET
    return render_template("new_customer.html", today_str=today_str, form_data=None)




# Add Appointment 
@app.route("/appointments/new", methods=["GET", "POST"])
def new_appointment():
    cursor = db.get_cursor()

    # Load choices used by the form (both GET and POST re-render)
    cursor.execute("""
        SELECT customer_id, family_name, first_name
        FROM customers
        ORDER BY family_name, first_name
    """)
    customers = cursor.fetchall()

    cursor.execute("""
        SELECT service_id, service_name, price
        FROM services
        ORDER BY service_name
    """)
    services = cursor.fetchall()

    if request.method == "POST":
        #Read form inputs
        customer_id = request.form.get("customer_id")
        dt_str      = (request.form.get("appt_datetime") or "").strip()  # "YYYY-MM-DDTHH:MM"
        notes       = (request.form.get("notes") or "").strip() or None
        service_ids = request.form.getlist("service_ids")  # list of strings

        #Validate
        errors = []

        if not customer_id:
            errors.append("Please select a customer.")

        try:
            appt_dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
            now = datetime.now()
            if appt_dt <= now:
                errors.append("Appointment must be in the future.")
            if appt_dt.weekday() == 6:  # Sunday
                errors.append("Appointments cannot be on a Sunday.")
        except ValueError:
            errors.append("Please provide a valid appointment date and time.")

        if not service_ids:
            errors.append("Please select at least one service.")

        if errors:
            for e in errors:
                flash(e, "danger")
            cursor.close()
            return render_template(
                "new_appointment.html",
                customers=customers,
                services=services,
                form_data={
                    "customer_id": customer_id,
                    "appt_datetime": dt_str,
                    "notes": notes,
                    "service_ids": service_ids,
                },
            )

        # Insert appointment
        cursor.execute("""
            INSERT INTO appointments (customer_id, appt_datetime, notes)
            VALUES (%s, %s, %s)
        """, (customer_id, appt_dt, notes))
        appt_id = cursor.lastrowid

        # Insert selected services
        for sid in service_ids:
            cursor.execute("""
                INSERT INTO appointment_services (appt_id, service_id)
                VALUES (%s, %s)
            """, (appt_id, sid))

        # Commit
        try:
            cursor.connection.commit()
        except Exception:
            pass

        cursor.close()
        flash("Appointment created successfully.", "success")
        return redirect(url_for("appointment_list"))

    # GET
    cursor.close()
    return render_template("new_appointment.html", customers=customers, services=services)




#Edit Customer
@app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    """Edit: first_name, family_name, email (optional), phone
       Not editable: customer_id, date_joined
    """
    # Fetch current record
    cursor = db.get_cursor()
    cursor.execute("""
        SELECT customer_id, first_name, family_name, email, phone, date_joined
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))
    customer = cursor.fetchone()

    if not customer:
        cursor.close()
        flash(f"Customer #{customer_id} not found.", "danger")
        return redirect(url_for("customer_list"))

    if request.method == "POST":
        first_name = (request.form.get("first_name") or "").strip()
        family_name = (request.form.get("family_name") or "").strip()
        email_raw = (request.form.get("email") or "").strip()
        phone = (request.form.get("phone") or "").strip()

        email = email_raw if email_raw else None

        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not family_name:
            errors.append("Family name is required.")
        if email and "@" not in email:
            errors.append("Please provide a valid email address or leave it blank.")

        if errors:
            for e in errors:
                flash(e, "danger")
            cursor.close()
            return render_template(
                "edit_customer.html",
                customer_id=customer["customer_id"],
                date_joined=customer["date_joined"],
                form_data={
                    "first_name": first_name,
                    "family_name": family_name,
                    "email": email_raw,
                    "phone": phone,
                }
            )

        # Update allowed fields only
        cursor = db.get_cursor()
        cursor.execute("""
            UPDATE customers
            SET first_name = %s,
                family_name = %s,
                email = %s,
                phone = %s
            WHERE customer_id = %s
        """, (first_name, family_name, email, phone, customer_id))

        try:
            cursor.connection.commit()
        except Exception:
            pass
        cursor.close()
        flash("Customer details updated.", "success")
        return redirect(url_for("customer_appointment", customer_id=customer_id))

    # GET: prefill
    cursor.close()
    return render_template(
        "edit_customer.html",
        customer_id=customer["customer_id"],
        date_joined=customer["date_joined"],
        form_data={
            "first_name": customer["first_name"],
            "family_name": customer["family_name"],
            "email": customer["email"] or "",
            "phone": customer["phone"] or "",
        }
    )


#Service summary report 
@app.route("/reports/services", methods=["GET"])
def service_summary_report():
    cursor = db.get_cursor()
    # Include services with zero usage (LEFT JOIN)
    cursor.execute("""
        SELECT
            s.service_id,
            s.service_name,
            s.price,
            COUNT(asj.appt_id) AS times_used,
            IFNULL(SUM(CASE WHEN asj.appt_id IS NOT NULL THEN s.price ELSE 0 END), 0) AS total_earnings
        FROM services s
        LEFT JOIN appointment_services asj
               ON asj.service_id = s.service_id
        GROUP BY s.service_id, s.service_name, s.price
        ORDER BY s.service_name
    """)
    rows = cursor.fetchall()
    cursor.close()

    # Grand totals for footer
    total_count = sum(r["times_used"] for r in rows)
    grand_total = sum(float(r["total_earnings"]) for r in rows)

    return render_template(
        "service_summary.html",
        rows=rows,
        total_count=total_count,
        grand_total=grand_total
    )
