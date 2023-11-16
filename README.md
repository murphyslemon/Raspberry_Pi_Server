
# International Sensor Development Project: Raspberry Pi Server
## Ver 1.0

## Table of Contents
1. Goals/requirements
2. Raspberry related teams
3. Voting device related teams

## Goals/requirements
### Goals
- A working server (raspberry pi) that collects votes and serves a website to guide voting device registration and final vote tally.
- The system shall support anonymous and registered voting.
- The system shall be as self explanatory and simple to use as possible. (A HR person should be able to handle it without a 30 minute lecture :) )
- The voting device shall be as power efficient as possible.
- Scalable (The voting remotes shall be plug and play)

## Raspberry related teams
### Votes processing
**Magnus / Aleksi**
Basically the backend server. Handles organizing votes, receiving the votes from end-user devices, tallying and forwarding the results to any services that require them. Handles confirmation of received votes

### Printer/PDF
**Javi**
Takes results of votes and prints them and or creates a PDF for users. (Can also support other teams)

### Display votes
**Jefferson / Adrian / Andrea**
Handles displaying the end results of votes for the users, most likely through a website hosted on the raspberry.

## Voting device related teams
Voting device repository can be accessed [here](https://github.com/murphyslemon/Voting_Device).
### Programming
**Felix / Nadim**
Handles any end device related programming.

### Design
**Timo / Daniel**
Handles mechanical design of the device.

### Electronics design
**Mong / Tuomas**
Handles design of device electronics.

### (G)UI
**Frank / Xuan**
User interface related design.
