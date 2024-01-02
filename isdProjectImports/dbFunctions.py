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
def get_registered_esps():
    try:
        registered_esps_with_users = (
            db.session.query(RegisteredESPs, Users)
            .join(Users, RegisteredESPs.DeviceIndex == Users.DeviceIndex)
            .filter(RegisteredESPs.Registered == True)
            .all()
        )

        esp_data = defaultdict(lambda: {"Users": []})

        for esp, user in registered_esps_with_users:
            esp_data[esp.DeviceIndex].update({
                "DeviceIndex": esp.DeviceIndex,
                "DeviceID": esp.DeviceID,
                "RegistrationTime": str(esp.RegistrationTime),
                "LastActiveTime": str(esp.LastActiveTime),
                "Assigned": esp.Assigned,
                "Registered": esp.Registered,
                "MacAddress": esp.MacAddress,
            })

            user_info = {
                "UserID": user.UserID,
                "Username": user.Username,
                "RegistrationDate": str(user.RegistrationDate),
                "DeviceIndex": user.DeviceIndex
            }

            esp_data[esp.DeviceIndex]["Users"].append(user_info)

        esp_data_list = list(esp_data.values())

        return jsonify(esp_data_list)

    except Exception as errorMsg:
        error_message = {"error": str(errorMsg)}
        return jsonify(error_message), 500


# GET all Esps from the database.
def get_all_esps():
    try:
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
def get_all_topics():
    try:
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
def get_topic(topicID):
    try:
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
def get_votes(topicID):
    try:
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
def get_votes_by_user(userID):
    try:
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
def clear_database():
    try:
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
def init_db():
    db.create_all()
    db.session.commit()
    return jsonify("Database initialized.")


# Inserts test data into the database.
# DEBUG ONLY
def insert_data():
    try:
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


# Modify the deviceid and registered status of an existing ESP with the given macAddress.
def register_esp(mac_address):
    try:
        registered_esp = RegisteredESPs.query.filter_by(MacAddress=mac_address).first()

        if registered_esp:
            device_id = str(uuid.uuid4())
            registered_esp.DeviceID = device_id
            registered_esp.Registered = True

            db.session.commit()

            return True, registered_esp

        else:
            return False, "ESP not found with the given macAddress"

    except Exception as errorMsg:
        return False, str(errorMsg)


# Create a new ESP with the given macAddress.
def add_esp(mac_address):
    try:
        add_esp = RegisteredESPs(MacAddress=mac_address)
        db.session.add(add_esp)
        db.session.commit()

        registered_esp = RegisteredESPs.query.filter_by(MacAddress=mac_address).first()

        return True, jsonify(registered_esp)

    except Exception as errorMsg:
        return False, str(errorMsg)


#Unregister specific ESP
def unregister_esp(device_index):
    try:
        esp = RegisteredESPs.query.get(device_index)

        if esp:
            esp.Registered = False
            db.session.commit()
            return True, esp #TODO: return something else than esp
        else:
            return False, "ESP not found with the given DeviceIndex"

    except Exception as errorMsg:
        return False, str(errorMsg)


# Unregister all ESPs.
def unregister_all_esps():
    try:
        registered_esps = RegisteredESPs.query.all()

        for esp in registered_esps:
            esp.Registered = False

        db.session.commit()

        return True, "All ESPs unregistered." #TODO: return something else.

    except Exception as errorMsg:
        return False, str(errorMsg)
    

# POST new topic (vote) to the database.   
def create_topic(obj: voteHandling.VoteInformation):
    try:
        topic = Topics(Title=obj.title, Description=obj.description, StartTime=obj.voteStartTime, EndTime=obj.voteEndTime)
        db.session.add(topic)
        db.session.commit()

        obj.topicID = topic.TopicID

        return True, "Topic created successfully."

    except Exception as errorMsg:
        return False, str(errorMsg)


# Register user to ESP.
# Create a new user in the database.
def create_user(username, deviceID):
    try:
        user = Users(Username=username, DeviceIndex=deviceID)
        db.session.add(user)
        db.session.commit()

        return True, "User created successfully."

    except Exception as errorMsg:
        return False, str(errorMsg)


# Assign user to ESP.
def assign_user_to_esp(userID, espID):
    try:
        user = Users.query.get(userID)
        esp = RegisteredESPs.query.get(espID)

        if user and esp:
            user.DeviceIndex = esp.DeviceIndex
            esp.Assigned = True
            db.session.commit()

            return True, "User assigned to ESP successfully."

        else:
            return False, "User or ESP not found."

    except Exception as errorMsg:
        return False, str(errorMsg)