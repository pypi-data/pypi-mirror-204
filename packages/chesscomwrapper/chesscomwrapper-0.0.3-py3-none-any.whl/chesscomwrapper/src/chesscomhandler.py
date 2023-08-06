from .requesthandler import RequestHandler
from .errorhandler import ErrorHandler, MovedPermanentlyError, CacheError, MalformedUrlError, DataNotAvailableError, RateLimitError, OtherError
from .errorhandlers.noneerrorhandler import NoneErrorHandler
from .errorhandlers.raisererrorhandler import RaiserErrorHandler
from .requesthandlers.singletonrequesthandler import SingletonRequestHandler
class ChesscomHandler(object):
    """ Interface for RequestHandler """
    
    errorHandler: ErrorHandler
    requestHandler: RequestHandler
    
    def doRequest(self, endpoint, ts=1):
        """Returns a dictionary of a player's info"""
        try:
            print("Handling request to: " + endpoint)
            response = self.requestHandler.doRequest(endpoint, ts-1)
            if response.status_code != 200:
                if response.status_code == 301:
                    raise MovedPermanentlyError("Moved Permanently", response.status_code, response.text, endpoint)
                elif response.status_code == 304:
                    raise CacheError("Cache error", response.status_code, response.text, endpoint)
                elif response.status_code == 404:
                    raise MalformedUrlError("Data not available", response.status_code, response.text, endpoint)
                elif response.status_code == 410:
                    raise DataNotAvailableError("Data not available", response.status_code, response.text, endpoint)
                elif response.status_code == 429:
                    raise RateLimitError("Time limit exceeded", response.status_code, response.text, endpoint)
                else:
                    raise OtherError("Other error", response.status_code, response.text, endpoint)
            else:
                return response
        except Exception as e:
            response = self.errorHandler.handle(e)
        
        return response