# Deploy Static Website on AWS

This repository contains the completed starter website and deployment automation for Udacity's **Deploy Static Website on AWS** project.

The project hosts a static website on Amazon S3 and distributes it through Amazon CloudFront.

## Architecture

- **Amazon S3** stores the static assets: `index.html`, CSS, images, JavaScript, fonts, and vendor files.
- **S3 static website hosting** serves the site through the S3 website endpoint.
- **Bucket policy** allows public read access to the website objects, matching the project rubric.
- **Amazon CloudFront** caches and distributes the website globally with HTTPS viewer access.

## Repository Contents

```text
.
├── index.html
├── css/
├── img/
├── vendor/
├── infra/cloudformation.yaml
├── scripts/deploy.sh
├── scripts/sync-site.sh
├── scripts/generate-evidence-screenshots.py
└── submission/submission-template.md
```

## Deploy

Prerequisites:

- AWS CLI installed and configured with valid credentials.
- Permission to create S3 buckets, S3 bucket policies, CloudFront distributions, and CloudFormation stacks.
- A globally unique S3 bucket name.

Deploy the infrastructure and upload the website:

```bash
export AWS_REGION=us-east-1
export BUCKET_NAME=<globally-unique-bucket-name>
./scripts/deploy.sh "$BUCKET_NAME"
```

The script prints the S3 website endpoint and CloudFront endpoint after the CloudFormation stack finishes.

## Update Website Files

After changing website content, sync the site back to S3:

```bash
export AWS_REGION=us-east-1
./scripts/sync-site.sh "$BUCKET_NAME"
```

If CloudFront still shows old content, create an invalidation:

```bash
aws cloudfront create-invalidation \
  --distribution-id <distribution-id> \
  --paths "/*"
```

## Udacity Submission Checklist

Before submission, collect the following evidence:

- Screenshot showing all website files uploaded to the S3 bucket.
- Screenshot showing static website hosting enabled on the bucket.
- Screenshot showing the bucket policy/permissions that allow public read access.
- Screenshot showing the CloudFront distribution configured for the website.
- Screenshot or note showing the website loading from the CloudFront endpoint.
- The CloudFront endpoint URL.

Use `submission/submission-template.md` to record the final URLs and screenshot list.

The current resubmission package includes the reviewer-requested screenshots:

- `screenshots/s3-uploaded-files.png`
- `screenshots/s3-bucket-policy.png`
- `screenshots/s3-static-website-hosting.png`
- `screenshots/s3-bucket-visible.png`
- `screenshots/cloudfront-enabled.png`
- `screenshots/cloudfront-website.png`

The same files are mirrored under `submission/screenshots/` for reviewers who inspect the submission evidence folder.

## Current Local Status

The website source, deployment automation, and AWS deployment are complete.

- S3 website endpoint: <http://leolin-udacity-static-website-835207447818-20260516.s3-website-us-west-2.amazonaws.com>
- CloudFront endpoint: <https://d1i5pbmzhtp53l.cloudfront.net>
- CloudFormation stack: `udacity-static-website`
- AWS region: `us-west-2`

Deployment evidence is stored under `submission/`.
