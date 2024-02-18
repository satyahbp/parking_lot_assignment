# parking_lot_assignment
This program is a solution for the parking lot problem. <br>
This documentation explains how to use this program

## Requirements
- Python (Preferably 3.11)
- MongoDB (> version 5.0)

## Deploying the program
1. Install the python environment. You can get the desired python environment [here](https://www.python.org/downloads/release/python-3117/). You can get the guide to install python here: [For Windows](https://www.tutorialspoint.com/how-to-install-python-in-windows) and [for Linux](https://docs.python-guide.org/starting/install3/linux/).
2. Install MongoDB. You can get a guide to install MongoDB [here](https://www.mongodb.com/docs/manual/installation/).
3. Once Python and MongoDB are installed, clone this repository to your desired system.
4. Navigate to the directory where the code has been copied and go into the cloned repository.
5. In the repository, go to the file: ```conf/application.conf```
6. In the ```application.conf``` file, replace ```$MONGO_HOST``` with the IP of your mongo server, and ```$MONGO_PORT``` with the port of your mongo server.
7. Go back to the root of the repository, and there install the python dependencies with the command:<br> ```python -m pip install -r requirements.txt``` <br>(if "python" command doesn't work, try the same with "python3")
8. Once all the above steps are completed, run the code by the command:<br>```python app.py```
<br>("python3" if "python" doesn't work)
9. Once you are into the program, enter the command: ```help``` to get the list of all the commands that can be entered in the program.

<b>You are good to go now!</b>