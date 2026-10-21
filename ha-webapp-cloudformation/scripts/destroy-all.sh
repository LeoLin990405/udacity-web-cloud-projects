#!/usr/bin/env bash
set -euo pipefail

export AWS_REGION="${AWS_REGION:-us-west-2}"

./scripts/delete.sh udagram-servers
./scripts/delete.sh udagram-network
