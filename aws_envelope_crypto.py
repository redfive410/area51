#!/usr/bin/env python
import base64
import boto3

from Crypto.Cipher import AES

pad = lambda s: s + (32 - len(s) % 32) * ' '

def encrypt_data(aws_data, plaintext_message):
    kms = boto3.client('kms')

    data_key = kms.generate_data_key(KeyId=aws_data['key_id'], KeySpec='AES_256')
    ciphertext_blob = data_key.get('CiphertextBlob')
    plaintext_key = data_key.get('Plaintext')

    # Note, does not use IV or specify mode... for demo purposes only.
    crypter = AES.new(plaintext_key)
    encrypted_data = base64.b64encode(crypter.encrypt(pad(plaintext_message)))

    # Need to preserve both of these data elements
    return encrypted_data, ciphertext_blob

def decrypt_data(aws_data, encrypted_data, ciphertext_blob):
    kms = boto3.client('kms')

    decrypted_key = kms.decrypt(CiphertextBlob=ciphertext_blob).get('Plaintext')
    crypter = AES.new(decrypted_key)

    return crypter.decrypt(base64.b64decode(encrypted_data)).rstrip()


def main():
    # Add your account number / region / KMS Key ID here.
    aws_data = {
        'region': 'us-west-2',
        'account_number': '1096135268162',
        'key_id': 'd1a77a82-9846-4a55-a49c-d618cb546b84',
    }

    # And your super sekret message to envelope encrypt...
    plaintext = 'Hello, World!'

    # Store encrypted_data & ciphertext_blob in your persistent storage. You will need them both later.
    encrypted_data, ciphertext_blob = encrypt_data(aws_data, plaintext)
    print encrypted_data

    # Later on when you need to decrypt, get these from your persistent storage.
    decrypted_data = decrypt_data(aws_data, encrypted_data, ciphertext_blob)
    print decrypted_data

if __name__ == '__main__':
    main()
