import os
import sys
import pkg_resources

from dotenv import load_dotenv


def get_path(filename: str):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.abspath(
            os.path.join(
                os.path.split(
                    os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]
                )[0],
                filename,
            )
        )
    else:
        return pkg_resources.resource_filename("cgc", filename)


ENV_FILE_PATH = get_path(".env")
load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=True)

API_HOST = os.getenv("API_HOST")
CGC_SECRET = os.getenv("CGC_SECRET")
API_SECURE_CONNECTION = os.getenv("API_SECURE_CONNECTION", "yes")
SERVER_CERT_FILENAME = os.getenv("SERVER_CERT_FILENAME", "server.crt")
CERT_FILE_PATH = get_path(SERVER_CERT_FILENAME)
if API_SECURE_CONNECTION == "yes":
    __prefix = "https"
elif API_SECURE_CONNECTION == "no":
    __prefix = "http"
else:
    raise Exception("not defined API_SECURE_CONNECTION. set yes/no")

API_PORT = os.getenv("API_PORT")
API_URL = f"{__prefix}://{API_HOST}:{API_PORT}"
CONFIG_FILE_NAME = os.getenv("CONFIG_FILE_NAME")
TMP_DIR = os.getenv("TMP_DIR")
RELEASE = int(os.getenv("RELEASE"))
MAJOR_VERSION = int(os.getenv("MAJOR_VERSION"))
MINOR_VERSION = int(os.getenv("MINOR_VERSION"))
