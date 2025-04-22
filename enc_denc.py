from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Fixed 256-bit key (32 bytes) for AES encryption (In real-world, use dynamic key management)
KEY = bytes.fromhex('603deb1015ca71be2b73aef0857d7781f353f1f0e5e8e3f3f2e1b501aeff6f1f')

def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()

    iv = os.urandom(12)  # GCM IV
    cipher = Cipher(algorithms.AES(KEY), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag

    with open(file_path, 'wb') as file:
        file.write(iv + tag + encrypted_data)

    print(f"File encrypted successfully: {file_path}")

def decrypt_file(file_path):
    with open(file_path, 'rb') as enc_file:
        iv = enc_file.read(12)
        tag = enc_file.read(16)
        encrypted_data = enc_file.read()

    cipher = Cipher(algorithms.AES(KEY), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return

    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

    print(f"File decrypted successfully: {file_path}")
