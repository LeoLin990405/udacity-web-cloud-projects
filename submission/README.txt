Udacity Nanodegree: Cloud DevOps Engineer (nd9991)
Project: Deploy Static Website on AWS
Student: Leo Lin
GitHub: https://github.com/LeoLin990405/udacity-nd9991-static-website

==================================================================
LIVE URLS (replace placeholders after running deploy.sh)
==================================================================

CloudFront URL:
    https://<DISTRIBUTION_DOMAIN>.cloudfront.net/

S3 Website Endpoint:
    http://<BUCKET_NAME>.s3-website-<REGION>.amazonaws.com/

S3 Object URL (index.html):
    https://<BUCKET_NAME>.s3.<REGION>.amazonaws.com/index.html

==================================================================
RESOURCES CREATED
==================================================================

AWS Account ID:      <ACCOUNT_ID>
Region:              <REGION>
S3 Bucket Name:      <BUCKET_NAME>
CloudFront Dist ID:  <DISTRIBUTION_ID>

==================================================================
SCREENSHOTS (in this folder)
==================================================================

01-s3-bucket-created.png       S3 console showing the created bucket
02-s3-objects-uploaded.png     Bucket contents (index.html + css/img/vendor)
03-bucket-policy.png           IAM bucket policy allowing public read access
04-static-website-hosting.png  Static website hosting enabled + endpoint
05-cloudfront-deployed.png     CloudFront distribution status = Deployed
06-cloudfront-origin-config.png  Origin domain = S3 website endpoint
07-browser-cloudfront-url.png  Website rendering via CloudFront URL
08-browser-s3-website-endpoint.png  Website rendering via S3 endpoint

==================================================================
NOTES FOR REVIEWER
==================================================================

- The site is deployed via the "public S3 bucket + CloudFront in front"
  pattern described in the lesson (Route A). Block Public Access is
  intentionally disabled and a bucket policy grants s3:GetObject to "*".

- The CloudFront origin is the S3 *website* endpoint
  (<bucket>.s3-website-<region>.amazonaws.com), NOT the S3 REST endpoint.
  This is so that root paths and missing-key behavior follow web
  semantics (index document, error document).

- Default Root Object is set to index.html on the CloudFront distribution,
  so requests to https://<dist>.cloudfront.net/ resolve to index.html
  even without going through the website endpoint's automatic root
  resolution.

- Bonus customization: the page title and H1 have been changed from
  "Travel Blog" to "Leo's Travel Blog".

- Deployment is fully reproducible via deploy.sh in the repo root.
  Teardown via teardown.sh once the project is reviewed.

Thank you for reviewing!
