#!/usr/bin/env bash
#
# Udacity nd9991 - Deploy Static Website on AWS
# End-to-end deployment: S3 + Bucket Policy + Static Website Hosting + CloudFront
#
# Prerequisites:
#   - AWS CLI v2 installed (`aws --version`)
#   - AWS credentials configured (`aws configure` or env vars)
#
# Usage:
#   ./deploy.sh                  # interactive, prompts for bucket name
#   BUCKET=my-name ./deploy.sh   # non-interactive
#
# State is persisted to .deploy-state so teardown.sh knows what to delete.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- Sanity checks --------------------------------------------------------

if ! command -v aws >/dev/null 2>&1; then
  echo "ERROR: aws CLI not found. Install with: brew install awscli" >&2
  exit 1
fi

if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo "ERROR: AWS credentials not configured." >&2
  echo "Run: aws configure" >&2
  echo "Or set: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION" >&2
  exit 1
fi

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
REGION="${AWS_DEFAULT_REGION:-$(aws configure get region || echo us-east-1)}"

# --- Bucket name ----------------------------------------------------------

if [[ -z "${BUCKET:-}" ]]; then
  DEFAULT_BUCKET="leo-${ACCOUNT_ID}-nd9991-site"
  read -p "S3 bucket name [${DEFAULT_BUCKET}]: " INPUT_BUCKET
  BUCKET="${INPUT_BUCKET:-$DEFAULT_BUCKET}"
fi

echo
echo "==> Deploying with:"
echo "    Account:  $ACCOUNT_ID"
echo "    Region:   $REGION"
echo "    Bucket:   $BUCKET"
echo

# --- 1. Create S3 bucket --------------------------------------------------

echo "==> [1/6] Creating S3 bucket..."
if aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  echo "    Bucket already exists, reusing."
else
  if [[ "$REGION" == "us-east-1" ]]; then
    aws s3api create-bucket --bucket "$BUCKET"
  else
    aws s3api create-bucket --bucket "$BUCKET" \
      --create-bucket-configuration "LocationConstraint=$REGION"
  fi
  echo "    Bucket created."
fi

# --- 2. Disable Block Public Access --------------------------------------

echo "==> [2/6] Disabling Block Public Access (required for static hosting)..."
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
echo "    Done."

# --- 3. Upload website files ---------------------------------------------

echo "==> [3/6] Uploading website files..."
aws s3 sync "$SCRIPT_DIR/website/" "s3://$BUCKET/" \
  --exclude ".DS_Store" --exclude "__MACOSX/*" \
  --delete
FILE_COUNT="$(aws s3 ls "s3://$BUCKET/" --recursive | wc -l | tr -d ' ')"
echo "    Uploaded ($FILE_COUNT files)."

# --- 4. Attach public-read Bucket Policy ---------------------------------

echo "==> [4/6] Attaching public-read Bucket Policy..."
POLICY=$(cat <<JSON
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AddPerm",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::${BUCKET}/*"]
    }
  ]
}
JSON
)
aws s3api put-bucket-policy --bucket "$BUCKET" --policy "$POLICY"
echo "    Done."

# --- 5. Enable Static Website Hosting -------------------------------------

echo "==> [5/6] Enabling Static Website Hosting..."
aws s3 website "s3://$BUCKET/" --index-document index.html --error-document index.html
WEBSITE_ENDPOINT="http://${BUCKET}.s3-website-${REGION}.amazonaws.com"
# us-east-1 uses "s3-website-" but other regions use "s3-website." - normalize:
if [[ "$REGION" != "us-east-1" ]]; then
  WEBSITE_ENDPOINT="http://${BUCKET}.s3-website.${REGION}.amazonaws.com"
fi
echo "    Website endpoint: $WEBSITE_ENDPOINT"

# --- 6. Create CloudFront distribution ------------------------------------

echo "==> [6/6] Creating CloudFront distribution..."

# Origin must be the WEBSITE endpoint, not the REST endpoint.
# Strip the http:// prefix for CloudFront origin domain name.
ORIGIN_DOMAIN="${WEBSITE_ENDPOINT#http://}"

CALLER_REF="nd9991-$(date +%s)"
DIST_CONFIG=$(cat <<JSON
{
  "CallerReference": "${CALLER_REF}",
  "Comment": "Udacity nd9991 - Deploy Static Website on AWS",
  "Enabled": true,
  "DefaultRootObject": "index.html",
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "s3-website-origin",
        "DomainName": "${ORIGIN_DOMAIN}",
        "CustomOriginConfig": {
          "HTTPPort": 80,
          "HTTPSPort": 443,
          "OriginProtocolPolicy": "http-only",
          "OriginSslProtocols": {
            "Quantity": 1,
            "Items": ["TLSv1.2"]
          },
          "OriginReadTimeout": 30,
          "OriginKeepaliveTimeout": 5
        }
      }
    ]
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "s3-website-origin",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"],
      "CachedMethods": {
        "Quantity": 2,
        "Items": ["GET", "HEAD"]
      }
    },
    "Compress": true,
    "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6"
  },
  "PriceClass": "PriceClass_All",
  "ViewerCertificate": {
    "CloudFrontDefaultCertificate": true
  }
}
JSON
)

CF_OUTPUT="$(aws cloudfront create-distribution --distribution-config "$DIST_CONFIG")"
DIST_ID="$(echo "$CF_OUTPUT" | python3 -c 'import json,sys;print(json.load(sys.stdin)["Distribution"]["Id"])')"
CF_DOMAIN="$(echo "$CF_OUTPUT" | python3 -c 'import json,sys;print(json.load(sys.stdin)["Distribution"]["DomainName"])')"
echo "    Distribution ID:    $DIST_ID"
echo "    CloudFront domain:  https://${CF_DOMAIN}"

# --- Persist state for teardown ------------------------------------------

cat > "$SCRIPT_DIR/.deploy-state" <<STATE
BUCKET=${BUCKET}
REGION=${REGION}
ACCOUNT_ID=${ACCOUNT_ID}
WEBSITE_ENDPOINT=${WEBSITE_ENDPOINT}
DIST_ID=${DIST_ID}
CF_DOMAIN=${CF_DOMAIN}
DEPLOYED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
STATE

# --- Summary --------------------------------------------------------------

cat <<EOF

============================================================
DEPLOYMENT COMPLETE
============================================================

Bucket:              $BUCKET
Region:              $REGION
S3 Website URL:      $WEBSITE_ENDPOINT
CloudFront URL:      https://${CF_DOMAIN}
Distribution ID:     $DIST_ID

NOTE: CloudFront takes 5-15 minutes to fully deploy.
      Status will go from "InProgress" to "Deployed".

Check deployment status:
    aws cloudfront get-distribution --id $DIST_ID --query 'Distribution.Status' --output text

Once Deployed, verify all three URLs:
    curl -sI $WEBSITE_ENDPOINT/ | head -1
    curl -sI https://${CF_DOMAIN}/ | head -1
    curl -sI https://${BUCKET}.s3.${REGION}.amazonaws.com/index.html | head -1

State saved to: .deploy-state
EOF
