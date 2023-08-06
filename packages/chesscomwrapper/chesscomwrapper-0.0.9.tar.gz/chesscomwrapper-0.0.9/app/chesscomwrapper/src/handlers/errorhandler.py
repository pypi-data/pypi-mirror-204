class ChesscomError(Exception):
    """Base class for other exceptions"""
    pass

# 301 = if the URL you requested is bad, but we know where it should be; your client should remember and correct this to use the new URL in future requests
# 304 = if your client supports "ETag/If-None-Match" or "Last-Modified/If-Modified-Since" caching headers and the data have not changed since the last request
# 404 = we try to tell you if the URL is malformed or the data requested is just not available (e.g., a username for a user that does not exist)
# 410 = we know for certain that no data will ever be available at the URL you requested; your client should not request this URL again
# 429 = we are refusing to interpret your request due to rate limits; see "Rate Limiting" above

class MovedPermanentlyError(ChesscomError):
    """Raised wehn the URL you requested is bad, but we know where it should be; your client should remember and correct this to use the new URL in future requests"""
    pass
class CacheError(ChesscomError):    
    """Raised when the cache is not available"""
    pass
class MalformedUrlError(ChesscomError):
    """Raised when the URL is malformed"""
    pass

class DataNotAvailableError(ChesscomError):
    """Raised when the data requested is not available"""
    pass

class RateLimitError(ChesscomError):
    """Raised when the rate limit is exceeded"""
    pass

class OtherError(ChesscomError):
    """Raised when the data requested is not available"""
    pass

class ErrorHandler(object):
    """Base interface to handle errors"""
    
    def handle(self, error: MovedPermanentlyError):
        raise NotImplementedError
    
    def handle(self, error: CacheError):
        raise NotImplementedError
    
    def handle(self, error: MalformedUrlError):
        raise NotImplementedError
    
    def handle(self, error: DataNotAvailableError):
        raise NotImplementedError
    
    def handle(self, error: RateLimitError):
        raise NotImplementedError
    
    def handle(self, error: OtherError):
        raise NotImplementedError
    
    def handle(self, error: ChesscomError):
        raise NotImplementedError