# How to Run API Server

I have completed this exercise using python3 and the Flask framework. This python project also has a requirements.txt file containing the project dependencies that will be used to create a virtual environment. This is necessary so that the app can be run with all the required dependencies. 

## First, the following 3 items need to be installed:

1. python3 --> https://www.python.org/downloads/
2. Flask --> Do so by running the pip3 install Flask command
3. virtualenv --> Do so by running the pip3 install virtualenv command

Once you have everything downloaded, make sure you are in the project directory in the command line.

## Create the virtual environment:
Run the following command:
  virtualenv env

Before you can start the local server, you will need to activate the virtual environment:
  - For mac, run this command --> source env/bin/activate
  - For windows, run this command --> env\Scripts\activate

Lastly, to load the dependencies from requirement.txt into your virtual environment, run the following:
  pip3 install -r requirements.txt

## Start the server
Once the virtual enviornment is ready, you can run the local server with the following command: 
  python3 app.py

This should start the local server on http://127.0.0.1:5000

Likewise, the unit tests can be run with this command:
  python3 test.py