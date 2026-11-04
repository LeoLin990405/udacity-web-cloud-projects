# Project reference

Detailed notes for the twelve course projects in this repository. The README keeps the module
table and the common commands; this file records what each project contains, what actually runs,
where its submission evidence lives, and what is missing.

Nothing here was executed while writing this reference. Build, test and deployment instructions are
transcribed from each project's own README, manifests and scripts.

## Inventory

| Path | Udacity course / module | Language / toolchain | Runs locally | Tests | License file |
|---|---|---|---|---|---|
| [`portfolio-site/`](../portfolio-site/README.md) | Portfolio Site project | HTML, SCSS, Sass CLI | yes, static | none | none |
| [`personal-portfolio-dom/`](../personal-portfolio-dom/README.md) | Personal Portfolio (DOM + fetch) | HTML, CSS, vanilla JS | yes, static | none | Udacity educational |
| [`business-landing-website/`](../business-landing-website/README.md) | Business landing page | HTML, CSS | yes, static | none | none |
| [`deploy-static-website-aws/`](../deploy-static-website-aws/README.md) | Deploy Static Website on AWS | S3, CloudFront, CloudFormation | deploys to AWS | none | none |
| [`udacity-nd9991-static-website/`](../udacity-nd9991-static-website/README.md) | nd9991 Cloud DevOps, Cloud Foundations project | S3, CloudFront, AWS CLI, bash | deploys to AWS | none | none |
| [`ha-webapp-cloudformation/`](../ha-webapp-cloudformation/README.md) | High-availability web app with CloudFormation | VPC, ALB, Auto Scaling, EC2, S3, IAM | deploys to AWS | template validation commands only | none |
| [`location-reminder-app/`](../location-reminder-app/README.md) | Android Kotlin Location Reminder | Kotlin, Gradle, Room, Koin, Firebase, Maps | needs Android SDK + Firebase | unit + instrumented | none |
| [`preparing-for-production/`](../preparing-for-production/README.md) | Study Night: Preparing for Production | JS, Parcel, Gulp, ESLint, Mocha, Cypress | yes | unit + Cypress e2e | Udacity educational |
| [`coworking-space-microservice/`](../coworking-space-microservice/README.md) | cd12355 Coworking Space Service | Flask, PostgreSQL, Docker, CodeBuild, ECR, EKS | needs AWS + cluster | none | Udacity educational |
| [`movie-picture-pipeline/`](../movie-picture-pipeline/README.md) | CI/CD for a React + Flask app | React, Flask, Docker, Actions, ECR, EKS, Terraform | app locally, CD needs AWS | pytest + Jest | Udacity educational |
| [`nd303-meme/`](../nd303-meme/README.md) | nd303 Intermediate Python, Course 3 capstone | Python, Pillow, python-docx, pandas, Flask, Xpdf | yes | unittest | none (attribution in README) |
| [`nd0044-fyyur/`](../nd0044-fyyur/README.md) | nd0044 Backend Developer with Python, Course 2 | Flask, SQLAlchemy, PostgreSQL, Flask-Migrate | yes, needs PostgreSQL | none | Udacity educational |

## Static front-end projects

### portfolio-site

A single-page portfolio built with semantic HTML and SCSS partials using BEM class names.
`src/scss/base/` holds resets, `src/scss/blocks/` the components, `src/scss/utils/` variables and
mixins. `dist/main.css` is committed and is what the page loads.

```sh
cd portfolio-site
npm install
npm run build     # sass src/scss/main.scss dist/main.css
npm run watch     # rebuild on change
```

### personal-portfolio-dom

The course supplied the HTML, CSS and JSON; `js/scripts.js` is the student implementation. It
fetches `data/aboutMeData.json` and `data/projectsData.json`, renders the about section, builds
project cards, swaps the spotlight on card click, scrolls the card strip with the navigation
arrows (using `matchMedia` to switch axis), and validates the contact form client-side with a
300-character message limit and placeholder images for missing data.

There is no build step: open `index.html` in a browser, or serve the directory (for example
`python3 -m http.server`) because `fetch` does not work from `file://` in most browsers.

### business-landing-website

