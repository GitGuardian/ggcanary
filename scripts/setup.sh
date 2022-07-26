#! /bin/bash


function check_prerequisite () {
    echo "Checking required dependencies..."
    echo
    declare -a commands_to_check=(jq terraform aws)
    declare -a not_found
    for command in "${commands_to_check[@]}"
    do
        command_path=$(which $command)
        if [[ $? == 0 ]]
        then
            printf "%-20sFound at %s\n" "$command" "$command_path"
        else
            printf "\e[91m%-20sNot Found !\e[0m\n" "$command"
            not_found+=($command)
        fi
    done
    echo
    return ${#not_found[@]}
}


function check_files() {
    echo "Checking files needed to deploy..."
    echo
    local res=0
    declare -a files_to_check=(terraform.tfvars)

    for file in "${files_to_check[@]}"
    do
        if [ -f $file ]
        then
            echo "File '$file' found."
        else
            echo "File '$file' has not been created."
            res=1
        fi
    done
    echo
    return $res
}

function check_backend_tf_changed() {
    echo  "Checking that the terraform backend has been configured..."
    grep CHANGEME backend.tf
    local return_value=$(expr 1 - $?)
    return $return_value
}


check_prerequisite
if [[ $? != 0 ]]
then
    echo "Some dependencies are missing, you have to install them before we can continue."
    exit 1
else
    echo "All dependencies found."
    echo
    echo "-----------------------------------------"
    echo
fi

check_files
if [[ $? != 0 ]]
then
    echo "Some required to the deployment are missing, you have to create them and fill them with appropriate values before we can continue."
    exit 1
else
    echo "All required files found."
    echo
    echo "-----------------------------------------"
    echo
fi

check_backend_tf_changed
if [[ $? != 0 ]]
then
    echo "Some values still need to be changed in backend.tf before we can continue."
    exit 1
else
    echo "backend.tf has been filled with appropriate values."
    echo
    echo "-----------------------------------------"
    echo
fi



echo
echo "Everything is set, you can now keep on with the installation steps."
