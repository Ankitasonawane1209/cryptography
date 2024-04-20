from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os


def generate_rsa_key_pair(private_key_path, public_key_path):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save the keys to their respective files
    with open(private_key_path, "wb") as prv_file:
        prv_file.write(private_key)
    with open(public_key_path, "wb") as pub_file:
        pub_file.write(public_key)


def encrypt_file_aes(input_file_path, aes_key, output_file_path):
    cipher = AES.new(aes_key, AES.MODE_CBC)  # CBC mode is used here
    with open(input_file_path, 'rb') as infile:
        plaintext_data = infile.read()

    ciphertext_data = cipher.encrypt(pad(plaintext_data, AES.block_size))

    with open(output_file_path, 'wb') as outfile:
        outfile.write(cipher.iv)  # Write the IV to the output file before the ciphertext
        outfile.write(ciphertext_data)


def encrypt_aes_key_with_rsa(aes_key, public_key_path, aes_key_enc_path):
    recipient_key = RSA.import_key(open(public_key_path).read())
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    with open(aes_key_enc_path, 'wb') as file:
        file.write(encrypted_aes_key)


def generate_aes_key():
    return get_random_bytes(32)


