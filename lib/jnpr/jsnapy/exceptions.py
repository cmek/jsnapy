"""
jsnapy exceptions
"""

class JsnapyException(Exception):
    """
    Base exception class.
    """
    def __init__(self, message=''):
        super(JsnapyException, self).__init__(message)
        self.strerror = message

class JsnapyRenderError(JsnapyException):
    """
    Used to report renderer exceptions.
    """
