# Deployment

To deploy to production server:

1. Clone the repository master branch without history:

  ```shell
  git clone --depth 1 -b master git@github.com:geometalab/osmaxx.git osmaxx && cd osmaxx
  git submodule init && git submodule update
  ```
  Repository details see [Project repository](git-repository.md).
2. Link production configuration for docker-compose, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
3. Add target specific environment variables to compose-production.yml
4. Build the containers
5. Run migrations and add create super user, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
6. Load data container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
7. Load database container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
8. Add a system startup script running `docker-compose up`
9. Start the containers
