#! /bin/bash

if [ -z $1 ]
then
    echo "Error: Missing argument, example usage: ./scripts/display_ggcanary_credentials.sh c1"
else
    set -e
    user_data=$(terraform state pull | jq ".outputs.ggcanary_access_keys.value[] | select(.name==\"$1\")")
    key_id=$(echo $user_data | jq -r .access_key_id)
    key_secret=$(echo $user_data | jq -r .access_key_secret)
    echo -e "\nGitGuardian Canary Token for $1:\naws_access_key_id = $key_id\naws_secret_access_key = $key_secret"
fi
