# PyEnv-Encrypt
GPG based env file encryptor utility.

PyEnv-Encrypt selectively encrypts and decrypts the fields of config files keeping the keys readable. For example, consider an environment variable file `.env` with the following values.

```bash
SOMEVAR="hello world"
ANOTHERVAR="test"
```
Running `pyenc .env` will encrypt the text fields into:

```bash
SOMEVAR="!ENC#~ hQGMA8pKDfwTzwbdAQv/c0/3Had47hxV6zuNmkBuOjv3bSGGGWzLGHVAN7ryL3tx =Y8Nr"
ANOTHERVAR="!ENC#~ hQGMA8pKDfwTzwbdAQv+JRBiVJB3rFqjONyXbBuN6pwzfHkHR43rbSIGX0o/B0zU =ljcz"
```

## Features
- Encryption support for the following file types.
    - .env
    - yaml
    - json
- Recursive update of all text fields.
- Automatic decision of encryption or decryption based on file contents.

## Installation
You can install `pyenv-encrypt` directly from [PyPI](https://pypi.org/project/pyenv-encrypt) using `pip`.

```sh
pip install pyenv-encrypt
```

Alternatively, clone this repo and install with `pip`.
```sh
git clone https://github.com/akhlakm/pyenv-encrypt.git
cd pyenv-encrypt
pip install -e .
```

### Dependencies
The `gpg` utility must be installed in your system. GPG comes built-in with most versions of Linux OS. For Mac, use homebrew: `brew install gpg`.

See the official [installation instructions](https://gnupg.org/download/) for more info. Run the following command to check if GPG is installed.

```sh
gpg --version
```

Python dependencies:
- python-dotenv
- pyyaml


## Commandline Usage
After installation, use the `pyenc` command to encrypt or decrypt your config/env files directly from terminal.

```sh
pyenc .env
```

Multiple files can also be processed.
```sh
pyenc .env vault.yaml data.json
```

`pyenc` will toggle between encryption and decryption. To force encryption or decryption specify `-e` or `-d` respectively.

```sh
pyenc -e .env vault.yaml data.json
```

To make sure you do not commit unencrypted files, you can setup a githook for your repository.
See an [example pre-commit](pre-commit) file here.

## Use As A Python Module

```python
import os
from pyenv_enc import enc

# User ID for GPG
USERID = os.environ.get("USER")

# Check if a encryption key-pair exists for the userid,
# or, create a new one.
enc.check_gpg_pubkey(USERID)

# Encrypt a value
text = "hello world"
encrypted = enc.gpg_encrypt(USERID, text)
print(encrypted)

# Decrypt a value
decrypted = enc.gpg_decrypt(encrypted)
print(decrypted)

# Recursively encrypt the string fields of a dictionary.
# This is useful to encrypt JSON, YAML, TOML files.
mydict = {
    "key1": 1234,
    "key2": "hello world",
    "key3": ["hello", "world"],
    "key4": {"foo": "bar"}
}
encrypted_dict = enc.encrypt_data(USERID, mydict)
print(encrypted_dict)

# Decrypt the dictionary.
print(enc.decrypt_data(encrypted_dict))
```

## About
LICENSE MIT Copyright 2023 Akhlak Mahmood
