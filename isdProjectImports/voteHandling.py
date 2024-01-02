class VoteInformation:

    # Vote object is initialized with NULL values.
    def __init__(self):
        self.topicID = None
        self.title = None
        self.description = None
        self.voteStartTime = None
        self.voteEndTime = None
    
    def updateVoteInformation(self, title, description, voteStartTime, voteEndTime):
        self.title = title
        self.description = description
        self.voteStartTime = voteStartTime
        self.voteEndTime = voteEndTime
