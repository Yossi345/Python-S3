pip install boto3

import boto3

import uuid

s3_client = boto3.client('s3')

s3_resource = boto3.resource('s3')


def create_bucket_name(bucket_prefix):
    # Generate a unique bucket name 
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    # Create a bucket with a unique name using "create_bucket_name" function and your region
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def create_temp_file(size, file_name, file_content):
    # Create a file with a desired name and size,
    #  The function allow you to pass in the number of bytes you want the file to have,
    # the file name, and a sample content for the file to be repeated to make up the desired file size
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name

def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    # copy file from the first bucket to the second bucket, using .copy()
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)

 
def enable_bucket_versioning(bucket_name):
    # Enable versioning for the bucket using the BucketVersioning class
    bkt_versioning = s3_resource.BucketVersioning(bucket_name)
    bkt_versioning.enable()
    print(bkt_versioning.status)

def delete_all_objects(bucket_name):
    # delete all the bucket versions and all the objects in the bucket
    res = []
    bucket=s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({'Key': obj_version.object_key,
                    'VersionId': obj_version.id})
    print(res)
    bucket.delete_objects(Delete={'Objects': res})





# cerate a bucket using a client connection
try:
    first_bucket_name, first_response = create_bucket(
    bucket_prefix='firstpythonbucket', 
    s3_connection=s3_resource.meta.client)
except:
    print("can't create bucket")


# create a bucket using a resource connection
try:
    second_bucket_name, second_response = create_bucket(
    bucket_prefix='secondpythonbucket', s3_connection=s3_resource)
except:
    print("can't create bucket")


# create a file with a desired filename, size and content
try:
    first_file_name = create_temp_file(300, 'firstfile.txt', 'f')
except:
    print("failed to create the file")


# upload the first file to the first bucket
first_bucket = s3_resource.Bucket(name=first_bucket_name)
first_object = s3_resource.Object(
    bucket_name=first_bucket_name, key=first_file_name)
try:
    s3_resource.Object(first_bucket_name, first_file_name).upload_file(
    Filename=first_file_name)
except:
    print("Could not upload the file")


# Download a file from S3 to your desired local path
try:
    s3_resource.Object(first_bucket_name, first_file_name).download_file(
    f'/tmp/{first_file_name}') 
except:
    print("could not download the file")


# Copying an Object Between Buckets
try:
    copy_to_bucket(first_bucket_name, second_bucket_name, first_file_name)
except:
    print("Could not copy the file")


# Deleting and object from s3 bucket
try:
    s3_resource.Object(second_bucket_name, first_file_name).delete()
except:
    print("Could not delete file from bucket")


# upload a new file to the bucket and make it public
try:
    second_file_name = create_temp_file(400, 'secondfile.txt', 's')
    second_object = s3_resource.Object(first_bucket.name, second_file_name)
    second_object.upload_file(second_file_name, ExtraArgs={
                          'ACL': 'public-read'})
except:
    print("failed to create or upload the file")


# get the object's acl
second_object_acl = second_object.Acl()
second_object_acl.grants


# change the object's permissions to private
response = second_object_acl.put(ACL='private')
second_object_acl.grants


# Create an new file, upload it and encrypt the file using ServerSideEncryption
try:
    third_file_name = create_temp_file(300, 'thirdfile.txt', 't')
    third_object = s3_resource.Object(first_bucket_name, third_file_name)
    third_object.upload_file(third_file_name, ExtraArgs={
                         'ServerSideEncryption': 'AES256'})
except:
    print("failed to create or upload the file")
third_object.server_side_encryption


# reupload the third_object and set its storage class to Standard_IA:
try:
    third_object.upload_file(third_file_name, ExtraArgs={
                         'ServerSideEncryption': 'AES256', 
                         'StorageClass': 'STANDARD_IA'})
except:
    print("failed to upload the file or set it's class")
third_object.reload()
third_object.storage_class


# Enable versioning for the first bucket
enable_bucket_versioning(first_bucket_name)


# create two new versions for the first file Object
s3_resource.Object(first_bucket_name, first_file_name).upload_file(
   first_file_name)
s3_resource.Object(first_bucket_name, first_file_name).upload_file(
   third_file_name)

# reupload the second file, which will create a new version
s3_resource.Object(first_bucket_name, second_file_name).upload_file(
    second_file_name)
s3_resource.Object(first_bucket_name, first_file_name).version_id


# lists all of your bucket instances uding s3 resources
for bucket in s3_resource.buckets.all():
    print(bucket.name)


# lists all of your bucket instances uding s3 clent
for bucket_dict in s3_resource.meta.client.list_buckets().get('Buckets'):
    print(bucket_dict['Name'])


# list all the objects from a bucket
for obj in first_bucket.objects.all():
    print(obj.key)


# list all the objects including their attributes from a bucket
for obj in first_bucket.objects.all():
    subsrc = obj.Object()
    print(obj.key, obj.storage_class, obj.last_modified,
          subsrc.version_id, subsrc.metadata)
    

# calling "delete_all_objects" function to remove all the versioned objects
try:
    delete_all_objects(first_bucket_name)
except:
    print("Could not remove object from bucket")


# Upload a file to the second bucket which doesn't have versioning enabled
# and than call the function "delete_all_objects" to remove all the objects
try:
    s3_resource.Object(second_bucket_name, first_file_name).upload_file(
        first_file_name)
    delete_all_objects(second_bucket_name)
except:
    print("failed to upload or delete the object")


# delete the empty first bucket using resource connection
s3_resource.Bucket(first_bucket_name).delete()


# delete the empty second bucket using client connection
s3_resource.meta.client.delete_bucket(Bucket=second_bucket_name)
