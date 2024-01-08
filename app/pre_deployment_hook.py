import os

APP_NAME = os.getenv('APP_NAME', 'temp')
APP_ENV = os.getenv('APP_ENV', 'dev')
def handle(*args):
    print("Running pre deployment hook")

    if APP_NAME == 'test' or APP_ENV == 'prod':
        print("Running on remote server. Executing init_setup.sh")
        os.system(f"sh {os.path.dirname(os.path.realpath(__file__))}/init_setup.sh")