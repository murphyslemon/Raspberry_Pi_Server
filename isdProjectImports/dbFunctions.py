from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
from isdProjectImports import esp
from isdProjectImports import voteHandling
from collections import defaultdict
import uuid

db = SQLAlchemy()

class RegisteredESPs(db.Model):
    __tablename__ = 'registeredesps'
    DeviceIndex = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    DeviceID = db.Column(db.String(255), unique=True, nullable=False)
    RegistrationTime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    LastActiveTime = db.Column(db.TIMESTAMP)
    Assigned = db.Column(db.Boolean, default=False)
    Registered = db.Column(db.Boolean, default=False)
    MacAddress = db.Column(db.String(255), unique=True)

class Users(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.Text)
    DeviceIndex = db.Column(db.Integer)
    RegistrationDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Topics(db.Model):
    __tablename__ = 'topics'
    TopicID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.Text, nullable=False)
    Description = db.Column(db.Text)
    StartTime = db.Column(db.TIMESTAMP)
    EndTime = db.Column(db.TIMESTAMP)

class Votes(db.Model):
    __tablename__ = 'votes'
    VoteID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    VoteType = db.Column(db.Text, nullable=False)
    TopicID = db.Column(db.Integer, db.ForeignKey('topics.TopicID', ondelete='CASCADE'), nullable=False)
    VoteTime = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


def get_registered_esps(app):
    """Retrieve information about registered ESP devices from the database.

    Args:
        app: The Flask application object.

    Returns:
        JSON: A JSON response containing information about registered ESP devices.
            Each device is represented by a dictionary with keys including:
                - DeviceIndex: The index of the device.
                - DeviceID: The unique ID of the device.
                - RegistrationTime: Time of device registration.
                - LastActiveTime: Time of the device's last activity.
                - Assigned: Status of device assignment.
                - Registered: Status of device registration.
                - MacAddress: MAC address of the device.

    Raises:
        JSON: A JSON response with an error message and a status code 500 in case of an exception.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_registered_esps()\n')

    try:
        with app.app_context():
            registered_esps = (
                db.session.query(RegisteredESPs)
                .filter(RegisteredESPs.Registered == True)
                .all()
            )

            esp_data = defaultdict(lambda: {})

            for esp in registered_esps:
                esp_data[esp.DeviceIndex].update({
                    "DeviceIndex": esp.DeviceIndex,
                    "DeviceID": esp.DeviceID,
                    "RegistrationTime": str(esp.RegistrationTime),
                    "LastActiveTime": str(esp.LastActiveTime),
                    "Assigned": esp.Assigned,
                    "Registered": esp.Registered,
                    "MacAddress": esp.MacAddress,
                })

            esp_data_list = list(esp_data.values())

            return jsonify(esp_data_list)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


def get_all_esps(app):
    """Retrieve information about all ESP devices from the database.

    Args:
        app: The Flask application object.

    Returns:
        JSON: A JSON response containing information about all ESP devices.
            Each device is represented by a dictionary with keys including:
                - DeviceIndex: The index of the device.
                - DeviceID: The unique ID of the device.
                - RegistrationTime: Time of device registration.
                - LastActiveTime: Time of the device's last activity.
                - Assigned: Status of device assignment.
                - Registered: Status of device registration.
                - MacAddress: MAC address of the device.

    Raises:
        JSON: A JSON response with an error message and a status code 500 in case of an exception.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_all_esps()\n')

    try:
        with app.app_context():
            registered_esps = RegisteredESPs.query.all()
            esp_data_list = []

            for esp in registered_esps:
                esp_data = {
                    "DeviceIndex": esp.DeviceIndex,
                    "DeviceID": esp.DeviceID,
                    "RegistrationTime": str(esp.RegistrationTime),
                    "LastActiveTime": str(esp.LastActiveTime),
                    "Assigned": esp.Assigned,
                    "Registered": esp.Registered,
                    "MacAddress": esp.MacAddress
                }
                esp_data_list.append(esp_data)

            return jsonify(esp_data_list)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


