# Submission Notes

## Project

Deploy a high-availability web app using CloudFormation.

## Stack Names

- Network stack: `udagram-network`
- Server stack: `udagram-servers`

## URLs

- Load balancer URL: http://udagra-Appli-L9Ppaf8Chf5n-677445926.us-west-2.elb.amazonaws.com

## Evidence

- `submission/screenshots/load-balancer-website.png` shows the deployed application through the ALB.
- `submission/evidence/alb-http-headers.txt` shows HTTP 200 from the ALB.
- `submission/evidence/network-stack.json` records the deployed network stack.
- `submission/evidence/servers-stack.json` records the deployed server stack and ALB URL output.
- `submission/evidence/autoscaling-group.json` records ASG desired/min/max capacity and launched instances.
- `submission/evidence/target-health.json` records four healthy targets in the target group.
- `submission/evidence/s3-bucket-objects.json` records the S3 bucket object `index.htm`.
- `submission/evidence/alb-page.html` records the working page returned by the ALB.

## Reviewer Notes

- The server template now uses `AWS::EC2::LaunchTemplate`; `AWS::AutoScaling::LaunchConfiguration` has been removed.
- The server template creates a private S3 bucket and grants EC2 least-privilege read access to that bucket through the instance profile.
- The EC2 UserData downloads `index.htm` from the private S3 bucket and serves it through NGINX; HTML is no longer hardcoded in CloudFormation.
- `scripts/deploy-all.sh` uploads `app/index.htm` to the generated S3 bucket and starts an Auto Scaling instance refresh so the instances pull the S3-hosted file.
- The architecture diagram includes the S3 bucket, IAM role, ALB, Auto Scaling group, EC2 instances, public/private subnets, NAT gateways, and Internet Gateway.
