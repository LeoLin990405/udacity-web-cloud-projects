# Udacity Submission Notes

## Website URLs

- S3 website endpoint: http://leolin-udacity-static-website-835207447818-20260516.s3-website-us-west-2.amazonaws.com
- CloudFront endpoint: https://d1i5pbmzhtp53l.cloudfront.net

## Required Screenshots

Screenshots are included in `submission/screenshots/`.

1. `s3-uploaded-files.png` shows uploaded website files, including `index.html`, `css/`, `img/`, and `vendor/`.
2. `s3-bucket-policy.png` shows the public-read bucket policy.
3. `s3-static-website-hosting.png` shows static website hosting enabled.
4. `s3-bucket-visible.png` shows the S3 bucket in the bucket list.
5. `cloudfront-enabled.png` shows the CloudFront distribution deployed and enabled.
6. `cloudfront-website.png` shows the website loading through the CloudFront endpoint.

## Submitted Evidence

- `submission/screenshots/cloudfront-website.png` shows the deployed website loaded through CloudFront.
- `submission/screenshots/s3-uploaded-files.png` shows all required website files uploaded to S3.
- `submission/screenshots/s3-bucket-policy.png` shows the bucket policy permitting public access.
- `submission/screenshots/s3-static-website-hosting.png` shows static website hosting configuration.
- `submission/screenshots/s3-bucket-visible.png` shows the S3 bucket in the AWS bucket list.
- `submission/screenshots/cloudfront-enabled.png` shows the enabled CloudFront distribution.
- `submission/evidence/s3-uploaded-files.json` shows objects uploaded to the S3 bucket.
- `submission/evidence/s3-website-configuration.json` shows static website hosting configuration.
- `submission/evidence/s3-bucket-policy.json` shows the public read bucket policy.
- `submission/evidence/cloudformation-resources.json` shows the S3 bucket, bucket policy, and CloudFront distribution resources.
- `submission/evidence/cloudformation-outputs.json` records the final S3 and CloudFront endpoints.
- `submission/evidence/cloudfront-distribution.json` shows the CloudFront distribution domain, origin, and deployed status.

## Deployment Commands

```bash
export AWS_REGION=us-east-1
export BUCKET_NAME=<globally-unique-bucket-name>
./scripts/deploy.sh "$BUCKET_NAME"
```
