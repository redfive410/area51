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
