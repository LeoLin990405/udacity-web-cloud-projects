#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <stack-name> <template-file> <parameters-file>"
  exit 1
fi

STACK_NAME="$1"
TEMPLATE_FILE="$2"
PARAMETERS_FILE="$3"
AWS_REGION="${AWS_REGION:-us-west-2}"

aws cloudformation create-stack \
  --stack-name "$STACK_NAME" \
  --template-body "file://$TEMPLATE_FILE" \
  --parameters "file://$PARAMETERS_FILE" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region "$AWS_REGION"

aws cloudformation wait stack-create-complete \
  --stack-name "$STACK_NAME" \
  --region "$AWS_REGION"

aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs" \
  --output table \
  --region "$AWS_REGION"
