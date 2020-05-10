# Iowa State Fair Vendors Orders Database
-----------------------------------------
```
The purpose of this database is to easily view and search through our organized database for existing order information. The Communications Department has the capabilities to add, update, and remove orders, while other departments are only able to view and search the orders.
```

# Technologies Used
----------------------------------------
```
The technology used to develop the database was MySQL. It was used to create two databases for user management and order information. After creating the databases, I use Visual Studio Code to work on my website. Main packages that were installed to make this website functional were Flask (Login, SQLAlchemy, WTF), Jinja2, SQLAlchemy, and Werkzeug.  GitBash is constantly used to make comments about changes that have been done throughout the project.  Lastly, everything gets pushed to GitHub to get it ready to be deployed. Microsoft Azure is used to connect to my project repository to deploy the offical website.
```

# How to Run The Application
-----------------------------------------
```
When you first get on the website, you are able to see the vendor orders database. You are viewing this webpage as an unauthenticated user. As an unauthenticated user, you can view, search, and see the details of the orders. Clicking on details shows that specific order information only. If you were to click 'Update' or 'Delete', you are prompted to log in as admins are the only ones who can make changes. The other pages you can see are the 'About', 'Contact', and 'Register'. 

The 'About' section describes what the purpose of this database is about and what functionality difference the admin and user has.  The 'Contact' section takes you to a fictional contact page if an individual outside of the department viewing the database has a question.  The 'Register' section is for an individual to sign up, and from there the admin would have to go in and enable them as an admin user to extend their privileges.

When you log in, you are an admin and have the capabilities to add, update, or delete a row from the database.  As an admin, you have three additional pages that the unauthenticated user would not be able to see. 

There is an 'Edit Orders' page where you can add a new order or view the specific details of a vendor's order.  When you click on the 'Details' button, you see the what the unautheneticated user would see. However, the only difference is when you click on 'Update' or 'Delete', you are able to perform any updates to the information or remove it completely.

'User Management' is where you can see all the admins who have the privilege to make these kinds of changes.  You can add a new user in this page or you can click on 'Details' and make any changes to their account or remove them as an admin. 

'Account Setting' gives the current admin the option to update their information on the account like: name, email, and password.
```

# Create the databases
-----------------------------------------
```
CREATE TABLE ksouravong_users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(30),
    password_hash VARCHAR(128),
    access INT(11), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE ksouravong_vendors (
    id INT(11) PRIMARY KEY,
    order_date DATE NOT NULL,  
    booth_num VARCHAR(10) NOT NULL,
    company VARCHAR(100) NOT NULL,
    rep VARCHAR(100) NOT NULL,
    phone_num VARCHAR(15) NOT NULL,
    installed_date DATE,
    asset_num INT, 
    service VARCHAR(100) NOT NULL, 
    amount VARCHAR(10) NOT NULL, 
    paid VARCHAR(5),
    returned VARCHAR(5)
    );
```
