Selwyn Veterinary Services (SVS) is a veterinary clinic located in Vermont, USA.

Web Application Evaluation Flashcard (Flask + MySQL Project) COMP636.

Selwyn veterinary services (SVS) is a small veterinary clinic in.
Harbleton, Pewsey.\
This web application will enable employees to handle clients, services, and
Only Flask, MySQL, and Bootstrap 5 are used to make the appointments.
JavaScript).

------------------------------------------------------------------------

## 🚀 Quick Setup Guide

### ⿡ Create Virtual Environment

 bash
python -m venv .venv


Activate: - **Windows PowerShell> bash .venv\Scripts/Activate.ps1 -
*MacOS / Linux*bash source.venv/bin/activate

### ⿢ Install Dependencies

 bash
pip install --upgrade pip
pip install requirements.txt.


### ⿣ Configure Database (MySQL)

The query to be run in your MySQL console is the following:

 sql
SOURCE svs_create_local_db.sql;
USE svs;
SOURCE svs_populate_data.sql;


This establishes all the tables (`customers, services, appointments, etc.).
Loads sample data and uses it to create a utility named appointment services.

------------------------------------------------------------------------

## ⚙ Environment Variables

The following should be run beforehand:

 bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=yourpassword
export DB_NAME=svs


Otherwise, declare them in connect.py.

------------------------------------------------------------------------

## ▶ Run the Application

 bash
python app.py


or

 bash
flask run


Then open:\
👉 <http://127.0.0.1:5000>

------------------------------------------------------------------------

## 🧰 Features Implemented

-   home page with picture and description.
-  Header and footer (Bootstrap-based) of every page.
-   Customer List and Search (Clickable to see appointments).
-   Appointment List (the past and the future, color-coded)
-   Adding and editing of customers with validation.
-   Add Appointments (never on Sundays, only in future)
-   Service Summary Report (totals and earnings)

------------------------------------------------------------------------

## 🎨 UI Design Notes

-   Pure *Bootstrap 5* via CDN.\
-   Flexible design (no custom CSS).
-   User-friendly and business-like design.
-   Example Bootstrap import:

 html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>


------------------------------------------------------------------------

Project Report (COMP636 Requirement)

## 🧩 Design Decisions

1.  The reason why Flask Blueprints was not chosen was to keep things simple (single app).
    file).
2.  Roads divided logically:/services,/customers,/ appointments etc.
3.  "GET and POST methods" are used in form processing, GET is used to list.
    POST for insert/update.
4.  All other templates were based on the extension of Single base.html template.
    navigable and footer that is consistent.
5.  Bootstrap Forms were utilized to guarantee intrinsic validation designs.
6.  MySQL dictionaries and cursors are used to access data through easy field access.
    names.
7.  Customer clickable link loads the appointment summary dynamically.
    using query parameters.
8.  DB operations were wrapped in try-except to add error handling.
9.  Check future validation of appointments current Danny using
    Python.
10. Reuse of template: customer list layout (search) layout.
    results.
11. Database connection stored in central database, that is, connect.py, in order to make it easy.
    environment changes.\
12. Professional layout was ensured by the use of Bootstrap containers and.
    cards.\
13. GROUP BY, COUNT and SUM queries can be used in querying the service summary.
    efficiency.

------------------------------------------------------------------------

## 🖼 Image Sources

-   Unsplash - Veterinary Care (unsplash.com) (Photo).
    (Free use)\
- Pexels - Pet Clinic ( https://www.PeXels.com/search/veterinary).
    All the pictures are open access and can be used in the learning process.

------------------------------------------------------------------------

## 🗃 Database Questions

*⿡ Table Creation (customers)*

 sql
CREATE TABLE customers (
  customer id int auto increase primary key,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone VARCHAR(20),
  email VARCHAR(100),
  date_joined DATE
);


*⿢ Table Relationships*

 sql
CREATE Table appointment services (
  appointment_id INT,
  service_id INT,
  PRIMARY KEY (appointment id, service id),
  FOREIGN KEY (appointment id) REFER to appointments(appointment id),
  Foreign key (service id) refers to services (service id).
);


*⿣ New Table -- animals*

 sql
CREATE TABLE animals (
  animal id INT AUTO INCREMENT PRIMARY Key,
  owner_id INT,
  name VARCHAR(50),
  species VARCHAR(30),
  sex VARCHAR(10),
  date_of_birth DATE,
  Foreign key(owner id) refers to customers(customer id).
);


*⿤ Insert Example*

 sql
INSERT animals (owner id, name, species, sex, date of birth);
VALUES (1, 'Buddy', 'Dog', 'Male', '2021-05-10');


*5* Discussion Ideally, the appointments are to be connected to an animal, not.
only the owner, as there are pets to which the services are applicable. This improves
record accuracy and enables more than one animal to a customer. However, for
the simplicity of this project, appointments are also bound to the *customer*
to simplify the model and combine requirement.



The PythonAnywhere deployment is also available.

-   GitHub Cloning Repository (Not uploaded manually).
-   Web interface recreated the database.
-   Application under test through live URL:
    https://yourusername.pythonanywhere.com

