#! /usr/bin/env bash

profile=CHANGEME
bucket_name=CHANGEME
region=us-west-2

# Create bucket
aws s3api create-bucket --bucket $bucket_name --region $region --create-bucket-configuration LocationConstraint=$region --profile $profile
# Add encryption to bucket
aws s3api put-bucket-encryption --bucket $bucket_name --server-side-encryption-configuration "{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\": \"AES256\"}}]}" --profile $profile
# Create dynamodb for lock
aws dynamodb create-table --table-name ggcanary-terraform-backend --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --profile $profile