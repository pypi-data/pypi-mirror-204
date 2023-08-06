import base64
import logging
import os
import pathlib
import shlex
import subprocess
import time
from typing import List

from foodsale import pathfromglob

from giftmaster import timestamp


class SigntoolPrivatekeyException(Exception):
    def __init__(self, message="signtool couldn't get a private key"):
        self.message = message
        super().__init__(self.message)


def unsign_cmd(*paths, signtool="signtool"):
    cmd = [
        signtool,  # fixme
        "remove",
        "/v",
        "/s",
    ]

    cmd.extend([str(pathlib.Path(path).resolve()) for path in paths])

    return cmd


def get_abs_path(file_list: List) -> List[pathlib.Path]:
    return [str(pathlib.Path(_str).resolve()) for _str in file_list]


class SignTool:
    HASH_ALGORITHM = "SHA256"
    url_manager = timestamp.TimeStampURLManager()

    def __init__(self, files_to_sign):
        self.files_to_sign = get_abs_path(files_to_sign)

    @classmethod
    def from_list(cls, paths: List[str], signtool: List[str]):
        tool = cls(paths)
        tool.set_path(signtool)
        return tool

    def set_path(self, globs: List[str]):
        def validate(globs):
            paths = pathfromglob.abspathglob(*globs)
            if len(paths) < 1:
                msg = f"no glob from list {globs} matche any paths on filesystem"
                logging.exception(msg)
                raise ValueError(msg)

            path = paths[0]

            if len(paths) > 1:
                msg = (
                    f"globs {globs} match too many paths on filesystem: {paths}.  "
                    f"Not sure i'm choosing the one you want, namely {path}.  Its "
                    "the first one in the list"
                )
                logging.warning(msg)

            if not path.exists():
                msg = f"{path} does not exist"
                logging.exception(msg)
                raise ValueError(msg)

            return path

        self.path = validate(globs)

    def remove_already_signed(self):
        done = []
        for path in self.files_to_sign:
            ret = self.run(self.verify_cmd(path))
            if ret == 0:
                logging.debug(f"{path} is already signed")
                done.append(path)
        self.files_to_sign = list(set(self.files_to_sign) - set(done))

    def run(self, cmd) -> int:
        if not cmd:
            logging.debug(f"skipping running cmd because cmd is empty")
            return 0

        try:
            logging.debug(shlex.join(cmd))
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError as ex:
            logging.exception(ex)
            raise ex

        epoch = int(time.time())
        stdout, stderr = process.communicate()

        log_path = pathlib.Path(f"signtool-{epoch}.log")
        log_path.write_text(stdout.decode())

        err_path = pathlib.Path(f"signtool-{epoch}.err")
        err_path.write_text(stderr.decode())

        log_cmd_path = pathlib.Path(f"signtool-{epoch}-cmd.txt")
        log_cmd_path.write_text(shlex.join(cmd))
        
        if err := stderr.decode():
            if "No private key is available" in err:
                raise SigntoolPrivatekeyException(err)
            logging.warning(err)

        logging.debug(f"singtool.exe's returncode: {process.returncode}")
        return process.returncode

    def verify_cmd(self, *paths: List[str]):
        """
        signtool.exe verify /debug /v /pa C:\dxLib.dll
        """
        prefix = [
            str(self.path),
            "verify",
            "/debug",
            "/v",
        ]

        x = ["/pa"]
        x.extend(paths)

        cmd = []
        cmd.extend(prefix)
        cmd.extend(x)

        return cmd

    def decode_credentials(self, _str) -> str:
        base64_bytes = _str.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode("ascii")

    def sign_cmd(self):
        if not self.files_to_sign:
            return None

        if not (password := os.environ.get("SAFENET_CLIENT_CREDENTIALS", "")):
            msg = (
                "credentials for signing could not be found from "
                "$ENV:SAFENET_CLIENT_CREDENTIALS"
            )
            logging.critical(msg)
            raise ValueError(msg)

        password_decoded = self.decode_credentials(password)

        cmd = [
            str(self.path),
            "sign",
            "/debug",
            "/v",
            "/f",
            "c:/sectigo.cer",
            "/csp",
            "eToken Base Cryptographic Provider",
            "/kc",
            password_decoded,
            "/n",
            "Streambox",
            "/fd",
            type(self).HASH_ALGORITHM,
            "/d",
            "Streambox",
            "/tr",
            type(self).url_manager.url,
            "/td",
            type(self).HASH_ALGORITHM,
        ]

        cmd.extend(self.files_to_sign)

        return cmd


def main():
    pass


if __name__ == "__main__":
    main()
