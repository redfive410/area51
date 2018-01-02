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
[aws_crypto.py](aws_crypto.py)
```
python aws_crypto.py
```

### aws boto3 python
```
pip install --user boto3
pip install --user pycrypto
```

#### envelope encryption example
[aws_envelope_crypto.py](aws_envelope_crypto.py)
```
python aws_envelope_crypto.py
```

### TODO
1. pycrypto does not support AES.MODE_GCM; investigate pycryptodome
    * https://github.com/wolf43/AES-GCM-example/blob/master/aes_gcm.py
    * http://pycryptodome.readthedocs.io/en/latest/src/introduction.html

### REFS
1. https://gist.github.com/Spaider/8fd0c97fd4785011032bc8144d00b8cc
2. https://boto3.readthedocs.io/en/latest/reference/services/kms.html#client
3. https://www.dlitz.net/software/pycrypto/
