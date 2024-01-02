## API Call Description

# API call name `getRegisteredESPs()`
### Link:
`GET /api/getRegisteredESPs`
### Format:
HTTP GET
### Payload Requirement:
None
### Description:
This API call retrieves all registered ESPs from the database.

### Return JSON:
The API call returns a JSON response containing information about all registered ESPs. The response includes details such as DeviceIndex, DeviceID, RegistrationTime, LastActiveTime, Assigned status, Registration status, and MacAddress for each ESP.

Example JSON Response:
```json
[
    {
        "DeviceIndex": 1,
        "DeviceID": "ESP001",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": "YYYY-MM-DD HH:MM:SS",
        "Assigned": true,
        "Registered": true,
        "MacAddress": "00:11:22:33:44:55"
    },
    {
        "DeviceIndex": 2,
        "DeviceID": "ESP002",
        "RegistrationTime": "YYYY-MM-DD HH:MM:SS",
        "LastActiveTime": null,
        "Assigned": false,
        "Registered": true,
        "MacAddress": "AA:BB:CC:DD:EE:FF"
    },
    ...
]
```
<br><br>
# API call name `getTopics()`

### Link:
`GET /api/getTopics`

### Format:
HTTP GET

### Payload Requirement:
None

### Description:
This API call retrieves all topics (votes) from the database.

### Return JSON:
The API call returns a JSON response containing information about all topics. Each topic includes details such as TopicID, Title, Description, StartTime, and EndTime.

Example JSON Response:
```json
[
    {
        "TopicID": 1,
        "Title": "Topic 1",
        "Description": "Description for Topic 1",
        "StartTime": "YYYY-MM-DD HH:MM:SS",
        "EndTime": "YYYY-MM-DD HH:MM:SS"
    },
    {
        "TopicID": 2,
        "Title": "Topic 2",
        "Description": "Description for Topic 2",
        "StartTime": "YYYY-MM-DD HH:MM:SS",
        "EndTime": "YYYY-MM-DD HH:MM:SS"
    },
    ...
]
```
<br><br>
# API call name `getTopic(topicID)`

### Link:
`GET /api/getTopic/<topicID>`

### Format:
HTTP GET

### Payload Requirement:
`topicID` (integer): The ID of the specific topic to retrieve.

### Description:
This API call retrieves a specific topic (vote) from the database based on the provided `topicID`.

### Return JSON:
The API call returns a JSON response containing information about the specified topic. The response includes details such as TopicID, Title, Description, StartTime, and EndTime for the selected topic.

Example JSON Response:
```json
{
    "TopicID": 1,
    "Title": "Topic 1",
    "Description": "Description for Topic 1",
    "StartTime": "YYYY-MM-DD HH:MM:SS",
    "EndTime": "YYYY-MM-DD HH:MM:SS"
}
```
<br><br>
# API call name `createTopic()`

### Link:
`POST /api/createTopic`

### Format:
HTTP POST

### Payload Requirement:
JSON payload with the following keys:
- `title` (string): Title of the topic.
- `description` (string): Description of the topic.
- `voteStartTime` (string): Start time of the vote (format: "YYYY-MM-DD HH:MM:SS").
- `voteEndTime` (string): End time of the vote (format: "YYYY-MM-DD HH:MM:SS").

### Description:
This API call creates a new topic (vote) by adding it to the database. It expects a JSON payload containing essential details about the topic, including its title, description, start time, and end time for the vote.

### Return JSON:
The API call returns a JSON response indicating the status of the topic creation.
- If the topic creation is successful, it returns a success message.
- If the topic creation fails due to invalid data or other issues, it returns an error message.

Example JSON Response (Success):
```json
{
    "message": "Topic created."
}
```
Example JSON Response (Failure):
```json
{
    "message": "Topic creation failed."
}
```
<br><br>
# API call name `assignUserToESP()`

### Link:
`POST /api/assignUserToESP`

### Format:
HTTP POST

### Payload Requirement:
JSON payload with the following keys:
- `userID` (integer): ID of the user to be assigned.
- `espID` (integer): ID of the ESP (Electronic Control Unit) to which the user is assigned.

### Description:
This API call assigns a user to a specific ESP (Electronic Control Unit) by linking their IDs in the system. It expects a JSON payload containing the `userID` and `espID` to perform the assignment.

### Return JSON:
The API call returns a JSON response indicating the status of the user assignment.
- If the user is successfully assigned to the ESP, it returns a success message.
- If there's an issue with the provided data or the assignment process, it returns an error message.

Example JSON Response (Success):
```json
{
    "message": "User assigned to ESP."
}
```
Example JSON Response (Failure):
```json
{
    "message": "Invalid data."
}
```
<br><br>