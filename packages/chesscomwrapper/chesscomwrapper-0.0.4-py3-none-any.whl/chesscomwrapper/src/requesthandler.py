from .errorhandler import ErrorHandler

class RequestHandler(object):
    """ Interface for RequestHandler """
    
    errorHandler: ErrorHandler
    
    def doRequest(self, endpoint, ts=0):
        """Returns a dictionary of a player's info"""
        raise NotImplementedError