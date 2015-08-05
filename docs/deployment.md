# Deployment

To deploy to production server:

1. Clone the repository, Details see [Project repository](git-repository.md).
2. Link production configuration for docker-compose, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
3. Build the containers
4. Add a system startup script running `docker-compose up`
5. Start the containers
