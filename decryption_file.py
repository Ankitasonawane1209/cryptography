from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def decrypt_file_aes(input_file_path, aes_key, output_file_path):
    with open(input_file_path, 'rb') as infile:
        iv = infile.read(AES.block_size)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)

        ciphertext = infile.read()
        decrypted_data = cipher.decrypt(ciphertext)
        decrypted_data = unpad(decrypted_data, AES.block_size)

    with open(output_file_path, 'wb') as outfile:
        outfile.write(decrypted_data)


def decrypt_aes_key_with_rsa(aes_key_enc_path, private_key_path):
    with open(private_key_path, 'rb') as prv_file:
        private_key = RSA.import_key(prv_file.read())

    with open(aes_key_enc_path, 'rb') as file:
        encrypted_aes_key = file.read()

    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    return aes_key
