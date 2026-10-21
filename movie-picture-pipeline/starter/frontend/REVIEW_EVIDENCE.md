# Frontend Review Evidence

This file intentionally lives inside `starter/frontend/` so that a pull request
touching it exercises the frontend CI path filter. The frontend workflows lint,
test, build the Docker image, and run the deployment job for manifest validation
when AWS/EKS training credentials are not configured.