def get_all_topics(app):
    """Retrieve information about all topics from the database.

    Args:
        app: The Flask application object.

    Returns:
        JSON: A JSON response containing information about all topics.
            Each topic is represented by a dictionary with keys including:
                - TopicID: The unique ID of the topic.
                - Title: The title of the topic.
                - Description: The description of the topic.
                - StartTime: The start time of the topic.
                - EndTime: The end time of the topic.

    Raises:
        JSON: A JSON response with an error message and a status code 500 in case of an exception.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_all_topics()\n')

    try:
        with app.app_context():
            topics = Topics.query.all()
            topic_data_list = []

            for topic in topics:
                topic_data = {
                    "TopicID": topic.TopicID,
                    "Title": topic.Title,
                    "Description": topic.Description,
                    "StartTime": str(topic.StartTime),
                    "EndTime": str(topic.EndTime)
                }
                topic_data_list.append(topic_data)

            return jsonify(topic_data_list)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


def get_topic(app, topicID):
    """Retrieve information about a specific topic from the database.

    Args:
        app: The Flask application object.
        topicID (int): The unique ID of the topic to retrieve.

    Returns:
        JSON: A JSON response containing information about the requested topic.
            The returned dictionary includes keys such as:
                - TopicID: The unique ID of the topic.
                - Title: The title of the topic.
                - Description: The description of the topic.
                - StartTime: The start time of the topic.
                - EndTime: The end time of the topic.

    Raises:
        JSON: A JSON response with an error message and a status code 500 in case of an exception.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_topic()\n')

    try:
        with app.app_context():
            topic = Topics.query.filter_by(TopicID=topicID).first()

            topic_data = {
                "TopicID": topic.TopicID,
                "Title": topic.Title,
                "Description": topic.Description,
                "StartTime": str(topic.StartTime),
                "EndTime": str(topic.EndTime)
            }

            return jsonify(topic_data)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


def get_votes(app, topicID):
    """Retrieve votes related to a specific topic from the database.

    Args:
        app: The Flask application object.
        topicID (int): The unique ID of the topic to retrieve votes for.

    Returns:
        JSON: A JSON response containing information about the votes related to the specified topic.
            The returned list includes dictionaries for each vote with keys such as:
                - VoteID: The unique ID of the vote.
                - UserID: The ID of the user who cast the vote.
                - VoteType: The type of the vote.
                - TopicID: The ID of the topic the vote is related to.
                - VoteTime: The timestamp of when the vote was cast.

    Raises:
        JSON: A JSON response with an error message and a status code 500 in case of an exception.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_votes()\n')

    try:
        with app.app_context():
            votes = Votes.query.filter_by(TopicID=topicID).all()
            vote_data_list = []

            for vote in votes:
                vote_data = {
                    "VoteID": vote.VoteID,
                    "UserID": vote.UserID,
                    "VoteType": vote.VoteType,
                    "TopicID": vote.TopicID,
                    "VoteTime": str(vote.VoteTime)
                }
                vote_data_list.append(vote_data)

            return jsonify(vote_data_list)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500
    

def get_votes_by_user(app, userID):
    """Retrieve votes cast by a specific user from the database.

    Args:
        app: The Flask application object.
        userID (int): The unique ID of the user to retrieve votes for.

    Returns:
        JSON: A JSON response containing information about the votes cast by the specified user.
            The returned list includes dictionaries for each vote with keys such as:
                - VoteID: The unique ID of the vote.
                - UserID: The ID of the user who cast the vote.
                - VoteType: The type of the vote.
                - TopicID: The ID of the topic the vote is related to.
                - VoteTime: The timestamp of when the vote was cast.

    Raises:
        JSON: A JSON response with an error message and a status code 500 in case of an exception.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_votes_by_user()\n')

    try:
        with app.app_context():
            votes = Votes.query.filter_by(UserID=userID).all()
            vote_data_list = []

            for vote in votes:
                vote_data = {
                    "VoteID": vote.VoteID,
                    "UserID": vote.UserID,
                    "VoteType": vote.VoteType,
                    "TopicID": vote.TopicID,
                    "VoteTime": str(vote.VoteTime)
                }
                vote_data_list.append(vote_data)

            return jsonify(vote_data_list)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


