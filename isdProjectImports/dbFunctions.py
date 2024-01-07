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
    Username = db.Column(db.Text, unique=True)
    DeviceIndex = db.Column(db.Integer, db.ForeignKey('registeredesps.DeviceIndex'))
    RegistrationDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    registered_esp = db.relationship('RegisteredESPs', backref='users')

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



# GET all registered ESPs from the database.
def get_registered_esps(app):
    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.get_registered_esps()\n')

    try:
        with app.app_context():
            registered_esps = (
                db.session.query(RegisteredESPs)
                .filter(RegisteredESPs.Registered == True, RegisteredESPs.Assigned == False)
                .all()
            )

            print(registered_esps)

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


# GET all Esps from the database.
def get_all_esps(app):
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


# GET all topics (votes) from the database.
def get_all_topics(app):
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


# GET topic (vote) based on topicID from the database.
def get_topic(app, topicID):
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


# GET all votes from the database based on topicID.
def get_votes(app, topicID):
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
    

# GET all votes from the database based on userID.
def get_votes_by_user(app, userID):
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


# Removes all data from the database.
# DEBUG ONLY
def clear_database(app):
    try:
        with app.app_context():
            db.session.query(RegisteredESPs).delete()
            db.session.query(Users).delete()
            db.session.query(Topics).delete()
            db.session.query(Votes).delete()
            db.session.commit()
            return jsonify("Database cleared.")

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


# Initializes the database.
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


# Inserts test data into the database.
# DEBUG ONLY
def insert_data(app):
    try:
        with app.app_context():
            registered_esps_data = [
                {'DeviceIndex': 1, 'DeviceID': 'ESP001', 'Assigned': True, 'Registered': True, 'MacAddress': '00:11:22:33:44:55'},
                {'DeviceIndex': 2, 'DeviceID': 'ESP002', 'Assigned': False, 'Registered': True, 'MacAddress': 'AA:BB:CC:DD:EE:FF'}
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
    

# Function to register an ESP by updating its DeviceID and Registered status
# Function to register an ESP by updating its DeviceID and Registered status
def register_esp(app, mac_address):
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


# Function to add a new ESP to the database
def add_esp(app, mac_address):
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


# Unregister specific ESP
def unregister_esp(app, device_index): 
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


# Unregister all ESPs.
def unregister_all_esps(app):
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
    

# POST new topic (vote) to the database.   
def create_topic(app, obj: voteHandling.VoteInformation):
    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.create_topic()\n')

    try:
        with app.app_context():
            topic = Topics(Title=obj.title, Description=obj.description, StartTime=obj.voteStartTime, EndTime=obj.voteEndTime)
            db.session.add(topic)
            db.session.commit()

            obj.topicID = topic.TopicID

            return "Topic created successfully.", True

    except Exception as errorMsg:
        return str(errorMsg), False


# Register user to ESP.
# Create a new user in the database.
def create_user(app, username, deviceID):
    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.create_user()\n')

    try:
        with app.app_context():
            user = Users(Username=username, DeviceIndex=deviceID)
            db.session.add(user)
            db.session.commit()

            return "User created successfully.", True

    except Exception as errorMsg:
        return str(errorMsg), False


# Assign user to ESP.
def assign_user_to_esp(app, userID, espID):
    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Running dbFunctions.assign_user_to_esp()\n')

    try:
        with app.app_context():
            user = Users.query.get(userID)
            esp = RegisteredESPs.query.get(espID)

            if user and esp:
                user.DeviceIndex = esp.DeviceIndex
                esp.Assigned = True
                db.session.commit()

                return "User assigned to ESP successfully.", True

            else:
                return "User or ESP not found.", False

    except Exception as errorMsg:
        return str(errorMsg), False
    

# Update ESP and user vote.
# Assumes vote time has been verified prior to calling this function.
def update_vote(app, DeviceID, voteType):
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

