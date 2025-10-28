# Selwyn Veterinary Services (SVS) 

Selwyn veterinary services (SVS) is a small veterinary clinic in 123 Lincoln Road, Lincoln 7608, New zealand.

This web application will enable employees to handle customers, services, and appointments.

Only Flask, MySQL, and Bootstrap 5 (JavaScript)are used to make the appointments.

## Steps to read this in VS code

1. **create virtual environment:**
*view*>*command palette* > *python create environment* > *venv*

## Steps 

**Create Virtual Environment:** 

*view > command palette > python create environment > venv > created virtual envrionment*

2.  **Install dependencies** 
pip install --upgrade pip
pip install requirements.txt.


3. **Configure database in mysql**
The query to be run in your MySQL console is the following:
sql
SOURCE `svs_create_local_db.sql` ;
USE svs;
SOURCE `svs_populate_data.sql`;
This establishes all the tables (customers, services, appointments, etc.).
Loads sample data and uses it to create a utility named appointment services.
- open file from workbench 
- Once query was run, press Refresh arrows on the top right of Schemas sidebar to appear in the list.


4. **Environment variables:**
The following should be run beforehand:
bash
-export DB_HOST=`127.0.0.1`
-export DB_PORT=`3306`
-export DB_USER=`root`
-export DB_PASSWORD=`yourpassword`
-export DB_NAME=`svs`

Otherwise, declare them in connect.py.

5. **Run the application**
To run with debugging:  **Run** > **Start Debugging** > **Python Debugger** > **Flask** (<u>NOT</u> *Python file*!) > **app.py**  

Then open:http://127.0.0.1:5000


## Web application features 

1. Home page with picture and description.
2. Header and footer (Bootstrap-based) of every page.
3. Customer List and Search (Clickable to see appointments).
4. Appointment List (the past and the future, color-coded)
5. Adding and editing of customers with validation.
6. Add Appointments (never on Sundays, only in future)
7. Service Summary Report (totals and earnings)


### UI designs used 

- Pure "Bootstrap 5".
- Flexible design (no custom CSS).
- User-friendly and business-like design.

Example Bootstrap import:
html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>


# Project Report Requirements ;

## Design Decisions 
1.  The reason why Flask Blueprints was not chosen was to keep things simple (single app).
    file.
2.  Roads divided logically:services,customers, appointments and report.So, the employer can easily get the right place in one click.
3.  "GET and POST methods" are used in form processing, GET is used to list.
     POST for insert/update.
4.  All other templates were based on the extension of Single base.html template. 
    navigable and footer that is consistent.
5.  The other fields (such as email) are optional and therefore can be used with a null value; date joined is set to a sensible default (or is validated) to prevent any future dates by default.
6.  MySQL dictionaries and cursors are used to access data through easy field access.
7.  Customer clickable link loads the appointment summary dynamically using query parameters.
8.  Check future validation of appointments by Date & time and color  using Python and bootstrap.
9. same layout for service list and customer list to make it similar.
10. Database connection stored in central database, that is, connect.py, in order to make it easy.
11. Professional layout was ensured by the use of Bootstrap containers and.
    cards.
12. GROUP BY, COUNT and SUM queries can be used in querying the service summary.
    efficiency.
13.The search by customers is an SQL query that orders by family name, first name to keep large lists of customers fast and consistent and we do not write a lot of client side code.
14. With the HTML5 validation, the user is assisted, whereas the rules are implemented by the Flask route: date should be in the future, not on Sunday, and at least one service should be chosen. Checks are done on the server to prevent bypasses.
15. Requirements.txt contains only Flask + MySQL client (and similar libs) and are thus easy to set up by markers or teammates.

## Image source

Pexels - ( https://www.pexels.com/photo/two-yellow-labrador-retriever-puppies-1108099/).
All the pictures are open access and can be used in the learning process.


## Database questions

1. **Table Creation (customers)**  
 sql
CREATE TABLE customers (
  customer id int auto increase primary key,
  first_name VARCHAR(50),
  family_name VARCHAR(50),
  email VARCHAR(100),
  phone VARCHAR(20),
  date_joined DATE
);


2. **Table Relationships**  

 sql
CREATE Table appointment services (
  appointment_id INT,
  service_id INT,
  PRIMARY KEY (appointment id, service id),
  FOREIGN KEY (appointment id) REFER to appointments(appointment id),
  Foreign key (service id) refers to services (service id).
);


3. **New Table - animals**  
 sql
CREATE TABLE animals (
  animal_id INT AUTO_INCREMENT PRIMARY KEY,
  owner_id INT,
  name VARCHAR(50),
  species VARCHAR(30),
  sex VARCHAR(10),
  date_of_birth DATE,
  FOREIGN KEY (owner_id) REFERENCES customers(customer_id)
);


 `Insert Example`
 sql
INSERT animals (owner id, name, species, sex, date of birth);
VALUES (1, 'Buddy', 'Dog', 'Male', '2021-05-10');


5. **Discussion** 

The simpler design to make, in most cases, is to associate the appointment with the animal in cases where a customer may possess more than one pet. It allows clinical history, procedures, and billing to automatically be tied to the appropriate animal at the same time that they can be accessed through owner_id. It also makes future features like keeping track of weight, microchip numbers, reminders per pet or species specific pricing very easy. It is easier to begin by linking to the customer but then the histories are ambiguous (which pet?) and reporting and reminders are difficult. 
The clean model gets the following: appointments.appt_id → animals.animal_id → customers.customer_id. On edge cases (walk-ins where animal information is not available but), you can permit an ad hoc temporary record of the animal marked as unknown, or permitting animal id to be a nullable field during intake, and mandatory before finalization.



#### The PythonAnywhere deployment is also available.

-   GitHub Cloning Repository (Not uploaded manually).
-   Web interface recreated the database.
-   Application under test through live URL:
    https://yourusername.pythonanywhere.com

