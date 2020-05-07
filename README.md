# Flask Role Based Access Control
Basic structure for starting a Flask project with basic role based security.

---

Create the database table
---
```
CREATE TABLE users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(30),
    password_hash VARCHAR(128),
    access INT(11), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
```

Create the first admin user
---

1. Create the database table.

2. Start the application and register a new user from the webpage

3. In the database users table, change access to ``` 2 ``` for admin

4. Log in to the application as this new user


Use this template to start a new application
---
1. Clone this repository to local computer

2. Rename the directory to reflect the new project name

3. Delete .git folder

4. Create a new virtual environment. ```python -m venv ./venv```

5. Activate the new virtual environment
   - Windows:  ```.\venv\Scripts\activate```
   - Mac:  ```source ./venv/bin/activate```

6. Install the dependencies ```pip install -r requirements.txt```

7. Make a new repository by running ```git init``` in the folder.

8. Track all the files in the new local repository ```git add .```

9. Make the first commit of this new project ```git commit -m 'first commit of <project name>``` from flask_template

10. On Github, create a new repository. DO NOT initialize it

11. Connect the local repository to the new Github repository ```git remote add origin <<repository_URL>>```

12. Create and change to a new local development branch ```git checkout b development```

13. Continue working with the project as you normally would.


-- use msci3300;

CREATE TABLE ksouravong_users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(30),
    password_hash VARCHAR(128),
    access INT(11), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE ksouravong_vendors (
    vendor_id INT(11) AUTO_INCREMENT PRIMARY KEY,
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

INSERT INTO ksouravong_vendors (order_date, booth_num, company, rep, phone_num, installed_date, asset_num, service, amount, paid)
VALUES ('2020-05-06', 'IA34J', 'Iowa Hawk Shop', 'Ruby Bollinger', '319-111-2222', '2020-06-30', '2341', 'DSL', '350.00', 'Yes');
