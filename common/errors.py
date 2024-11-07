"""The exceptions to handle the errors"""


class HTMLFormattingError(BaseException):
    """The html file was not formatted properly!"""


class LogFileExistsError(BaseException):
    """The logging file doesn't exist under the current path"""

