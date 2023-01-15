# MeusLembretes
CS50X Final Project
#### Video Demo:  <https://youtu.be/yME9f6HhZA8>
#### Description:
- The main idea of this project is to have a web site where you can write your appointments
- It is necessary create an account to use the app 
- A SQL database is used to store the information like username, password, appointments and date
- The languages used: python, html, javascript, css and SQL 
### Libraries
The libraries used in this project are: 
- flask, to create the application e manage the routes
- flask_session, was used to remember which user is logged in
- pyodbc, to create a link between the python file and the SQL database and update it when requested
### Database 
A SQL database was used to store all the information. In this database there is two tables, the first is for store the username and password and de second is for store the appointments that the user wrote and the date of this appointment
### How it works
First you will have to log in, if you don't have an account there is one button to register. 
The register page has a form where you can create a username and a password, if the username already exists, a message will be prompt.
Once you create your account, you will be able to log in and the homepage is where you can write an appointment and set its the date. There is also a section where you can see all your appointments. 
