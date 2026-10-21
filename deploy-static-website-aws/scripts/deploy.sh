#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="${STACK_NAME:-udacity-static-website}"
AWS_REGION="${AWS_REGION:-us-east-1}"
BUCKET_NAME="${1:-${BUCKET_NAME:-}}"

if [[ -z "${BUCKET_NAME}" ]]; then
  echo "Usage: BUCKET_NAME=<globally-unique-name> $0"
  echo "   or: $0 <globally-unique-bucket-name>"
  exit 1
fi

aws cloudformation deploy \
  --stack-name "${STACK_NAME}" \
  --template-file infra/cloudformation.yaml \
  --parameter-overrides BucketName="${BUCKET_NAME}" \
  --region "${AWS_REGION}"

aws s3 sync . "s3://${BUCKET_NAME}" \
  --exclude ".git/*" \
  --exclude ".gitignore" \
  --exclude "infra/*" \
  --exclude "scripts/*" \
  --exclude "submission/*" \
  --exclude "README.md" \
  --exclude "README.txt" \
  --exclude "*.zip" \
  --exclude ".DS_Store" \
  --delete \
  --region "${AWS_REGION}"

echo
echo "Deployment outputs:"
aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --region "${AWS_REGION}" \
  --query "Stacks[0].Outputs[*].[OutputKey,OutputValue]" \
  --output table
