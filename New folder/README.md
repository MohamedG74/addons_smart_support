# What is it? 

This project can be seen as a starting template to send some endpoints that are managed with a backoffice.

It was built with **NodeJS**, **ExpressJS**, **Bootstrap 4**, **AdminLTE 3**, **Pug** and **MySQL**. 

## Features and ToDo List

* [x] Add, Edit and Delete data from DB with the use of the backoffice
* [x] Login and Logout
* [x] Endpoint to send data from the DB 
* [x] Responsive data tables
* [x] Pagination and search from data tables
* [x] Export options: CSV, PDF e Print
* [x] Dynamic menu
* [ ] Upload image example
* [ ] Manage login users in backoffice
* [ ] Store session for a period of time (Remember me)
* [ ] Forgot password form
* [ ] Register form

## How to use it? 

After cloning this repo, run the command: ```npm install```

Import the database that is inside the folder **db**

Copy ```.env.example``` to ```.env``` and add your settings, including database connection

To run the project, run: ```npm start```

The default port is ```:3000``` and you can use ```teste@teste.pt``` and ```teste``` as password to login.

The example endpoint can be accessed in ```http://localhost:3000/api/customers```

### Links

[AdminLte](https://adminlte.io/)
[Pug - How to use](https://flaviocopes.com/pug/#including-other-pug-files)
