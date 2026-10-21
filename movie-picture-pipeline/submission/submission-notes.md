# Movie Picture Pipeline Submission Notes

## Implemented Workflows

- `frontend-ci.yaml` implements the `Frontend Continuous Integration` workflow for pull requests to `main` and manual runs. It runs frontend lint and tests in parallel, then builds the Docker image only after both checks pass.
- `backend-ci.yaml` implements the `Backend Continuous Integration` workflow for pull requests to `main` and manual runs. It runs backend lint and tests in parallel, then builds the Docker image only after both checks pass.
- `frontend-cd.yaml` implements the `Frontend Continuous Deployment` workflow for pushes to `main` and manual runs. It runs lint, tests, Docker build with `REACT_APP_MOVIE_API_URL`, ECR login, ECR push, and EKS deployment with `kustomize` and `kubectl`.
- `backend-cd.yaml` implements the `Backend Continuous Deployment` workflow for pushes to `main` and manual runs. It runs lint, tests, Docker build, ECR login, ECR push, and EKS deployment with `kustomize` and `kubectl`.

## Required Secrets

The CD workflows read AWS and deployment configuration from GitHub Secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` for temporary Udacity credentials
- `AWS_REGION`
- `EKS_CLUSTER_NAME`
- `BACKEND_ECR_REPOSITORY`
- `FRONTEND_ECR_REPOSITORY`
- `REACT_APP_MOVIE_API_URL`

No AWS credentials are committed to the repository. For the May 23, 2026 resubmission, `REACT_APP_MOVIE_API_URL` was configured to the live backend LoadBalancer root URL, so the React app calls the backend service instead of `localhost`.

## Working Application Evidence

Direct EKS service URL evidence is included in `submission/eks-service-urls.md`. The latest successful CD workflows print the Kubernetes LoadBalancer records and the resulting service URLs after deployment:

- Backend service URL: http://a18afe5b90bb24585b4860dffc07ae59-672671680.us-east-1.elb.amazonaws.com/movies
- Frontend service URL: http://adb861f7c07204d42886b22f0c9a88bd-1344898137.us-east-1.elb.amazonaws.com

Fresh screenshots for the working URLs are included in `submission/screenshots/`:

- `backend-api-movies.png` shows the backend `/movies` endpoint returning the list of movies in a real browser window.
- `frontend-movie-list.png` shows the frontend rendering the movie list returned by the backend in a real browser window.
- `github-actions-workflows.png` shows the successful Frontend Continuous Deployment workflow run.

## GitHub Actions Verification

The latest successful GitHub Actions runs at resubmission time are:

- Frontend CI, triggered by pull request: https://github.com/LeoLin990405/movie-picture-pipeline/actions/runs/26163899024
- Backend CI, triggered by pull request: https://github.com/LeoLin990405/movie-picture-pipeline/actions/runs/26163899039
- Backend CD, manually rerun after provisioning fresh Udacity AWS infrastructure and configuring secrets: https://github.com/LeoLin990405/movie-picture-pipeline/actions/runs/26329390352
- Frontend CD, manually rerun after configuring `REACT_APP_MOVIE_API_URL` to the backend LoadBalancer: https://github.com/LeoLin990405/movie-picture-pipeline/actions/runs/26329482307

Pull request used to prove the required `pull_request` CI trigger:
https://github.com/LeoLin990405/movie-picture-pipeline/pull/1

The CD workflows require the deployment secrets and do not include an offline deployment fallback. If AWS/ECR/EKS secrets are missing or expired, the workflow fails in the `Verify deployment configuration` or AWS authentication steps. With valid secrets configured, the jobs authenticate to AWS, log in to ECR, push the built image to ECR, update the EKS kubeconfig, and run `kustomize build . | kubectl apply -f -` against the configured EKS cluster. The successful CD runs above both executed that real AWS/ECR/EKS path, waited for the deployment to become available, ran `kubectl get service`, and printed the service URL from the assigned LoadBalancer hostname. No mock or offline deployment step is used.
