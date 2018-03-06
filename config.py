import os


class Config(object):
    # needed by flask wtf for CSRC
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YOU WILL NEVER GUESS'