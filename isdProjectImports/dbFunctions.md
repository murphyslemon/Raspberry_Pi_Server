# Functions and JSON Responses
<br><br>
# Function: `get_registered_esps()`

### Description:
This function retrieves all registered ESPs along with associated user information from the database.

### Arguments:
None

### JSON Return:
The function returns a JSON array containing objects representing registered ESPs and their associated users. 

#### Example JSON Response:
```json
[
    {
        "DeviceIndex": "ESP_DeviceIndex_1",
        "DeviceID": "ESP_DeviceID_1",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": "YYYY-MM-DD HH:MM:SS",
        "Assigned": true,
        "Registered": true,
        "MacAddress": "ESP_MacAddress_1",
        "Users": [
            {
                "UserID": "User_ID_1",
                "Username": "Username_1",
                "RegistrationDate": "YYYY-MM-DD HH:MM:SS",
                "DeviceIndex": "User_DeviceIndex_1"
            },
        ]
    },
    // More ESP objects if available
]
```

In case of an exception, the function returns a JSON object with an error message and a status code of 500:
```json
{
    "error": "Error message here"
}
```
<br><br>
# Function: `get_all_esps()`

### Description:
This function retrieves all Electronic Service Providers (ESPs) from the database.

### Arguments:
None

### JSON Return:
The function returns a JSON array containing objects representing all ESPs available in the database.

#### Example JSON Response:
```json
[
    {
        "DeviceIndex": "ESP_DeviceIndex_1",
        "DeviceID": "ESP_DeviceID_1",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": "YYYY-MM-DD HH:MM:SS",
        "Assigned": true,
        "Registered": true,
        "MacAddress": "ESP_MacAddress_1"
    },
    // More ESP objects if available
]
```

In case of an exception, the function returns a JSON object with an error message and a status code of 500:
```json
{
    "error": "Error message here"
}
```
<br><br>
# Function: `get_all_topics()`

### Description:
This function retrieves all topics from the database.

### Arguments:
None

### JSON Return:
The function returns a JSON array containing objects representing all topics available in the database.

#### Example JSON Response:
```json
[
    {
        "TopicID": "Topic_ID_1",
        "Title": "Topic_Title_1",
        "Description": "Topic_Description_1",
        "StartTime": "YYYY-MM-DD HH:MM:SS",
        "EndTime": "YYYY-MM-DD HH:MM:SS"
    },
    // More topic objects if available
]
```
In case of an exception, the function returns a JSON object with an error message and a status code of 500:
```json
{
    "error": "Error message here"
}
```
<br><br>
# Function: `get_topic(topicID)`

### Description:
This function retrieves a specific topic from the database based on the provided `topicID`.

### Arguments:
- `topicID` (integer): Unique identifier of the topic to be retrieved.

### JSON Return:
The function returns a JSON object representing the specific topic based on the provided `topicID`.

#### Example JSON Response:
```json
{
    "TopicID": "Topic_ID",
    "Title": "Topic_Title",
    "Description": "Topic_Description",
    "StartTime": "YYYY-MM-DD HH:MM:SS",
    "EndTime": "YYYY-MM-DD HH:MM:SS"
}
```
In case of an exception, the function returns a JSON object with an error message and a status code of 500:
```json
{
    "error": "Error message here"
}
```
<br><br>
# Function: `get_votes(topicID)`

### Description:
This function retrieves all votes from the database based on the provided `topicID`.

### Arguments:
- `topicID` (integer): Unique identifier of the topic to retrieve votes for.

### JSON Return:
The function returns a JSON array containing objects representing all votes related to the specified `topicID`.

#### Example JSON Response:
```json
[
    {
        "VoteID": "Vote_ID_1",
        "UserID": "User_ID_1",
        "VoteType": "Vote_Type_1",
        "TopicID": "Topic_ID_1",
        "VoteTime": "YYYY-MM-DD HH:MM:SS"
    },
    // More vote objects if available
]
```
In case of an exception, the function returns a JSON object with an error message and a status code of 500:
```json
{
    "error": "Error message here"
}
```
<br><br>
# Function: `get_votes_by_user(userID)`

### Description:
This function retrieves all votes from the database associated with the provided `userID`.

