# Deployment

To deploy to production server:

1. Clone the repository master branch without history:

  ```shell
  git clone --depth 1 -b master https://github.com/geometalab/osmaxx.git osmaxx && cd osmaxx
  git submodule init && git submodule update
  ```
  Repository details see [Project repository](git-repository.md).
2. Link production configuration for docker-compose, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
3. Add target specific environment variables to compose-production.yml
4. Build the containers.

  ```shell
  docker-compose build --no-cache
  ```
  
  If there is **no docker-compose installed** on the target system, use a docker-compose container:

  ```shell
  docker run \
      -v "/path/to/source/repo:/app" \
      -v "/var/run/docker.sock:/var/run/docker.sock" \
      -e "COMPOSE_PROJECT_NAME=osmaxx" \
      --rm \
      "dduportal/docker-compose:1.2.0" build --no-cache
  ```
5. Run migrations and add create super user, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
  For docker-compose container run:

  ```shell
  docker run \
      -v "/path/to/source/repo:/app" \
      -v "/var/run/docker.sock:/var/run/docker.sock" \
      -e "COMPOSE_PROJECT_NAME=osmaxx" \
      --rm -ti \
      "dduportal/docker-compose:1.2.0" run osmaxxwebapp /bin/bash -c "python3 manage.py migrate && python3 manage.py createsuperuser"
  ```
6. Load data container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
7. Load database container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
8. Add a system startup script running `docker-compose up`
  E.g. /etc/systemd/system/osmaxx.service:

  ```shell
  [Unit]
  Description=Start osmaxx application
  
  [Service]
  ExecStart=/usr/bin/docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.2.0" up -d
  ExecStop=/usr/bin/docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.2.0" stop
  Restart=always
  
  [Install]
  WantedBy=multi-user.target
  ```
9. Start the containers
