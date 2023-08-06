# Logging
Logging is Python package that contains a class to log an application happenings.

## Installation and updating

Use the package manager  [pip](https://pypi.org/project/dorsa-logging/)  to install package.

## Usage
Class Methods:
-   app_logger.create_new_log --> This function creates a log with input message and log level.
-   app_logger.set_current_user --> This function sets the input username as the current user.
#### Demo of the features:
```python
from  logging_funcs  import  app_logger

logger = app_logger()

logger.set_current_user(current_username='DORSA')
logger.create_new_log(message='This is a debug message', level=0)
logger.create_new_log(message='This is a info message', level=1)
logger.create_new_log(message='This is a warning message', level=2)
logger.create_new_log(message='This is a error message', level=3)
logger.create_new_log(message='This is a critical error message', level=4)
logger.create_new_log(message='This is a exception error message', level=5)
```
## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)