A two-page static site for a fictional workspace-design studio: `index.html` (hero, repeated
cards, captioned image) and `contact/contact.html` (labelled form fields). Styles are split into
`global.css`, `home.css` and `contact.css`; layout uses Flexbox, CSS Grid and responsive media
queries. No JavaScript, no build step.

## AWS deployment projects

`deploy-static-website-aws` and `udacity-nd9991-static-website` reach the same end state by
different routes: a public-read S3 bucket with static website hosting, fronted by CloudFront.
The first provisions the bucket, policy and distribution with `infra/cloudformation.yaml`; the
second drives the AWS CLI from `deploy.sh` and keeps its resource identifiers in `.deploy-state`
so `teardown.sh` can remove them.

```sh
# deploy-static-website-aws
cd deploy-static-website-aws
export AWS_REGION=us-east-1
export BUCKET_NAME=<globally-unique-bucket-name>
./scripts/deploy.sh "$BUCKET_NAME"
./scripts/sync-site.sh "$BUCKET_NAME"     # after content changes
```

```sh
# udacity-nd9991-static-website
cd udacity-nd9991-static-website
./deploy.sh            # prompts for a bucket name, or BUCKET=my-name ./deploy.sh
./teardown.sh          # deletes distribution, empties and deletes the bucket
```

`ha-webapp-cloudformation` builds a two-stack VPC + application deployment: two public subnets
with an internet-facing ALB and two NAT gateways, two private subnets with EC2 web servers, an
Auto Scaling group of four `t3.medium` instances (defaults in `templates/servers.yml`), a private
S3 bucket, and an IAM instance profile with read access to that bucket. EC2 UserData downloads
`app/index.htm` from the bucket and serves it with NGINX.

```sh
cd ha-webapp-cloudformation
export AWS_REGION=us-west-2
./scripts/deploy-all.sh      # network stack, then server stack
./scripts/destroy-all.sh     # reverse dependency order
```

All three projects keep their submission material in `submission/` (screenshots plus CLI JSON
evidence) and mirror screenshots into a top-level `screenshots/` directory. The public URLs
printed in those files were captured during the Udacity review window and are not kept alive.

## Container and CI/CD projects

### coworking-space-microservice

A Flask analytics API (`analytics/app.py`) with `/health_check`, `/readiness_check`,
`/api/reports/daily_usage` and `/api/reports/user_visits`, backed by PostgreSQL. The image is
built from `analytics/Dockerfile`; `buildspec.yml` is the CodeBuild specification that pushes
`coworking-analytics:1.0.0` and `:latest` to ECR; `deployment/` holds the Kubernetes manifests
(PostgreSQL StatefulSet and ClusterIP Service, ConfigMap, Secret, application Deployment and
LoadBalancer Service on port 5153). `deployment-local/` holds local-cluster variants of the
ConfigMap and application manifests.

```sh
./scripts/deploy-codebuild.sh   # ECR repository, IAM role, CodeBuild project, webhook
./scripts/wait-codebuild.sh
./scripts/deploy-k8s.sh         # apply PostgreSQL, then the application
./scripts/seed-db.sh            # load db/1_create_tables.sql and the seed files
```

The manifests commit a demo database password in clear text (`deployment/secrets.yaml`); it has
to be replaced before the manifests are used anywhere but a throwaway cluster. `kubernetes.md`
documents the deployment sequence and the CloudWatch Container Insights expectation.

### movie-picture-pipeline

A React front end and a Flask back end deployed to EKS by four GitHub Actions workflows:

| Workflow | Trigger | Jobs |
|---|---|---|
| `frontend-ci.yaml` | pull request to `main` touching `starter/frontend/**`, or manual | lint + test in parallel, then Docker build |
| `backend-ci.yaml` | pull request to `main` touching `starter/backend/**`, or manual | lint + test in parallel, then Docker build |
| `frontend-cd.yaml` | push to `main` touching `starter/frontend/**`, or manual | lint, test, build, ECR push, `kustomize` + `kubectl` deploy |
| `backend-cd.yaml` | push to `main` touching `starter/backend/**`, or manual | lint, test, build, ECR push, `kustomize` + `kubectl` deploy |

