#! /bin/bash

if [ -z $1 ]
then
    echo "Error: Missing argument, example usage: ./scripts/ggcanry_call.sh c1"
else
    echo -e "\nPerforming ggcanary call for USER: $1"
    set -e
    user_data=$(terraform state pull | jq ".outputs.ggcanary_access_keys.value[] | select(.name==\"$1\")")
    key_id=$(echo $user_data | jq -r .access_key_id)
    key_secret=$(echo $user_data | jq -r .access_key_secret)
    if [ "$user_data" = "" ]
    then
        echo -e "Error: User $1 not found"
        exit 1
    else
        AWS_ACCESS_KEY_ID=$key_id AWS_SECRET_ACCESS_KEY=$key_secret AWS_DEFAULT_REGION=us-west-2 aws s3 ls
    fi
fi
