# BookStoreDjango
Server application written in python and using django framework.
It represents the back end side of my Bookstore web side being coupled with the BookStoreAngularApp repository
The aplication runs on windows , preferably windows10.
To use the application you need a MySQL database, and change the database information in the file proj521/settings.py in the object DATABASES
To start the server you need to make use of a cmd window opened in the Scripts folder and run activate.bat to open the virtual enviornment used by the python aplication.
After starting the virtual enviornment move in folder proj251 using cmd ans type: py manage.py runserver.
For this aplication you will also need python so it is the best to have installed and set as path variable  python3
The logic of the backend is implemented in the folder products ,in the file views.py.
In the same folder you have the database models in the file models2.py
In the file urls.py from the folder proj521 you will find all the paths a client app can use to receve or send data to the aplication.
The aplication is independent of the angular side but is best used coupled with this one.

Between many features it also makes use of my trial twolio account used to send sms on users phones when they sign in ,log in or buy a product
To use this feature you should make a personal account of twolio and set the phone numbers of your  users as verified numbers
The changes you need to make in the app are in the file views.py 
in account_side,auth_token and trial_number.