# DEBUG ONLY
def clear_database(app):
    try:
        with app.app_context():
            db.session.query(Votes).delete()
            db.session.query(Topics).delete()
            db.session.query(Users).delete()
            db.session.query(RegisteredESPs).delete()
            db.session.commit()
            return jsonify("Database cleared.")

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


# DEBUG ONLY
def init_db(app):
    try:
        with app.app_context():
            db.create_all()
            db.session.commit()
            return jsonify("Database initialized.")

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


# DEBUG ONLY
def insert_data(app):
    try:
        with app.app_context():
            registered_esps_data = [
                {'DeviceID': 'ESP001', 'Registered': True, 'MacAddress': '00:11:22:33:44:55'},
                {'DeviceID': 'ESP002', 'Registered': True, 'MacAddress': 'AA:BB:CC:DD:EE:FF'}
            ]
            for data in registered_esps_data:
                registered_esp = RegisteredESPs(**data)
                db.session.add(registered_esp)

            users_data = [
                {'DeviceIndex': 1, 'Username': 'User1'},
                {'DeviceIndex': 2, 'Username': 'User2'},
                {'DeviceIndex': 1, 'Username': 'User3'}
            ]
            for data in users_data:
                user = Users(**data)
                db.session.add(user)

            topics_data = [
                {'Title': 'Topic 1', 'Description': 'Description for Topic 1', 'StartTime': '2023-01-01', 'EndTime': '2023-01-10'},
                {'Title': 'Topic 2', 'Description': 'Description for Topic 2', 'StartTime': '2023-02-01', 'EndTime': '2023-02-15'}
            ]
            for data in topics_data:
                topic = Topics(**data)
                db.session.add(topic)

            votes_data = [
                {'UserID': 1, 'VoteType': 'yes', 'TopicID': 1},
                {'UserID': 2, 'VoteType': 'no', 'TopicID': 1},
                {'UserID': 3, 'VoteType': 'yes', 'TopicID': 2}
            ]
            for data in votes_data:
                vote = Votes(**data)
                db.session.add(vote)

            db.session.commit()
            return jsonify("Data inserted successfully.")

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


def register_esp(app, mac_address):
    """Register an ESP by updating its DeviceID and Registered status in the database.

    Args:
        app: The Flask application object.
        mac_address (str): The MAC address of the ESP to be registered.

    Returns:
        tuple or str: A tuple containing the instance of RegisteredESPs and a boolean value indicating the operation's success.
            - If the operation succeeds, returns the RegisteredESPs instance and True.
            - If the given MAC address is not found, it attempts to add the ESP and returns the result of add_esp function.
            - In case of an exception, returns the error message as a string and False.

    Note:
        - The returned tuple contains either the RegisteredESPs instance and True or an error message and False.
        - The function updates the DeviceID and Registered status for the ESP and commits changes to the database.

    Raises:
        Exception: If an error occurs during the registration process.

    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.register_esp()\n')

    try:
        with app.app_context():
            registered_esp = RegisteredESPs.query.filter_by(MacAddress=mac_address).first()

            if registered_esp:
                device_id = str(uuid.uuid4())
                registered_esp.DeviceID = device_id
                registered_esp.Registered = True
                db.session.commit()

                # Return the instance of RegisteredESPs
                registered_esp = RegisteredESPs.query.filter_by(MacAddress=mac_address).first()
                return registered_esp, True

            else:
                with open('log.txt', 'a') as logFile:
                    logFile.write(f'{datetime.now()}: dbFunctions.register_esp(), ESP not found with the given MacAddress\n')
                return add_esp(app, mac_address)

    except Exception as errorMsg:
        return str(errorMsg), False


def add_esp(app, mac_address):
    """Add a new ESP to the database.

    Args:
        app: The Flask application object.
        mac_address (str): The MAC address of the ESP to be added.

    Returns:
        tuple or str: A tuple containing the instance of RegisteredESPs and a boolean value indicating the operation's success.
            - If the operation succeeds, returns the RegisteredESPs instance and True.
            - In case of an exception, returns the error message as a string and False.

    Note:
        - The returned tuple contains either the RegisteredESPs instance and True or an error message and False.
        - The function adds a new ESP to the database with the provided MAC address, setting Registered as True
          and generating a new DeviceID using uuid4().
        - The function commits changes to the database.

    Raises:
        Exception: If an error occurs during the ESP addition process.

    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.add_esp()\n')

    try:
        with app.app_context():
            add_esp = RegisteredESPs(MacAddress=mac_address, Registered=True, DeviceID=str(uuid.uuid4()))
            db.session.add(add_esp)
            db.session.commit()

            # Return the instance of RegisteredESPs
            registered_esp = RegisteredESPs.query.filter_by(MacAddress=mac_address).first()
            return registered_esp, True

    except Exception as errorMsg:
        return str(errorMsg), False


