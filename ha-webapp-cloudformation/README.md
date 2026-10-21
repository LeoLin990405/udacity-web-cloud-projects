# Deploy a High-Availability Web App Using CloudFormation

This repository contains the completed Udacity Cloud DevOps project for deploying a highly available web application with AWS CloudFormation.

## Architecture

The solution creates:

- One VPC across two availability zones.
- Two public subnets for the internet-facing Application Load Balancer and NAT Gateways.
- Two private subnets for EC2 web servers.
- Two NAT Gateways so private instances can install packages while remaining unreachable from the public internet.
- An Application Load Balancer with a public HTTP listener.
- An Auto Scaling group with four EC2 instances.
- A launch template using a 2 vCPU / 4 GiB instance type and a 10 GB root volume.
- Security groups that allow public HTTP only to the load balancer and allow web traffic to EC2 only from the load balancer.
- A private S3 bucket for application artifacts.
- An IAM instance profile with least-privilege read access to the application S3 bucket, matching the project requirement that the servers have S3 access.

See `diagrams/architecture.mmd` for the architecture diagram source.

## Files

```text
templates/network.yml              VPC, subnets, route tables, internet gateway, NAT gateways
templates/servers.yml              IAM, launch template, ASG, ALB, listener, target group
parameters/network-parameters.json Network stack parameters
parameters/servers-parameters.json Server stack parameters
scripts/create.sh                  Generic stack creation helper
scripts/update.sh                  Generic stack update helper
scripts/delete.sh                  Generic stack deletion helper
scripts/deploy-all.sh              Deploys both stacks in order
scripts/destroy-all.sh             Deletes both stacks in dependency order
app/index.htm                      Sample app uploaded to S3 and downloaded by NGINX user data
submission/                        Deployment evidence and screenshots
```

The UserData script downloads `index.htm` from the private S3 application bucket and serves that file through NGINX. The deployment script uploads `app/index.htm` to the bucket and refreshes the Auto Scaling group so the EC2 instances serve the S3-hosted artifact instead of hardcoded CloudFormation HTML.

## Deploy

```bash
export AWS_REGION=us-west-2
./scripts/deploy-all.sh
```

Or deploy stack-by-stack:

```bash
./scripts/create.sh udagram-network templates/network.yml parameters/network-parameters.json
./scripts/create.sh udagram-servers templates/servers.yml parameters/servers-parameters.json
```

## Update

```bash
./scripts/update.sh udagram-network templates/network.yml parameters/network-parameters.json
./scripts/update.sh udagram-servers templates/servers.yml parameters/servers-parameters.json
```

## Delete

```bash
./scripts/destroy-all.sh
```

## Validation

Before deployment, both templates were validated with:

```bash
aws cloudformation validate-template --template-body file://templates/network.yml --region us-west-2
aws cloudformation validate-template --template-body file://templates/servers.yml --region us-west-2
```

## Deployment Result

The stacks should be deployed in `us-west-2`.

- Network stack: `udagram-network`
- Server stack: `udagram-servers`
- Load balancer URL: <http://udagra-Appli-L9Ppaf8Chf5n-677445926.us-west-2.elb.amazonaws.com>

The reviewer should be able to open the Load Balancer URL and see `It works! Udagram, Udacity`. If the stack is deleted before review, include screenshots for both stack outputs with deployment timestamps, successful access to the Load Balancer URL, and the S3 bucket containing `index.htm`.
