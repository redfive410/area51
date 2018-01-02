import aws_encryption_sdk

kms_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(key_ids=[
    'arn:aws:kms:us-west-2:109613526816:key/d1a77a82-9846-4a55-a49c-d618cb546b84'
])
my_plaintext = 'This is some super secret data!  Yup, sure is!'

my_ciphertext, encryptor_header = aws_encryption_sdk.encrypt(
    source=my_plaintext,
    key_provider=kms_key_provider
)

decrypted_plaintext, decryptor_header = aws_encryption_sdk.decrypt(
    source=my_ciphertext,
    key_provider=kms_key_provider
)
print(my_plaintext)
print(decrypted_plaintext)

assert my_plaintext == decrypted_plaintext
assert encryptor_header.encryption_context == decryptor_header.encryption_context
