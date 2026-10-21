#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <stack-name>"
  exit 1
fi

AWS_REGION="${AWS_REGION:-us-west-2}"

aws cloudformation delete-stack \
  --stack-name "$1" \
  --region "$AWS_REGION"

aws cloudformation wait stack-delete-complete \
  --stack-name "$1" \
  --region "$AWS_REGION"
