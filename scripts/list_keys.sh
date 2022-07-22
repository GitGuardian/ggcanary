#! /usr/bin/env bash

terraform state pull | jq .outputs.ggcanary_access_keys.value