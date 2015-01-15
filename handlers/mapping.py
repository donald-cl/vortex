'''
    Author: Donald Hui
    Description: Handles application route/url mapping to handlers.
    Date started: Dec 5 2014
'''

from handlers import *

mappings = [
        (r"/", MainHandler),
        ]
