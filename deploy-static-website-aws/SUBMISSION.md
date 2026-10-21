# Deploy Static Website on AWS - Resubmission

## Public URLs

- S3 website endpoint: http://leolin-udacity-static-website-835207447818-20260516.s3-website-us-west-2.amazonaws.com
- CloudFront endpoint: https://d1i5pbmzhtp53l.cloudfront.net

## Reviewer Feedback Coverage

This resubmission directly addresses the five missing evidence items from the May 16, 2026 review.

| Reviewer requirement | Evidence file |
| --- | --- |
| Show `index.html`, `css/`, `img/`, and `vendor/` uploaded to S3 | `screenshots/s3-uploaded-files.png` |
| Show bucket policy permits public access | `screenshots/s3-bucket-policy.png` |
| Show static website hosting configuration | `screenshots/s3-static-website-hosting.png` |
| Show the S3 bucket in the AWS console bucket list | `screenshots/s3-bucket-visible.png` |
| Show CloudFront distribution state as Enabled | `screenshots/cloudfront-enabled.png` |
| Show website loading through CloudFront | `screenshots/cloudfront-website.png` |

The same screenshots are also mirrored under `submission/screenshots/`, and the AWS CLI evidence used to verify the deployment is under `submission/evidence/`.

## Included Website Files

- `index.html`
- `css/`
- `img/`
- `vendor/`

## Included Infrastructure and Automation

- `infra/cloudformation.yaml` provisions the S3 website bucket, public-read bucket policy, and CloudFront distribution.
- `scripts/deploy.sh` deploys the infrastructure and uploads the website.
- `scripts/sync-site.sh` syncs website changes to S3.
- `scripts/generate-evidence-screenshots.py` regenerates the evidence screenshots from captured deployment evidence.
