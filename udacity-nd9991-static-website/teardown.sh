#!/usr/bin/env bash
#
# Udacity nd9991 - Teardown
# Deletes the CloudFront distribution and S3 bucket created by deploy.sh.
# Reads state from .deploy-state.
#
# IMPORTANT: Run this only AFTER your project review passes,
# to stop accruing AWS charges.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f .deploy-state ]]; then
  echo "ERROR: .deploy-state not found. Did deploy.sh run successfully?" >&2
  exit 1
fi

# shellcheck disable=SC1091
source .deploy-state

echo "About to delete:"
echo "  CloudFront distribution: $DIST_ID ($CF_DOMAIN)"
echo "  S3 bucket:               $BUCKET"
echo
read -p "Type 'yes' to confirm: " CONFIRM
[[ "$CONFIRM" == "yes" ]] || { echo "Aborted."; exit 1; }

# --- 1. Disable CloudFront distribution (required before delete) ---------

echo "==> Fetching distribution config..."
ETAG="$(aws cloudfront get-distribution-config --id "$DIST_ID" --query 'ETag' --output text)"
aws cloudfront get-distribution-config --id "$DIST_ID" --query 'DistributionConfig' > /tmp/dist-config.json

echo "==> Disabling distribution..."
python3 -c "
import json
with open('/tmp/dist-config.json') as f:
    cfg = json.load(f)
cfg['Enabled'] = False
with open('/tmp/dist-config.json', 'w') as f:
    json.dump(cfg, f)
"

aws cloudfront update-distribution --id "$DIST_ID" --if-match "$ETAG" \
  --distribution-config file:///tmp/dist-config.json > /dev/null

echo "==> Waiting for distribution to fully disable (this can take 5-15 min)..."
aws cloudfront wait distribution-deployed --id "$DIST_ID"

# --- 2. Delete CloudFront distribution -----------------------------------

ETAG="$(aws cloudfront get-distribution --id "$DIST_ID" --query 'ETag' --output text)"
echo "==> Deleting distribution..."
aws cloudfront delete-distribution --id "$DIST_ID" --if-match "$ETAG"
echo "    Deleted."

# --- 3. Empty + delete S3 bucket -----------------------------------------

echo "==> Emptying bucket..."
aws s3 rm "s3://$BUCKET/" --recursive

echo "==> Deleting bucket..."
aws s3api delete-bucket --bucket "$BUCKET"
echo "    Deleted."

rm -f /tmp/dist-config.json
mv .deploy-state ".deploy-state.deleted.$(date +%s)"

echo
echo "Teardown complete. All AWS resources removed."
