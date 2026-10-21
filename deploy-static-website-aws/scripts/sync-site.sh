#!/usr/bin/env bash
set -euo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
BUCKET_NAME="${1:-${BUCKET_NAME:-}}"

if [[ -z "${BUCKET_NAME}" ]]; then
  echo "Usage: BUCKET_NAME=<bucket-name> $0"
  echo "   or: $0 <bucket-name>"
  exit 1
fi

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
