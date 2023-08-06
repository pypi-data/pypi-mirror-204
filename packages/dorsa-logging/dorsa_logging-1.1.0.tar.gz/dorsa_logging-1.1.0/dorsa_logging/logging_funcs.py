import logging
import os

import dorsa_datetime


class app_logger():
    def __init__(self, name='app_logger', log_mainfolderpath='./app_logs', console_log=True, persian=True):
        """This class initializes a logger object that will be used for logging all things happening in the application. The logs are written in a log file, and can be shown
        in the console too. The logs are saved day by day, and on every app start/close.

        :param name: Logger object name, defaults to 'app_logger'
        :type name: str, optional
        :param log_mainfolderpath: Main folder path to create logs, defaults to './app_logs'
        :type log_mainfolderpath: str, optional
        :param console_log: Boolean value to determine whether to show logs in console or not, defaults to True
        :type console_log: bool, optional
        """

        # Create a custom logger
        self.logger_name = name
        self.logger = logging.getLogger(name)

        # set language
        self.persian = persian

        # create log folders and files
        self.console_log = console_log
        self.main_folderpath = log_mainfolderpath
        self.daily_folderpath = dorsa_datetime.get_date(persian=self.persian, folder_path=True)
        self.current_filepath = os.path.join(self.main_folderpath, self.daily_folderpath, dorsa_datetime.get_datetime(persian=self.persian, folder_path=True)+'.log')
        self.__create_mainfolder()
        self.__create_dailyfolder()

        # set log levels to write logs
        self.logger_level = logging.DEBUG
        self.console_level = logging.DEBUG
        self.file_level = logging.DEBUG
        self.logger.setLevel(self.logger_level)

        # current user
        self.current_username = 'root'

        # 1.Create log handlers
        # console handler
        if self.console_log:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel(self.console_level)

        # file handler
        self.file_handler = logging.FileHandler(filename=self.current_filepath, mode='w')
        self.file_handler.setLevel(self.file_level)


        # 2.Create formatters and add it to handlers (format of logging)
        # console formatter
        if self.console_log:
            self.console_format = logging.Formatter('%(levelname)s - %(message)s')
            self.console_handler.setFormatter(self.console_format)

        # file formatter
        self.file_format = logging.Formatter('%(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.file_format)

        # 3.Add handlers to the logger
        # console 
        if self.console_log:
            self.logger.addHandler(self.console_handler)
        # file
        self.logger.addHandler(self.file_handler)

    # create main folder to create logs 
    def __create_mainfolder(self):
        """This function creates the main folder to store log files.
        """

        # create if not exist
        if not os.path.exists(self.main_folderpath):
            os.mkdir(self.main_folderpath)

    # create daily folders to create logs
    def __create_dailyfolder(self):
        """This function creates day by day folders in the main folder, to storing the log files of each day.
        """

        # create if not exist
        if not os.path.exists(os.path.join(self.main_folderpath, self.daily_folderpath)):
            os.mkdir(os.path.join(self.main_folderpath, self.daily_folderpath))
 

    def __change_path_on_date_change(self):
        """This function is used to change log file path on date change (end of the day).
        """

        self.daily_folderpath = dorsa_datetime.get_date(persian=self.persian, folder_path=True)
        self.current_filepath = os.path.join(self.main_folderpath, self.daily_folderpath, dorsa_datetime.get_datetime(persian=self.persian, folder_path=True)+'.log')
        self.__create_dailyfolder()

        # file handler
        self.file_handler = logging.FileHandler(filename=self.current_filepath, mode='w')
        self.file_handler.setLevel(self.file_level)

        # file formatter
        self.file_format = logging.Formatter('%(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.file_format)

        # remove current handlers and add new handlers
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)
        # console 
        if self.console_log:
            self.logger.addHandler(self.console_handler)
        # file
        self.logger.addHandler(self.file_handler)

    # create new log
    def create_new_log(self, message='nothing', level=1):
        """This function creates a log with input message and log level.

        :param message: The log message, defaults to 'nothing'
        :type message: str, optional
        :param level: The log level (in int), an int value between [0, 5] specifying the log level.
                    0: debug
                    1: info
                    2: warning
                    3: error
                    4: critical error
                    5: excepion error
                    , defaults to 1
        :type level: int, optional
        """
        
        # get date and tme
        datetime = dorsa_datetime.get_datetime(persian=self.persian, folder_path=False)

        # change log path on date change
        if self.daily_folderpath != dorsa_datetime.get_date(persian=self.persian, folder_path=True):
            self.__change_path_on_date_change()


        # do log by levels
        # debug
        if level == 0:
            self.logger.debug(msg='%s - %s : %s\n------------------------------------------------------------------------------' % (datetime, self.current_username, message))
        #
        # info
        elif level == 1:
            self.logger.info(msg='%s - %s : %s\n------------------------------------------------------------------------------' % (datetime, self.current_username, message))
        #
        # warning
        elif level == 2:
            self.logger.warning(msg='%s - %s : %s\n------------------------------------------------------------------------------' % (datetime, self.current_username, message))
        #
        # error
        elif level == 3:
            self.logger.error(msg='%s - %s : %s\n------------------------------------------------------------------------------' % (datetime, self.current_username, message))
        #
        # critical error
        elif level == 4:
            self.logger.critical(msg='%s - %s : %s\n------------------------------------------------------------------------------' % (datetime, self.current_username, message))
        #
        # exception error (with logging exception message)
        elif level == 5:
            self.logger.exception(msg='%s - %s : %s\n------------------------------------------------------------------------------' % (datetime, self.current_username, message))

    # set current logged-in user to logger
    def set_current_user(self, current_username=None):
        """This function sets the input username as the current user.

        :param current_username: Current username that logged in the app
        :type current_username: str, optional
        """
        
        self.current_username = current_username if current_username!=None else 'root'

