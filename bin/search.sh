#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <collection> <search query> [results limit (default: 3)]"
  exit 1
fi

HOST="http://localhost:8000"
COLLECTION=$1
QUERY=$2
LIMIT="${3:-3}"

curl -s -G "$HOST/search/$COLLECTION" \
  --data-urlencode "q=$QUERY" \
  --data-urlencode "limit=$LIMIT" \
  -H "Accept: application/json" \
  | jq .

