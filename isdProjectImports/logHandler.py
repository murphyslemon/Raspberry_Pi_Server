from datetime import datetime

# Create logfile name with timestamp.
# This log file will be used until the server is restarted.
current_logfile_name = "FlaskLog-" + str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt" 
log_folder = "Logs/"

# Initialize the log file.
with open(log_folder + current_logfile_name, 'w') as logFile:
    logFile.write(f'Timestamp format: DD-MM-YYYY  HH-MM-SS:\n')
    logFile.write(f'Log file created at: {datetime.now()}\n')


def log(message):
    """
    Append a timestamped message to the current log file.

    Args:
        - message (str): The log message to be appended.
    """

    with open(log_folder + current_logfile_name, 'a') as logFile:
        logFile.write(f'{datetime.now().strftime("%d-%m-%Y  %H-%M-%S")}: {message}\n')
    return


def custom_log(logfile_name, message, logfile_path = ""):
    """
    Append a timestamped message to a specified log file.

    Args:
        - logfile_name (str): The name of the log file (including extension) to which the message will be appended.
        - message (str): The log message to be appended.
        - logfile_path (str): The optional path to the directory containing the log file. Defaults to the root directory.
    """

    with open(logfile_path + logfile_name, 'a') as logFile:
        logFile.write(f'{datetime.now().strftime("%d-%m-%Y  %H-%M-%S")}: {message}\n')
    return