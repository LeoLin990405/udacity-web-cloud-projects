# Backend Review Evidence

This file intentionally lives inside `starter/backend/` so that a pull request
touching it exercises the backend CI path filter. The backend workflows lint,
test, build the Docker image, and run the deployment job for manifest validation
when AWS/EKS training credentials are not configured.
