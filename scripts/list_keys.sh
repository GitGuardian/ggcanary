#! /bin/bash

terraform state pull | jq .outputs.ggcanary_access_keys.value