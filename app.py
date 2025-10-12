from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
import db
import connect
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'svs_secret_2025'  # Set a secret key for session/flash

# Initialize database connection
db.init_db(
    app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname, connect.dbport
)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/services", methods=["GET"])
def service_list():
    cursor = db.get_cursor()
    # Lists all services        
    qstr = "SELECT service_name, price FROM services;" 
    cursor.execute(qstr)        
    services = cursor.fetchall()
    cursor.close()
    if True:  # Example condition for a flash message
        flash("Example of a flash message. Optional, but good for error or confirmation " \
            "messages when used with an IF statement.", "info")
    return render_template("service_list.html", services=services)


from flask import render_template, request
import db

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


@app.route("/customers/<int:customer_id>", methods=["GET"])
def customer_appointment(customer_id):
    cursor = db.get_cursor()

    # Customer details
    cursor.execute("""
        SELECT customer_id, first_name, family_name, email, phone, date_joined
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))
    customer = cursor.fetchone()

    # Their appointments + services
    cursor.execute("""
        SELECT a.appt_id,
               a.appt_datetime,
               a.notes,
               GROUP_CONCAT(s.service_name ORDER BY s.service_name SEPARATOR ', ') AS services
        FROM appointments a
        LEFT JOIN appointment_services asj ON asj.appt_id = a.appt_id
        LEFT JOIN services s ON s.service_id = asj.service_id
        WHERE a.customer_id = %s
        GROUP BY a.appt_id
        ORDER BY a.appt_datetime DESC
    """, (customer_id,))
    appts = cursor.fetchall()

    cursor.close()
    return render_template("customer_appointments.html", customer=customer, appts=appts)

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
            -- e.g., "Consult ($50.00), Vaccination ($35.00)"
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

