from ..errorhandler import ErrorHandler, RateLimitError
class NoneErrorHandler(ErrorHandler):
    """ Concrete implementation of ErrorHandler """
    


    def handle(self, e):
        """Handle returning None"""
        if type(e) is RateLimitError:
            print("error: time limit")
        elif e is not None:
            print("error: " + str(e))
        return None
