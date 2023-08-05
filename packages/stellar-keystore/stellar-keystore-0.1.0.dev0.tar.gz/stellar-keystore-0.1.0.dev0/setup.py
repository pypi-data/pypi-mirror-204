# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stellar_keystore']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0', 'stellar-sdk>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'stellar-keystore',
    'version': '0.1.0.dev0',
    'description': 'Tools for handling the encrypted keystore format used to store Stellar keypairs.',
    'long_description': '# Stellar Keystore\n\nThis is a helper library for creating stellar keystore wallets. \n\nDue to the lack of relevant [SEPs](https://github.com/stellar/stellar-protocol/tree/master/ecosystem) currently, [stellarport/stellar-keystore](https://github.com/stellarport/stellar-keystore) is the most widely applied implementation, so the implementation of this library is consistent with it.\n\n## What is a keystore wallet?\nA keystore wallet is a data blob that stores an encrypted secret key. The objective of a keystore wallet is to allow a user who does not want to remember/manage a secret key\nand would instead rather manage a password, to store and securely encrypt their secret key using their desired password.\n\n## What does this library offer?\nThis library offers methods that will allow your application to create stellar keystore wallets (i.e. keystore wallets containing secret keys controlling stellar public keys)\nas well as retrieve a stellar keypair given a keystore wallet/password combination.\n\n## Installation\n```bash\npip install stellar-keystore\n```\n\n## Usage\n```python\nfrom stellar_sdk import Keypair\nfrom stellar_keystore import *\n\n# Create a new keystore wallet\nkeypair = Keypair.random()\nkeystore_wallet = create_keystore(keypair, b"password")\n\n# Retrieve the keypair from the keystore wallet\nkeypair = load_keystore(keystore_wallet, b"password")\n```\n\n## API\n```python\ndef create_keystore(keypair: Keypair, password: bytes) -> dict:\n    """Create a keystore from a keypair.\n\n    :param keypair: The keypair to create a keystore from.\n    :param password: The password to encrypt the keystore with.\n    :return: The keystore.\n    """\n    pass\n```\n\n```python\ndef load_keystore(keystore: dict, password: bytes) -> Keypair:\n    """Load a keypair from a keystore.\n\n    :param keystore: The keystore to load a keypair from.\n    :param password: The password to decrypt the keystore with.\n    :return: The keypair.\n    """\n    pass\n```',
    'author': 'overcat',
    'author_email': '4catcode@gmail.com',
    'maintainer': 'overcat',
    'maintainer_email': '4catcode@gmail.com',
    'url': 'https://github.com/overcat/stellar-keystore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
