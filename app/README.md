# Introduction
This README provides an overview for the deployment flow for the project generated from https://github.com/d-lab/mephisto template.

# Prerequisites
Before deploying, you must set the following variables/secrets in your Github Actions environment:

- DOTNETRC (Heroku .netrc file content with "" wrapped)
- HEROKU_API_KEY (Heroku API key)
- MTURK_ACCESS_KEY_ID (Mturk access key)
- MTURK_SECRET_ACCESS_KEY (Mturk secret key)
- PRIVATE_KEY (Private key for ssh access)

You also need to install the following tools:
- Docker (Desktop)

# Configuration

- The practical deployment flow: local -> test -> prod
  - branch `deployment-test` for test/staging env
  - branch `deployment-prod` for production env 

- Refer to https://mephisto.ai/docs/guides/tutorials/first_task/ for other configuration details

`Please ensure that you have changed the taskname in hydra_config in example_sb.yml and example_production.yml. 
Note that Heroku app names for each cannot be duplicated and cannot exceed 30 characters ().`

# How to start
1. Create a new repo from d-lab/mephisto template with the option "Include all branches"
2. Clone the new repo to your local machine
3. Switch to the `deployment-test` branch


# Local Deployment
1. Start from the `deployment-test` branch
2. cd to `app` directory
3. Run `docker-compose up` to start the local server
4. Run `docker exec -it mephisto-service sh -c "cd webapp && npm run dev:watch"` to
build the frontend
5. Start implementing your task in webapp/src

# Test Deployment
1. Once you are ready to test your task, you can deploy it to the test environment by 
pushing to the `deployment-test` branch.
2. Make sure to config the hydra_config in example_sb.yml and environment variables in github actions
3. Check github actions log for the deployment status and the sandbox path to access the task

# Production Deployment
1. Make sure to config the hydra_config in example_production.yml and environment variables in github actions
2. Merge your changes from `deployment-test` to `deployment-prod` branch
3. Check github actions log for the deployment status and the production path to access the task