import os
from datetime import datetime
import logging
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# -------------------------------SET LOGGER (daily log file)------------------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # INFO BY DEFAULT

# File handler
log_file_name = f"A360_BOT_IMPORT_LOGS_{datetime.now().strftime('%d-%b-%Y')}.log"
log_file_path = os.path.join(os.environ["USERPROFILE"], "Documents", log_file_name)
fh = logging.FileHandler(log_file_path)
fh.setLevel(logging.INFO)

# Common formatter for all handlers
formatter = logging.Formatter(fmt='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s', datefmt='%H:%M:%S')
fh.setFormatter(formatter)

# Add handlers
logger.addHandler(fh)

DESCRIPTION = "Given control room url, username, apikey and folder path, this script will import all bots from the " \
              "given folder to A360 CR"

parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument("--cr_url", dest="cr_url", type=str,
                    help="Control Room URL", required=True)

parser.add_argument("--username", dest="username", type=str,
                    help="Full username", required=True)

parser.add_argument("--api_key", dest="api_key", type=str,
                    help="API Key from user", required=True)

parser.add_argument("--folder_path", dest="folder_path", type=str,
                    help="Folder path where bot exports are located", required=True)

args = parser.parse_args()

cr_url = str(args.cr_url)
username = str(args.username)
api_key = str(args.api_key)
folder_path = str(args.folder_path)


def get_token():
    # Get token using api_key
    uri = f"{cr_url}/v1/authentication"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "username": username,
        "apiKey": api_key
    }

    r = requests.post(uri, json=payload, headers=headers, verify=False)

    r.raise_for_status()
    logger.info("Token fetched")
    return r.json()["token"]


def upload_file(file_path):
    try:
        url = f"{cr_url}/v2/blm/import"
        headers = {
            # "Content-Type": "multipart/form-data", BE VERY CAREFUL,IF YOU SPECIFY THIS IN HEADER IT DOES NOT GET IMPORTED
            "X-Authorization": token
        }
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {'upload': (filename, f)}
            data = {
                'actionIfExisting': 'SKIP',
                'publicWorkspace': True
            }
            print("Proceeding to import: " + filename)
            logger.info("Proceeding to import: " + filename)
            response = requests.post(url, headers=headers, files=files, data=data, verify=False)
            response.raise_for_status()  # throw error if response is not 20x
            print(f"Status for {filename} import: " + str(response.status_code))
            logger.info(f"Status for {filename} import: " + str(response.status_code))
            return response
    except Exception as e:
        print(f"Could not import {filename}. Error: {str(e)}")
        logger.error(f"Could not import {filename}. Error: {str(e)}")


def main(folder_path):
    logger.info("Starting bot import from this folder: " + folder_path)
    file_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
    # One by one
    # for file in file_paths:
    #     print("Importing following file: " + os.path.join(folder_path, file))
    #     f.upload_file(os.path.join(folder_path, file), token)

    # Multi-thread
    with ThreadPoolExecutor() as executor:
        results = [executor.submit(upload_file, file_path) for file_path in file_paths]
        for f in as_completed(results):
            pass


if __name__ == '__main__':
    logger.info("### START ###")
    token = get_token()
    logger.info("Starting import from folder: " + folder_path)
    main(folder_path=folder_path)
    logger.info("### END ###")