### Arguments:
- `userID` (integer): Unique identifier of the user to retrieve votes for.

### JSON Return:
The function returns a JSON array containing objects representing all votes related to the specified `userID`.

#### Example JSON Response:
```json
[
    {
        "VoteID": "Vote_ID_1",
        "UserID": "User_ID_1",
        "VoteType": "Vote_Type_1",
        "TopicID": "Topic_ID_1",
        "VoteTime": "YYYY-MM-DD HH:MM:SS"
    },
    // More vote objects if available
]
```
In case of an exception, the function returns a JSON object with an error message and a status code of 500:
```json
{
    "error": "Error message here"
}
```
<br><br>
# Function: `register_esp(mac_address)`

### Description:
This function modifies the device ID and registered status of an existing ESP based on the provided `mac_address`.

### Arguments:
- `mac_address` (string): MAC address of the ESP to be modified.

### JSON Return:
The function returns a tuple containing a boolean value and either an object representing the modified ESP or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    {
        "DeviceIndex": "ESP_DeviceIndex",
        "DeviceID": "New_DeviceID",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": "YYYY-MM-DD HH:MM:SS",
        "Assigned": true,
        "Registered": true,
        "MacAddress": "ESP_MacAddress"
    }
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "ESP not found with the given macAddress"
]
```
<br><br>
# Function: `add_esp(mac_address)`

### Description:
This function creates a new ESP with the provided `mac_address`.

### Arguments:
- `mac_address` (string): MAC address for the new ESP.

### JSON Return:
The function returns a tuple containing a boolean value and either an object representing the newly created ESP or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    {
        "DeviceIndex": "ESP_DeviceIndex",
        "DeviceID": "ESP_DeviceID",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": null,
        "Assigned": false,
        "Registered": false,
        "MacAddress": "New_ESP_MacAddress"
    }
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "Error message here"
]
```
<br><br>
# Function: `unregister_esp(device_index)`

### Description:
This function unregisters a specific ESP based on the provided `device_index`.

### Arguments:
- `device_index` (integer): Device index of the ESP to be unregistered.

### JSON Return:
The function returns a tuple containing a boolean value and either an object representing the unregistered ESP or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    {
        "DeviceIndex": "ESP_DeviceIndex",
        "DeviceID": "ESP_DeviceID",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": "YYYY-MM-DD HH:MM:SS",
        "Assigned": true,
        "Registered": false,
        "MacAddress": "ESP_MacAddress"
    }
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "Error message here"
]
```
<br><br>
# Function: `unregister_all_esps()`

### Description:
This function unregisters all Electronic Service Providers (ESPs) from the system.

### Arguments:
None

### JSON Return:
The function returns a tuple containing a boolean value and either a success message or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    "All ESPs unregistered."
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "Error message here"
]
```
<br><br>
# Function: `create_topic(obj: voteHandling.VoteInformation)`

### Description:
This function adds a new topic (vote) to the database.

### Arguments:
- `obj` (voteHandling.VoteInformation): An object containing information about the topic to be created, including its title, description, start time, and end time.

### JSON Return:
The function returns a tuple containing a boolean value and either a success message or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    "Topic created successfully."
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "Error message here"
]
```
<br><br>
# Function: `create_user(username, deviceID)`

### Description:
This function registers a user to an Electronic Service Provider (ESP) by creating a new user in the database.

### Arguments:
- `username` (string): The username of the new user.
- `deviceID` (integer): The device index of the ESP to which the user will be associated.

### JSON Return:
The function returns a tuple containing a boolean value and either a success message or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    "User created successfully."
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "Error message here"
]
```
<br><br>
# Function: `assign_user_to_esp(userID, espID)`

### Description:
This function assigns a user to an Electronic Service Provider (ESP) by linking their device index to the ESP.

### Arguments:
- `userID` (integer): The ID of the user to be assigned.
- `espID` (integer): The ID of the ESP to which the user will be assigned.

### JSON Return:
The function returns a tuple containing a boolean value and either a success message or an error message.

#### Example JSON Response (Success):
```json
[
    true,
    "User assigned to ESP successfully."
]
```
In case of an exception, the function returns a tuple containing a boolean value (false) and an error message:
```json
[
    false,
    "Error message here"
]
```