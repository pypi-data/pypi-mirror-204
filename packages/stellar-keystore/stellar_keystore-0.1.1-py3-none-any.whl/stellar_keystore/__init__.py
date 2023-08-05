import base64
import secrets

import nacl.secret
from nacl.hashlib import scrypt
from stellar_sdk import Keypair

__all__ = ["create_keystore", "load_keystore"]

__version__ = "0.1.1"

VERSION = "stellarport-1-20-2018"
NONCE_SIZE = nacl.secret.SecretBox.NONCE_SIZE
SALT_SIZE = 32
DK_LEN = nacl.secret.SecretBox.KEY_SIZE
SCRYPT_N = 16384
SCRYPT_R = 8
SCRYPT_P = 1
ENCODING_FORMAT = "binary"


def create_keystore(keypair: Keypair, password: bytes) -> dict:
    """Create a keystore from a keypair.

    :param keypair: The keypair to create a keystore from.
    :param password: The password to encrypt the keystore with.
    :return: The keystore.
    """
    if not keypair.can_sign():
        raise ValueError("The keypair does not have a secret key.")

    nonce = secrets.token_bytes(NONCE_SIZE)
    salt = secrets.token_bytes(SALT_SIZE)

    key = scrypt(
        password=password,
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=DK_LEN,
    )
    secret_box = nacl.secret.SecretBox(key)
    # In my opinion, it may be better to use keypair.raw_secret_key() as data.
    encrypted_data = bytes(secret_box.encrypt(keypair.secret.encode(), nonce=nonce))
    if not encrypted_data.startswith(nonce):
        raise ValueError("Encryption failed, nonce mismatch.")

    encrypted_data = encrypted_data[len(nonce):]
    return {
        "version": VERSION,
        "address": keypair.public_key,
        "crypto": {
            "ciphertext": base64.b64encode(encrypted_data),
            "nonce": base64.b64encode(nonce),
            "salt": base64.b64encode(salt),
            "scryptOptions": {
                "N": SCRYPT_N,
                "r": SCRYPT_R,
                "p": SCRYPT_P,
                "dkLen": DK_LEN,
                "encoding": ENCODING_FORMAT,
            },
        },
    }


def load_keystore(keystore: dict, password: bytes) -> Keypair:
    """Load a keypair from a keystore.

    :param keystore: The keystore to load a keypair from.
    :param password: The password to decrypt the keystore with.
    :return: The keypair.
    """
    if keystore.get("version") != VERSION:
        raise NotImplementedError("Unsupported keystore version.")

    encrypted_data = base64.b64decode(keystore["crypto"]["ciphertext"])
    nonce = base64.b64decode(keystore["crypto"]["nonce"])
    salt = base64.b64decode(keystore["crypto"]["salt"])
    scrypt_options = keystore["crypto"]["scryptOptions"]
    n = scrypt_options["N"]
    r = scrypt_options["r"]
    p = scrypt_options["p"]
    dklen = scrypt_options["dkLen"]
    encoding = scrypt_options["encoding"]
    if encoding != ENCODING_FORMAT:
        raise NotImplementedError("Unsupported encoding format.")

    key = scrypt(
        password=password,
        salt=salt,
        n=n,
        r=r,
        p=p,
        dklen=dklen,
    )
    secret_box = nacl.secret.SecretBox(key)
    decrypted_data = secret_box.decrypt(encrypted_data, nonce=nonce)
    kp = Keypair.from_secret(decrypted_data.decode())

    address = keystore.get("address")
    if kp.public_key != address:
        raise ValueError(f"Invalid address: {address}")
    return kp
