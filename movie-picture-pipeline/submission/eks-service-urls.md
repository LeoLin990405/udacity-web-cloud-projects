# EKS Service URL Evidence

This resubmission includes fresh deployment evidence from the successful May 23, 2026 GitHub Actions CD runs. The reviewer feedback requested live, reachable EKS LoadBalancer URLs and browser screenshots that show the ELB hostnames in the address bar, so the evidence below replaces the earlier `example.local` screenshots and expired service URLs.

## Successful CD Runs

- Backend CD run: https://github.com/LeoLin990405/movie-picture-pipeline/actions/runs/26329390352
- Frontend CD run: https://github.com/LeoLin990405/movie-picture-pipeline/actions/runs/26329482307

## Live Service URLs

- Backend API: http://a18afe5b90bb24585b4860dffc07ae59-672671680.us-east-1.elb.amazonaws.com/movies
- Frontend app: http://adb861f7c07204d42886b22f0c9a88bd-1344898137.us-east-1.elb.amazonaws.com

## Runtime Verification

The backend service returned the expected movie payload from the live EKS LoadBalancer:

```json
{"movies":[{"id":"123","title":"Top Gun: Maverick"},{"id":"456","title":"Sonic the Hedgehog"},{"id":"789","title":"A Quiet Place"}]}
```

The frontend service rendered the React Movie List application from the live EKS LoadBalancer and loaded the movies from the backend URL configured in `REACT_APP_MOVIE_API_URL`.

## Browser Screenshots

The screenshots in `submission/screenshots/` were captured from a real local browser window after the successful CD runs:

- `backend-api-movies.png` shows the backend `/movies` endpoint with the ELB hostname in the browser address bar and JSON movie output in the page.
- `frontend-movie-list.png` shows the frontend ELB hostname in the browser address bar and the rendered Movie List with `Top Gun: Maverick`, `Sonic the Hedgehog`, and `A Quiet Place`.
- `github-actions-workflows.png` shows the successful Frontend Continuous Deployment run, including the EKS deploy job.

GitHub Actions masks configured secret values in workflow logs, so the raw workflow logs replace `us-east-1`, `backend`, and `frontend` with `***`. The service hostnames in this note are the unmasked live AWS LoadBalancer hostnames verified after deployment.

Full downloaded workflow logs are included in:

- `submission/evidence/backend-cd-run-26329390352.log`
- `submission/evidence/frontend-cd-run-26329482307.log`
