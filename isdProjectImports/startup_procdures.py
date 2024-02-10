# This is a stupid workaround cause flask has removed the ability the run code after stratup.

from isdProjectImports import  dbFunctions, logHandler
import app as mainApp

# Startup procedures.
with mainApp.app_context():
    logHandler.log(f'Server started.')
    logHandler.log(f'Finding active topic.')
    dbFunctions.find_active_topic(app, mainApp.globalVoteInformation)
    logHandler.log(f'Active topic: {mainApp.globalVoteInformation.title}, voteStartTime: {mainApp.globalVoteInformation.voteStartTime}, voteEndTime: {mainApp.globalVoteInformation.voteEndTime}')