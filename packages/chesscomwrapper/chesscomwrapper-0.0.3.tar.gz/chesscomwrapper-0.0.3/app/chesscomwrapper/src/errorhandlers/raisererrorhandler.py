from ..errorhandler import ErrorHandler
class RaiserErrorHandler(ErrorHandler):
    """ Concrete implementation of ErrorHandler """

    def handle(self, e):
        """How to handle an error"""
        raise e