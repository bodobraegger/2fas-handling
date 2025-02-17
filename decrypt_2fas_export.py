import json
import base64
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def main():
    backup = sys.argv[1]
    passphrase = sys.argv[2]

    with open(backup) as f:
        data = json.load(f)
    services_enc = data["servicesEncrypted"]
    credentials_enc, pbkdf2_salt, nonce = map(base64.b64decode, services_enc.split(":"))
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=pbkdf2_salt, iterations=10000)
    key = kdf.derive(passphrase.encode("utf8"))
    aesgcm = AESGCM(key)
    credentials_dec = aesgcm.decrypt(nonce, credentials_enc, None)
    credentials_dec = json.loads(credentials_dec)
    json.dump(credentials_dec, sys.stdout, indent=4)

if __name__ == "__main__":
    main()