The CD workflows read eight GitHub secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`AWS_SESSION_TOKEN`, `AWS_REGION`, `EKS_CLUSTER_NAME`, `BACKEND_ECR_REPOSITORY`,
`FRONTEND_ECR_REPOSITORY`, `REACT_APP_MOVIE_API_URL`) and have no offline fallback: without them
the run fails at the configuration or AWS authentication step. `setup/terraform/` provisions the
cluster and the IAM user for Actions; `setup/init.sh` adds that user to the cluster's
authentication configuration.

```sh
cd movie-picture-pipeline/starter/backend
pipenv install
pipenv run test        # 3 pytest tests
pipenv run lint
pipenv run serve       # http://localhost:5000/movies

cd ../frontend
nvm use
npm ci
CI=true npm test       # 2 suites, 3 tests
npm run lint
```

`submission/submission-notes.md` and `submission/eks-service-urls.md` record the resubmission
evidence, including the Actions run URLs and the LoadBalancer hostnames observed at that time.

## Applications and coursework

### location-reminder-app

A Kotlin Android app (`com.udacity.project4`) that stores reminders with Room, shows them with a
RecyclerView, and registers geofences that trigger notifications. Architecture pieces: Koin for
dependency injection, Navigation with Safe Args, ViewModel/LiveData/Coroutines, FirebaseUI for
email and Google sign-in, Google Maps for picking a point of interest.

Build configuration: Gradle 8.4.1, Kotlin 1.9.23, `minSdk 24`, `targetSdk 33`, `compileSdk 34`.
The project README asks for Android Studio Jellyfish or newer and JDK 21; the CI workflow runs
`./gradlew testDebugUnitTest` on Java 17.

To run the app you need your own Firebase project with Email/Password and Google sign-in enabled,
plus a Maps SDK for Android key restricted to the app's package name and signing fingerprint.
Unit tests live in `app/src/test`, instrumented tests in `app/src/androidTest`; the app README's
"Break Down Tests" section is still the starter template text.

```sh
cd location-reminder-app
./gradlew testDebugUnitTest      # what .github/workflows/android.yml runs
./gradlew assembleDebug          # requires the Android SDK
```

### preparing-for-production

The Study Night flashcard app prepared for a production review: Parcel 2 build, Gulp 5 task
pipeline, ESLint 9 and Prettier, Mocha/Chai unit tests for the shuffle utility, Cypress end-to-end
specs for navigation and the create-set / add-card forms, and a committed `dist/` build.

```sh
cd preparing-for-production
npm install
npm run lint
npm run test          # mocha "test/**/*.js"
npm run gulp          # lint, unit tests, parcel build
npm run serve         # http://127.0.0.1:1234
npm run cypress:run   # starts the server, then runs Cypress
```

### nd303-meme

The nd303 capstone: a quote engine that parses TXT, DOCX, CSV and PDF files (PDF through the
Xpdf `pdftotext` binary via `subprocess`), an image engine that resizes to a maximum width of
500 px and draws the quote, a CLI (`src/meme.py` with optional `--body`, `--author`, `--path`) and
a Flask service (`src/app.py` with `/` and `/create`). Quote parsing dispatches on file extension
through an abstract `IngestorInterface`; `MemeEngine` normalizes JPEG and PNG inputs to RGB.

```sh
cd nd303-meme
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
brew install xpdf                 # macOS; apt-get install xpdf on Debian/Ubuntu
cd src
python3 meme.py --body "Such wow" --author "Xander"
python3 app.py                    # http://127.0.0.1:5000
```

The starter code, sample data, `demo.gif` and templates come from Udacity's
[PYND/02_meme_gen_starter](https://github.com/udacity/PYND/tree/master/02_meme_gen_starter); the
quote engine, meme engine and integration work are the student implementation, as stated in the
project README.

### nd0044-fyyur

The Fyyur artist/venue booking site, completed: `models.py` defines `Venue`, `Artist` and `Show`
with unique constraints and cascading relationships, `migrations/versions/` contains the schema
migration, and `app.py` implements the venue, artist and show routes plus search. Database
configuration is read from `DATABASE_URL` and falls back to a local `fyyur` database for the
current OS user.

```sh
cd nd0044-fyyur
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
createdb fyyur                    # PostgreSQL must be running
flask db upgrade
python3 app.py                    # http://127.0.0.1:5000
```

The project README keeps the original Udacity brief, rubric and troubleshooting notes; its setup
section still points at the upstream `udacity/FSND` starter repository.
