#! /bin/bash

if [ -z $1 ]
then
    echo "Error: Missing argument, example usage: ./scripts/ggcanary_call.sh c1"
else
    echo -e "\nPerforming ggcanary call for USER: $1"
    set -e
    user_data=$(terraform state pull | jq ".outputs.ggcanary_access_keys.value[] | select(.name==\"$1\")")
    if [ "$user_data" = "" ]
    then
        echo -e "Error: User $1 not found"
        exit 1
    else
        set +e
        key_id=$(echo $user_data | jq -r .access_key_id)
        key_secret=$(echo $user_data | jq -r .access_key_secret)
        aws_response=$(AWS_ACCESS_KEY_ID=$key_id AWS_SECRET_ACCESS_KEY=$key_secret AWS_DEFAULT_REGION=us-west-2 aws s3 ls 2>&1)
        # expect "An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied"
        if [[ "$aws_response" == *AccessDenied* ]]
        then
            echo -e "Call performed at $(date)"
        else
            echo -e "Unexpected response : $aws_response"
            exit 1
        fi
    fi
fi
