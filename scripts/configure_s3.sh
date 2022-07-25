#! /bin/bash

# This script creates the S3 bucket and dynamodb table holding the terraform state.

s3_backend=$(cat "./backend.tf.json"| jq .terraform.backend.s3)

if [ "$s3_backend" = "null" ]
  then
    echo "No S3 backend found. Exiting..."
    exit 1
  else
    profile=$(echo $s3_backend | jq -r .profile)
    bucket_name=$(echo $s3_backend | jq -r .bucket)
    region=$(echo $s3_backend | jq -r .region)

    # Create bucket
    aws s3api create-bucket --bucket $bucket_name --region $region --create-bucket-configuration LocationConstraint=$region --profile $profile
    # Add encryption to bucket
    aws s3api put-bucket-encryption --bucket $bucket_name --server-side-encryption-configuration "{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\": \"AES256\"}}]}" --profile $profile
    # Create DynamoDB for lock
    aws dynamodb create-table --table-name ggcanary-terraform-backend --region $region --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --profile $profile
fi