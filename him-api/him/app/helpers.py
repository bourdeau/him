from rest_framework.views import exception_handler
import logging
import time
from random import randint

logger = logging.getLogger(__name__)

import pathlib
from os import listdir
from os.path import isfile, join

from him.app.api import TinderAPIClient
from him.settings import BASE_DIR, config


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    return response


class Base:
    def __init__(self) -> None:
        self.logger = logger
        self.tinderapi = TinderAPIClient(token=config["x_auth_token"])

    def sleep_short(self) -> None:
        time.sleep(randint(100, 1000) / 1000)

    def sleep_medium(self) -> None:
        time.sleep(randint(1000, 2000) / 1000)

    def sleep_long(self) -> None:
        time.sleep(randint(2000, 5000) / 1000)


def get_list_files(relative_path_dir: str, extension=".json"):

    files_path = join(BASE_DIR, relative_path_dir)

    for f in listdir(files_path):
        if (
            isfile(join(files_path, f))
            and pathlib.Path(join(files_path, f)).suffix == extension
        ):
            yield join(files_path, f)