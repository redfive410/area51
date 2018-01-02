# area51

### simple secrets management
```
KMS_ALIAS=<KMS_ALIAS>
S3_BUCKET=<S3_BUCKET>

echo $KMS_ALIAS
echo $S3_BUCKET

aws kms encrypt --key-id $KMS_ALIAS --plaintext file://secrets.txt --output text --query CiphertextBlob | base64 --decode > secrets.bin
aws s3 cp secrets.bin s3://$S3_BUCKET/secrets.bin

aws s3 cp s3://$S3_BUCKET/secrets.bin secrets.s3.bin
aws kms decrypt --ciphertext-blob fileb://secrets.s3.bin --output text --query Plaintext | base64 --decode

```

### simple envelope encryption
```
aws kms generate-data-key --key-id alias/2701 --key-spec AES_256 --output json
echo 'aYwzrJ7LxVe2aZnaTxXYER7LTo9waIYNliRC0ba/JrQ=' | base64 --decode > ~/tmp/plaintext_key_decoded.txt
echo "Top Secret!!" | openssl enc -e -aes256 -k fileb://home/jarmitage/tmp/plaintext_key_decoded.txt > ~/tmp/encrypted.txt
rm ~/tmp/plaintext_key_decoded.txt

echo 'AQIDAHheC4xf/RrS2zIOZjUE4sOzl0UH2kzg/aqbzFGd89eaVAGQLHe9pC94A983Hl3El9lLAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMBSlMOHtyiNTUX7rTAgEQgDt9eE5mv9K2UfCSz5rrvMom9YLbi8G+tQIC1/qYM7WJZ8ukNGTZ9dHo8DGJhJaNmELd2p+QI8h/LTj9XQ==' | base64 --decode > ~/tmp/ciphertext_blob_decoded.txt
aws kms decrypt --ciphertext-blob fileb:///home/jarmitage/tmp/ciphertext_blob_decoded.txt --output json
echo 'aYwzrJ7LxVe2aZnaTxXYER7LTo9waIYNliRC0ba/JrQ=' |base64 --decode > ~/tmp/plaintext_key_decoded.txt
cat ~/tmp/encrypted.txt |openssl enc -d -aes256 -k fileb://home/jarmitage/tmp/plaintext_key_decoded.txt

```

### aws encryption sdk python
```
pip install --user aws-encryption-sdk
```

#### encryption example
```
import aws_encryption_sdk

kms_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(key_ids=[
    'arn:aws:kms:us-west-2:0000000000000:key/00000000-0000-0000-0000-000000000000'
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
```

### aws boto3 python
```
pip install --user boto3
```

#### envelope encryption example
```
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
        'account_number': '0000000000000',
        'key_id': '00000000-0000-0000-0000-000000000000',
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
```
