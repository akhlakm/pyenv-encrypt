# PyEnv-Encrypt
GPG based env file encryptor utility.

## Commandline Usage
Use the `pyenc` utility to encrypt or decrypt your config/env files.
```sh
pyenc .env
```

## Use As A Python Module

```python
import os
from pyenc_enc import enc

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
    "key2": "hello world"
    "key3": ["hello", "world"],
    "key4": {"foo": "bar"}
}
encrypted_dict = enc.encrypt_data(USERID, mydict)
print(encrypted_dict)

# Decrypt the dictionary.
print(enc.decrypt_data(encrypted_dict))

```

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

LICENSE GPLv3.0+
