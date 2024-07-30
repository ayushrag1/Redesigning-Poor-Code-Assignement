import datetime

class Logger:
    def __init__(self, log_file='library.log'):
        """
        Initializes the Logger with a specified log file.

        Parameters:
        log_file (str): The file where logs will be written. Defaults to 'library.log'.
        """
        self.log_file = log_file

    def log(self, message):
        """
        Logs a message to the log file with the current timestamp.

        Parameters:
        message (str): The message to be logged.
        """
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{datetime.datetime.now()} - {message}\n")
        except IOError as e:
            print(f"An error occurred while writing to the log file: {e}")

    def log_custom(self, message, log_type="INFO"):
        """
        Logs a message to the log file with a specified log type and timestamp.

        Parameters:
        message (str): The message to be logged.
        log_type (str): The type of log (e.g., 'INFO', 'WARNING', 'ERROR'). Defaults to 'INFO'.
        """
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{datetime.datetime.now()} [{log_type}] - {message}\n")
        except IOError as e:
            print(f"An error occurred while writing to the log file: {e}")