def unregister_esp(app, device_index):
    """Unregister an ESP from the database.

    Args:
        app: The Flask application object.
        device_index (int): The DeviceIndex of the ESP to be unregistered.

    Returns:
        tuple or str: A tuple containing the instance of RegisteredESPs and a boolean value indicating the operation's success.
            - If the operation succeeds, returns the RegisteredESPs instance and True.
            - If the ESP with the given DeviceIndex is not found, returns an error message and False.
            - In case of an exception, returns the error message as a string and False.

    Note:
        - The returned tuple contains either the RegisteredESPs instance and True, an error message, or False.
        - The function finds the ESP in the database using the provided DeviceIndex and sets its Registered status as False.
        - The function commits changes to the database.

    Raises:
        Exception: If an error occurs during the ESP unregistering process.

    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.unregister_esp()\n')

    try:
        with app.app_context():
            esp = RegisteredESPs.query.get(device_index)

            if esp:
                esp.Registered = False
                db.session.commit()
                return esp, True #TODO: return something else than esp
            else:
                return "ESP not found with the given DeviceIndex", False

    except Exception as errorMsg:
        return str(errorMsg), False


def unregister_all_esps(app):
    """Unregister all ESPs from the database.

    Args:
        app: The Flask application object.

    Returns:
        tuple or str: A tuple containing a success message and a boolean value indicating the operation's success.
            - If the operation succeeds, returns "All ESPs unregistered." and True.
            - In case of an exception, returns the error message as a string and False.

    Note:
        - This function sets the Registered status of all ESPs in the database as False.
        - It utilizes the RegisteredESPs model and commits changes to the database.
        - The returned tuple contains either a success message and True or an error message and False.

    Raises:
        Exception: If an error occurs during the ESPs unregistering process.

    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.unregister_all_esps()\n')

    try:
        with app.app_context():
            registered_esps = RegisteredESPs.query.all()

            for esp in registered_esps:
                esp.Registered = False

            db.session.commit()

            return "All ESPs unregistered.", True #TODO: return something else.

    except Exception as errorMsg:
        return str(errorMsg), False
    

def create_topic(app, obj: voteHandling.VoteInformation):
    """Create a new topic in the database based on the provided VoteInformation object.

    Args:
        app: The Flask application object.
        obj (voteHandling.VoteInformation): An object containing information about the topic:
            - title (str): Title of the topic.
            - description (str): Description of the topic.
            - voteStartTime (datetime): Start time of the topic.
            - voteEndTime (datetime): End time of the topic.

    Returns:
        bool: True if the topic creation succeeds; False otherwise.

    Note:
        - This function creates a new entry in the Topics table with the provided information.
        - It utilizes the Topics model and commits changes to the database.
        - The topicID attribute of the provided obj is updated with the ID of the created topic.
        - Returns True upon successful creation; False otherwise.

    Raises:
        Exception: If an error occurs during the topic creation process.

    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.create_topic()\n')

    try:
        with app.app_context():
            topic = Topics(Title=obj.title, Description=obj.description, StartTime=obj.voteStartTime, EndTime=obj.voteEndTime)
            db.session.add(topic)
            db.session.commit()

            obj.topicID = topic.TopicID

            return  True

    except Exception as errorMsg:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: dbFunctions.create_topic(), {str(errorMsg)}\n')
        return False


def create_user(app, username):
    """Create a new user in the database.

    Args:
        app: The Flask application object.
        username (str): The username of the new user.

    Returns:
        tuple: A tuple containing the registered user object and a boolean indicating success.
            - If successful, the first element is the instance of the registered user (Users model).
            - If unsuccessful, the first element is an error message.
            - The second element is a boolean flag indicating success (True/False).

    Note:
        - This function creates a new entry in the Users table with the provided username.
        - It utilizes the Users model and commits changes to the database.
        - Returns a tuple containing the registered user object and a success flag.
            - If successful, returns the registered user object and True.
            - If an error occurs, returns an error message and False.

    Raises:
        Exception: If an error occurs during the user creation process.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.create_user()\n')

    try:
        with app.app_context():
            user = Users(Username=username)
            db.session.add(user)
            db.session.commit()

            # Fetch the latest entry for the user with the provided username
            registered_user = Users.query.filter_by(Username=username).order_by(Users.UserID.desc()).first()

            return registered_user, True

    except Exception as errorMsg:
        return str(errorMsg), False


