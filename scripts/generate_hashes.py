#!/usr/bin/env python3

"""
This script will output a json document containing, for each ggcanary token, it's name and hash.
It only depends on the python standard library (python >= 3.7)


The output has the following the format:
```
[
  {
    "name": "canary_token: <token name>",
    "hash": <hash>
  },
  ...
]
```

"""

import argparse
import json
import subprocess
from base64 import b64encode
from hashlib import blake2b
from typing import Dict, Iterable, List


def hash_string(token: str, digest_size: int = 64) -> str:
    """Util function to hash a string and return a base64 encoded string"""
    return b64encode(blake2b(token.encode(), digest_size=digest_size).digest()).decode()


def hash_matches(match_values: Iterable[str]) -> str:
    """
    Return a 48 characters string that uniquely identifies matches.
    """

    sep = "<gg>"
    return hash_string(
        sep.join(sorted(value for value in match_values)), digest_size=36
    )


def iter_secret(content: dict) -> List[Dict[str, str]]:
    return [
        {
            "hash": hash_matches((token["access_key_id"], token["access_key_secret"])),
            "name": f"ggcanary_token: {token['name']}",
        }
        for token in content["outputs"]["ggcanary_access_keys"]["value"]
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generates hashes of the ggcanary tokens, and output them in json format."
    )
    parser.add_argument("--pretty", action="store_true", help="Display indented json.")

    args = parser.parse_args()
    indent = 2 if args.pretty else None

    process = subprocess.run(
        ["terraform", "state", "pull"],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    content = json.loads(process.stdout)
    result = iter_secret(content)
    print(json.dumps(result, indent=indent))


if __name__ == "__main__":
    main()
