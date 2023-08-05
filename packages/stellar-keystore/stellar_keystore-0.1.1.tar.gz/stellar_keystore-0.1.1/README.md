# Stellar Keystore

This is a helper library for creating stellar keystore wallets. 

Due to the lack of relevant [SEPs](https://github.com/stellar/stellar-protocol/tree/master/ecosystem) currently, [stellarport/stellar-keystore](https://github.com/stellarport/stellar-keystore) is the most widely applied implementation, so the implementation of this library is consistent with it.

## What is a keystore wallet?
A keystore wallet is a data blob that stores an encrypted secret key. The objective of a keystore wallet is to allow a user who does not want to remember/manage a secret key
and would instead rather manage a password, to store and securely encrypt their secret key using their desired password.

## What does this library offer?
This library offers methods that will allow your application to create stellar keystore wallets (i.e. keystore wallets containing secret keys controlling stellar public keys)
as well as retrieve a stellar keypair given a keystore wallet/password combination.

## Installation
```bash
pip install stellar-keystore
```

## Usage
```python
from stellar_sdk import Keypair
from stellar_keystore import *

# Create a new keystore wallet
keypair = Keypair.random()
keystore_wallet = create_keystore(keypair, b"password")

# Retrieve the keypair from the keystore wallet
keypair = load_keystore(keystore_wallet, b"password")
```

## API
```python
def create_keystore(keypair: Keypair, password: bytes) -> dict:
    """Create a keystore from a keypair.

    :param keypair: The keypair to create a keystore from.
    :param password: The password to encrypt the keystore with.
    :return: The keystore.
    """
    pass
```

```python
def load_keystore(keystore: dict, password: bytes) -> Keypair:
    """Load a keypair from a keystore.

    :param keystore: The keystore to load a keypair from.
    :param password: The password to decrypt the keystore with.
    :return: The keypair.
    """
    pass
```