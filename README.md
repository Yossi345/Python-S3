This Python script use boto3 to work with s3 buckets and files
the script does the following steps:

1. Creates 1 bucket using client connection and a second bucket using resource connection.
2. Creates files and uploading them to the buckets.
3. Downloads files from the buckets.
4. Copies an Object Between Buckets.
5. Deletes an Object from the bucket.
6. Changes the files access permissions from private to public and vice versa.
7. Uploads a file and encrypt it using ServerSideEncryption.
8. Upload a file and set its storage class.
9. Tests how doed bucket versioning works with files.
10. Lists our bucket names and their content.
11. Deleting Buckets and Objects.