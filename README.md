# Deploy Static Website on AWS

Udacity Nanodegree **Cloud DevOps Engineer (nd9991)** — final project of the *Cloud Foundations* course.

Deploys a static blog site to AWS using **S3** for object storage, an **IAM bucket policy** for public read access, **S3 Static Website Hosting** as the origin, and **CloudFront** as the global CDN.

## Architecture

```
              ┌──────────────────────────┐
              │   Viewer (browser)       │
              └─────────────┬────────────┘
                            │ HTTPS
                            ▼
              ┌──────────────────────────┐
              │   CloudFront Distribution │
              │   (global edge cache)    │
              └─────────────┬────────────┘
                            │ HTTP (origin pull)
                            ▼
              ┌──────────────────────────┐
              │   S3 Static Website      │
              │   Endpoint               │
              │   (HTTP, index/error doc) │
              └─────────────┬────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │   S3 Bucket              │
              │   (public-read policy)   │
              │   - index.html           │
              │   - css/, img/, vendor/  │
              └──────────────────────────┘
```

Why CloudFront fronts the **S3 website endpoint** (not the bucket directly): the website endpoint resolves `/` → `index.html` and applies error-document semantics, which the plain S3 REST endpoint does not.

## Repository layout

```
.
├── deploy.sh             # End-to-end AWS deploy (S3 + policy + hosting + CloudFront)
├── teardown.sh           # Delete distribution + empty + delete bucket
├── website/              # Static site uploaded to S3
│   ├── index.html
│   ├── css/
│   ├── img/
│   └── vendor/
├── submission/           # Materials submitted to Udacity reviewers
│   ├── README.txt        # Live URLs + resource IDs (template to fill in)
│   └── screenshots/      # 8 console screenshots (added manually)
└── STARTER-README.txt    # Original starter-code README (kept for reference)
```

## Prerequisites

- macOS / Linux with bash 4+
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (`brew install awscli`)
- An AWS account with permissions for: `s3:*`, `cloudfront:*`
- `python3` (used for parsing JSON outputs in scripts)

## Deploy

```bash
# 1. Configure AWS credentials (one-time)
aws configure
# AWS Access Key ID:     <your key>
# AWS Secret Access Key: <your secret>
# Default region:        us-east-1
# Default output format: json

# 2. Run the deploy script
./deploy.sh
# Prompts for bucket name (default: leo-<account-id>-nd9991-site)
# Or set BUCKET=my-name ./deploy.sh
```

The script will:

1. Create the S3 bucket
2. Disable Block Public Access on the bucket
3. Upload `website/` contents
4. Attach a public-read bucket policy (`s3:GetObject` for `Principal: "*"`)
5. Enable static website hosting (`index.html` as index + error doc)
6. Create a CloudFront distribution with the S3 website endpoint as origin

State is persisted to `.deploy-state` so `teardown.sh` knows what to remove.

## Verify

CloudFront takes 5-15 minutes after `deploy.sh` finishes to fully deploy.

```bash
# Wait for Status = Deployed
source .deploy-state
aws cloudfront get-distribution --id "$DIST_ID" --query 'Distribution.Status' --output text

# Then test all three access paths
curl -sI "https://$CF_DOMAIN/" | head -1
curl -sI "$WEBSITE_ENDPOINT/" | head -1
curl -sI "https://$BUCKET.s3.$REGION.amazonaws.com/index.html" | head -1
# All three should return 200
```

## Submit (Udacity)

1. Verify all three URLs return 200
2. Capture 8 console screenshots into `submission/screenshots/` (filenames listed in `submission/README.txt`)
3. Fill in the placeholders in `submission/README.txt` with your actual URLs and IDs
4. Zip the `submission/` folder:
   ```bash
   cd submission && zip -r ../submission.zip . && cd ..
   ```
5. Upload `submission.zip` on the Udacity project page

## Teardown

After your project review passes (1-3 days), delete the AWS resources to stop accruing charges:

```bash
./teardown.sh
```

CloudFront distributions take 5-15 minutes to fully disable before they can be deleted, so this script will block on that wait.

## Rubric mapping

| Rubric criterion | Where it's satisfied |
|---|---|
| S3 bucket created and visible | `deploy.sh` step 1 — verify in S3 console |
| All website files uploaded | `deploy.sh` step 3 (`aws s3 sync website/`) |
| Bucket configured for static website hosting | `deploy.sh` step 5 (`aws s3 website ... --index-document index.html`) |
| Bucket policy makes contents publicly accessible | `deploy.sh` step 4 (public-read `s3:GetObject` policy) |
| CloudFront distributes the website | `deploy.sh` step 6 (creates distribution with website endpoint as custom origin) |
| Website accessible via browser | Verified via `curl` and screenshots #7-8 |

## Stand-out customization

The page title and H1 have been changed from "Travel Blog" to **"Leo's Travel Blog"** — see `website/index.html` lines 11 and 62.
