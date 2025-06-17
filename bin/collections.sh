#!/bin/bash

HOST="http://localhost:8000"
COLLECTION=$1
LIMIT="${3:-3}"

curl -s -X GET "$HOST/collections" \
  -H "Accept: application/json" \
  | jq .

