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
To use, clone this repo and install with `pip`.
```sh
git clone git+https://github.com/akhlakm/pyenv-encrypt.git
cd pyenv-encrypt
pip install -e .
```

Alternatively, use the following for packaging (for example, in your `requirements.txt` file).
```sh
pip install git+https://github.com/akhlakm/pyenv-encrypt.git
```

### Dependencies
The `gpg` utility must be installed in your system. GPG comes built-in with most versions of Linux OS. For Mac, use homebrew: `brew install gpg`.

See the official [installation instructions](https://gnupg.org/download/) for more info. Run the following the verify GPG is installed.

```sh
gpg --version
```

The following python packages are installed to support reading files.
- python-dotenv
- pyyaml


## Commandline Usage
Use the `pyenc` utility to encrypt or decrypt your config/env files direct from the terminal.

```sh
pyenc .env
```

Multiple files can also be encrypted.
```sh
pyenc .env vault.yaml data.json
```

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
# This is useful to encrypt the JSON, YAML, TOML files.
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
