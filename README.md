# Item Catalog

## About

Item catalog project from Udacity Full Stack Nanodegree Lesson 4 Servers, Authorization and CRUD. 
The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.
The project works as follow:
1. In this sample project, the homepage displays all current categories along with the latest added items.
2. Selecting a specific category shows you all the items available for that category.
3. Selecting a specific item shows you specific information of that item.
4. Clicking on Log in button will take the user to a login page where will be able to login throught Google Login
5. Clicking on Log out will sing out the user from google
6. After logging in, a user has the ability to add, update, or delete item info.

## In order to run the project

### You will need:
- Virtual Machine:
    - VirtualBox
    - Vagrant
- Python

### Setup

1. Install Vagrant And VirtualBox:
Virtual box can be download from here (https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system.
Then, Vagrant will be use to launch the VirtualBox, you can get Vagrant from here (https://www.vagrantup.com/)
Vagrant will do that.
2. Install Python3 (https://www.python.org/downloads/). Follow documentation.
3. Clone this repo

### Run the project

To start the Virtual Machine:
1. Open Terminal and navigate to the project folders we setup above.
2. cd into the vagrant directory inside the database folder
3. Run `vagrant up`
4. Run `vagrant ssh` to log into it
5. cd into the vagrant foler where item-catalogue is
6. Run `python database_setup.py` in order to set up the database
7. Run `python loatsofcategories.py` in order to add dummy data to the database
8. Run `python projects.py` to run the project
9. Open your browser and go to `http://localhost:1239`