def assign_user_to_esp(app, username, espID):
    """Assign a user to an ESP in the database.

    Args:
        app: The Flask application object.
        username (str): The username of the user to be assigned.
        espID (str): The ID of the ESP to which the user will be assigned.

    Returns:
        tuple: A tuple containing a JSON response message and an HTTP status code.
            - If successful, the first element is a JSON response indicating success and a status code 200.
            - If the user creation fails, the first element is a JSON response indicating failure and a status code 500 or an error message.

    Note:
        - This function tries to assign the user with the provided username to the specified ESP.
        - Returns a JSON response message with an HTTP status code indicating the outcome of the assignment process.

    Raises:
        Exception: If an error occurs during the assignment process.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.assign_user_to_esp()\n')

    # Assign user to ESP.
    try:
        with app.app_context():
            # Verify the ESP exists.
            print(espID)
            esp = RegisteredESPs.query.filter_by(DeviceIndex=espID).first()
            if esp is None:
                return jsonify({'message': 'ESP not found.'}), 404
            
            # Create user in DB.
            user, status = create_user(app, username)
            if not status:
                with open('log.txt', 'a') as logFile:
                    logFile.write(f'{datetime.now()}: dbFunctions.assign_user_to_esp(), failed to create user: "{user}"\n')
                return jsonify({'message': 'Failed to create user.'}), 500

            # Assign user to ESP.
            esp.Assigned = True
            user.DeviceIndex = esp.DeviceIndex
            db.session.commit()
            return jsonify({'message': 'User assigned to ESP successfully.'}), 200

    except Exception as errorMsg:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: dbFunctions.assign_user_to_esp(), {str(errorMsg)}\n')
        return str(errorMsg), 500

    

def update_vote(app, DeviceID, voteType):
    """Update the vote type for a user associated with a specific ESP.

    Args:
        app: The Flask application object.
        DeviceID (str): The ID of the ESP.
        voteType (str): The updated vote type.

    Returns:
        tuple: A tuple containing a message and a boolean indicating success.
            - If successful, returns a message string indicating successful vote update and True.
            - If the ESP is not assigned or an error occurs, returns an error message and False.

    Note:
        - This function updates the vote type for a user associated with the specified ESP.
        - Retrieves the ESP information based on the provided DeviceID.
        - If the ESP is assigned, it fetches the associated user and updates the vote type.
        - Returns a message indicating the success or failure of the vote update process.
    """

    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.update_vote()\n')

    try:
        with app.app_context():
            esp = RegisteredESPs.query.filter_by(DeviceID=DeviceID).first()
            
            if esp.Assigned:
                user = Users.query.filter_by(DeviceIndex=esp.DeviceIndex).first()
                vote = Votes.query.filter_by(UserID=user.UserID).first()
                vote.VoteType = voteType
                db.session.commit()
                return "Vote updated successfully.", True
            else:
                return "ESP not assigned.", False
    except Exception as errorMsg:
        return str(errorMsg), False

