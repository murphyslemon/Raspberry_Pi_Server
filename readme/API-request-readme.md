# API Endpoints.

- ##  **GET all registered ESPs**
    
    -   **Endpoint:** `/api/getRegisteredESPs`
    -   **Method:** `GET`
    -   **Payload:** None
    -   **Returns:** JSON array containing information about all registered ESPs + HTTP status code.
 Example return:
```json
[
    {
        "DeviceIndex": 1,
        "DeviceID": "ABC123",
        "RegistrationTime": "2024-01-16 12:30:45",
        "LastActiveTime": "2024-01-16 15:45:20",
        "Assigned": true,
        "Registered": true,
        "MacAddress": "00:11:22:33:44:55"
    },
    {
        "DeviceIndex": 2,
        "DeviceID": "XYZ789",
        "RegistrationTime": "2024-01-15 09:10:30",
        "LastActiveTime": "2024-01-16 14:20:55",
        "Assigned": false,
        "Registered": true,
        "MacAddress": "AA:BB:CC:DD:EE:FF"
    },
    // ... additional entries for other registered ESPs
]
```
- ##   **GET all Topics (votes)**
    
    -   **Endpoint:** `/api/getTopics`
    -   **Method:** `GET`
    -   **Payload:** None
    -   **Returns:** JSON array containing information about all topics (votes) + HTTP status code.
     Example return:
```json
[
    {
        "TopicID": 1,
        "Title": "Sample Topic 1",
        "Description": "Description for Sample Topic 1",
        "StartTime": "2024-01-16 12:30:00",
        "EndTime": "2024-01-16 15:30:00"
    },
    {
        "TopicID": 2,
        "Title": "Sample Topic 2",
        "Description": "Description for Sample Topic 2",
        "StartTime": "2024-01-17 09:00:00",
        "EndTime": "2024-01-17 12:00:00"
    },
    // ... additional entries for other topics
]
```
- ##   **GET Specific Topic (vote)**
    
    -   **Endpoint:** `/api/getTopic/<topicID>`
    -   **Method:** `GET`
    -   **Payload:** None
    -   **Returns:** JSON object containing information about the specified topic (vote) identified by `<topicID>` + HTTP status code.
     Example return:
```json
{
    "TopicID": 1,
    "Title": "Sample Topic 1",
    "Description": "Description for Sample Topic 1",
    "StartTime": "2024-01-16 12:30:00",
    "EndTime": "2024-01-16 15:30:00"
}
```
- ##   **Create new Topic (vote)**
    
    -   **Endpoint:** `/api/createTopic`
    -   **Method:** `POST`
    -   **Payload:** JSON
    Example payload:
```json
   {
    "Title": "TEXT",
    "Description": "TEXT",
    "StartTime": "YYYY-MM-DD HH:MM:SS",
    "EndTime": "YYYY-MM-DD HH:MM:SS"
}
```
-   -   **Returns:** JSON message indicating the success or failure of the topic creation + HTTP status code.
     Example return:
```json
[
"message": "Topic created successfully."
]
```
- ##   **Assign user to ESP**
    
    -   **Endpoint:** `/api/assignUserToESP`
    -   **Method:** `POST`
    -   **Payload:** JSON
    Example payload:
```json
{
    "username": "TEXT",
    "espID": "INT"
}
```
-   -   **Returns:** JSON message indicating the success or failure of assigning the user to the ESP + HTTP status code.
     Example return:
```json
{
    "message": "User assigned to ESP successfully."
}
```
- ##   **Unassign ESP**
    
    -   **Endpoint:** `/api/unassignESP`
    -   **Method:** `POST`
    -   **Payload:** JSON
    Example payload:
```json
{
    "espID": "INT"
}
```
-   -   **Returns:** JSON message indicating the success or failure of unassigning the specified ESP + HTTP status code.
     Example return:
```json
{
    "message": "ESP1 unassigned."
}
```
- ##   **Unassign all ESPs**
    
    -   **Endpoint:** `/api/unassignAllESPs`
    -   **Method:** `POST`
    -   **Payload:** None
    -   **Returns:** JSON message indicating the success or failure of unassigning all ESPs + HTTP status code.
         Example return:
```json
{
    "message": "All ESPs unassigned."
}
```
- ## **Get Votes by Topic ID**
-   **Endpoint:** `/api/getVotes/<int:topicID>`
-   **Method:** `GET`
-   **Parameters:**
    -   `topicID` (int): The unique ID of the topic to retrieve votes for.
-   **Returns:**
    -   **Success (200):** A JSON response containing information about the votes related to the specified topic. The response includes a list of dictionaries, each representing a vote. The keys in each dictionary include:
        
        -   `VoteID`: The unique ID of the vote.
        -   `UserID`: The ID of the user who cast the vote.
        -   `VoteType`: The type of the vote.
        -   `TopicID`: The ID of the topic the vote is related to.
        -   `VoteTime`: The timestamp of when the vote was cast.
    -   **Error (500):** A JSON response with an error message in case of an exception during the retrieval process.
        
-   **Example:**
    ```json
    {
	"VoteID": 1,
	"UserID": 123,
	"VoteType": "upvote",
	"TopicID": 456,
	"VoteTime": "2024-02-08 14:30:00"
	},
	{
	"VoteID": 2,
	"UserID": 456,
	"VoteType": "downvote",
	"TopicID": 456,
	"VoteTime": "2024-02-08 14:35:00"
	}
	// ... additional entries.
    ```
-   **Raises:**
    -   **Error (500):** A JSON response with an error message if an exception occurs during the process of retrieving votes.

- ## **Get Unassigned ESP Devices**
-   **Endpoint:** `/api/getUnassignedESPs`
-   **Method:** `GET`
-   **Parameters:**
-   **Returns:**
    -   **Success (200):** A JSON response containing information about unassigned ESP devices. Each device is represented by a dictionary with keys including:
        
        -   `DeviceIndex`: The unique index of the device.
        -   `DeviceID`: The ID of the ESP device.
        -   `RegistrationTime`: The timestamp when the device was registered.
        -   `LastActiveTime`: The timestamp of the device's last activity.
        -   `Assigned`: Boolean indicating whether the device is assigned (False for unassigned).
        -   `Registered`: Boolean indicating whether the device is registered.
        -   `MacAddress`: The MAC address of the ESP device.
    -   **Error (500):** A JSON response with an error message in case of an exception during the retrieval process.
        
-   **Example:**
```json
    {
        "DeviceIndex": 1,
        "DeviceID": "ESP123",
        "RegistrationTime": "2024-02-08 14:30:00",
        "LastActiveTime": "2024-02-08 15:00:00",
        "Assigned": false,
        "Registered": true,
        "MacAddress": "00:11:22:33:44:55"
    },
    {
        "DeviceIndex": 2,
        "DeviceID": "ESP456",
        "RegistrationTime": "2024-02-08 14:45:00",
        "LastActiveTime": "2024-02-08 15:10:00",
        "Assigned": false,
        "Registered": true,
        "MacAddress": "11:22:33:44:55:66"
    }
    // ... additional entries.
```   
-   **Raises:**
    -   **Error (500):** A JSON response with an error message if an exception occurs during the process of retrieving votes.