# Deployment

To deploy to production server:

1. Clone the repository, Details see [Project repository](git-repository.md).
2. Link production configuration for docker-compose, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
3. Build the containers
4. Run migrations and add create super user, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
5. Load data container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
6. Load database container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
7. Add a system startup script running `docker-compose up`
8. Start the containers
