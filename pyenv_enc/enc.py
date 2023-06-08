"""
GPG based config and environment file encryption utility.

"""
import os
import re
import shlex
import subprocess
import argparse

import json
import yaml
from dotenv import dotenv_values

_MARKUP = "!ENC#~ "


def parse_arguments():
    parser = argparse.ArgumentParser("ENC", description=__doc__)

    parser.add_argument("filelist", nargs='+', help="File(s) to process.")

    parser.add_argument("-u", "--user", default=None,
                        help="GPG user ID (default $USER).")

    parser.add_argument("-e", "--encrypt", default=False,
                        action="store_true", help="Specify for encryption.")

    parser.add_argument("-d", "--decrypt", default=False,
                        action="store_true", help="Specify for decryption.")

    args = parser.parse_args()

    return args


def exec(command, *, stdin=None, capture=True) -> argparse.Namespace:
    """
    Execute a command with arguments and optional stdin value.
    Args:
        capture bool: Whether to capture the stdout and stderr.
    Returns: subprocess.CompletedProcess
    """
    cmdlist = shlex.split(command)
    if stdin is not None:
        stdin = str(stdin)
        stdin = bytes(stdin, encoding='utf-8')
    result = subprocess.run(cmdlist, shell=False,
                            capture_output=capture, input=stdin)
    return result


def check_gpg_pubkey(userid) -> bool:
    """
    Check if public key exists for userid. Else create a new one.
    
    """
    res = exec(f"gpg --list-keys {userid}")
    if res.returncode == 0:
        return True

    print("Note!! No GPG key set under your username. Creating a new one.")
    print("Quick reference: http://irtfweb.ifa.hawaii.edu/~lockhart/gpg/")

    expiration = 'none'
    command = f"gpg --quick-generate-key {userid} future-default default {expiration}"
    if exec(command, capture=False).returncode != 0:
        print("Error - failed to create GPG key for userid", userid)
        return False

    # confirm key exists
    res = exec(f"gpg --list-keys {userid}")
    if res.returncode == 0:
        return True
    else:
        print("Error - no public key found:", userid)
        return False


def read_file(file: str) -> dict:
    with open(file, 'r') as fp:
        if file.endswith(".yaml") or file.endswith(".yml"):
            # print("Loading YAML file:", file)
            return yaml.safe_load(fp)
        elif file.endswith(".json"):
            # print("Loading JSON file:", file)
            return json.load(fp)
        else:
            # print("Loading ENV file:", file)
            return dotenv_values(stream=fp)


def save_file(file: str, data: dict):
    with open(file, 'w+') as fp:
        if file.endswith(".yaml") or file.endswith(".yml"):
            yaml.dump(data, fp, indent=4)
        elif file.endswith(".json"):
            json.dump(data, fp, indent=4)
        else:
            for key, val in data.items():
                if type(val) == str:
                    val = f'"{val}"'
                fp.write(f"{key}={val}\n")
            fp.flush()


def gpg_encrypt(userid: str, value: str) -> str:
    """
    Encrypt a value using GPG and userid.
    Returns: encrypted value.

    """
    command = f"gpg --yes --armor -e -r {userid}"
    encvalue = exec(command, stdin=value).stdout
    lines = str(encvalue, encoding="utf-8").split("\n")
    # Remove the PGP and empty lines
    encvalue = " ".join(lines[2:-2])
    # Add a markup to indicate encryption
    return _MARKUP + encvalue


def gpg_decrypt(value: str) -> str:
    """
    Decrypt a value using GPG.
    Returns: decrypted value.

    """
    # Remove the markup
    value = value.lstrip(_MARKUP)
    # Add the PGP and empty lines
    value = value.replace(" ", "\n")
    value = "-----BEGIN PGP MESSAGE-----\n\n" + value
    value = value + "-----END PGP MESSAGE-----"
    command = f"gpg -d"
    encvalue = exec(command, stdin=value).stdout
    return str(encvalue, encoding="utf-8")


def encrypted(value : str) -> bool:
    return type(value) == str and value.startswith(_MARKUP)


def encrypt_data(userid: str, data: dict) -> dict:
    """
    Recursively loop over a dictionary and encrypt all string fields.
    
    """
    for key, value in data.items():
        # encrypt the string values
        if not encrypted(value):
            data[key] = gpg_encrypt(userid, value)
        elif type(value) == dict:
            data[key] = encrypt_data(userid, value)
        elif type(value) == list:
            for i in range(len(value)):
                if not encrypted(value[i]):
                    value[i] = gpg_encrypt(userid, value[i])
            data[key] = value
    return data


def decrypt_data(data: dict) -> dict:
    """
    Recursively loop over a dictionary and decrypt all string fields.
    
    """
    for key, value in data.items():
        # decrypt the string values
        if encrypted(value):
            data[key] = gpg_decrypt(value)
        elif type(value) == dict:
            data[key] = decrypt_data(value)
        elif type(value) == list:
            for i in range(len(value)):
                if encrypted(value[i]):
                    value[i] = gpg_decrypt(value[i])
            data[key] = value

    return data



def main():
    args = parse_arguments()

    if args.user is None:
        args.user = os.environ.get('USER', None)
        if args.user is None:
            raise RuntimeError(
                "Environment variable $USER undefined. Please provide --user value.")

    # Check GPG setup
    check_gpg_pubkey(args.user)

    for filepath in args.filelist:
        filepath = os.path.expanduser(filepath)

        # Read the file
        content = read_file(filepath)

        if args.decrypt:
            data = decrypt_data(content)
            save_file(filepath, data)
            print("Decrypt:", filepath)

        if args.encrypt:
            data = encrypt_data(args.user, content)
            save_file(filepath, data)
            print("Encrypt:", filepath)

        if args.decrypt == False and args.encrypt == False:
            pattern = re.compile(rf"{_MARKUP}")
            match = pattern.search(str(content))
            if match is None:
                data = encrypt_data(args.user, content)
                save_file(filepath, data)
                print("Encrypt:", filepath)
            else:
                data = decrypt_data(content)
                save_file(filepath, data)
                print("Decrypt:", filepath)

if __name__ == "__main__":
    main()
