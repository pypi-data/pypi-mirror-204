import os

APP_DIR = os.path.join(os.path.expanduser('~'), '.lecture_automator')

def get_app_dir() -> str:
    if not os.path.exists(APP_DIR):
        os.makedirs(APP_DIR)
    return APP_DIR
