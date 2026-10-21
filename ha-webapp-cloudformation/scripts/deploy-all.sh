#!/usr/bin/env bash
set -euo pipefail

export AWS_REGION="${AWS_REGION:-us-west-2}"

deploy_or_update() {
  local stack_name="$1"
  local template_file="$2"
  local parameters_file="$3"

  if aws cloudformation describe-stacks --stack-name "$stack_name" --region "$AWS_REGION" >/dev/null 2>&1; then
    ./scripts/update.sh "$stack_name" "$template_file" "$parameters_file"
  else
    ./scripts/create.sh "$stack_name" "$template_file" "$parameters_file"
  fi
}

deploy_or_update udagram-network templates/network.yml parameters/network-parameters.json
deploy_or_update udagram-servers templates/servers.yml parameters/servers-parameters.json

BUCKET_NAME="$(aws cloudformation describe-stacks \
  --stack-name udagram-servers \
  --region "$AWS_REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='WebAppBucketName'].OutputValue" \
  --output text)"

aws s3 cp app/index.htm "s3://${BUCKET_NAME}/index.htm" --region "$AWS_REGION"

AUTO_SCALING_GROUP="$(aws cloudformation describe-stacks \
  --stack-name udagram-servers \
  --region "$AWS_REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='AutoScalingGroupName'].OutputValue" \
  --output text)"

aws autoscaling start-instance-refresh \
  --auto-scaling-group-name "$AUTO_SCALING_GROUP" \
  --region "$AWS_REGION" \
  --preferences MinHealthyPercentage=50,InstanceWarmup=120 >/dev/null

aws cloudformation describe-stacks \
  --stack-name udagram-servers \
  --region "$AWS_REGION" \
  --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNSName'].OutputValue" \
  --output text
