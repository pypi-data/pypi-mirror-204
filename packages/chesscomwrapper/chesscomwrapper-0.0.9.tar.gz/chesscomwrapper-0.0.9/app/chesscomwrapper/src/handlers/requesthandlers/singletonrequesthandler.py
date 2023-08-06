from ..requesthandler import RequestHandler
from time import sleep
import requests
import threading


class SingletonRequestHandler(RequestHandler):
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """

        def spam(self):
            """ Test method, return singleton id """
            return id(self)

    # storage for the instance reference
    __instance = None

    def doRequest(self, endpoint, ts=0):
        """Returns a dictionary of a player's info"""
        
        with self.lock:
            if ts > 0:
                print("Sleeping for " + str(ts) + " milliseconds")
                sleep(ts/1000)
            response = requests.get(endpoint)
            if response.status_code == 429:
                if ts < 30:
                    return self.doRequest(endpoint, (ts + 3))
        # print(response.json())
        return response
        
        

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if SingletonRequestHandler.__instance is None:
            # Create and remember instance
            SingletonRequestHandler.__instance = SingletonRequestHandler.__impl()
            SingletonRequestHandler.__instance.lock = threading.Lock()
        print(SingletonRequestHandler.__instance)
        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = SingletonRequestHandler.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
