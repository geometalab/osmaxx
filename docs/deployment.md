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
  * If you are using an nginx proxy (jwilder/nginx-proxy), you need to set the environment variable
    `VIRTUAL_HOST=osmaxx.yourdomain.tld`
4. Build the containers. Use docker-compose container instead of native installation:

  a. Create the docker-compose container:
  ```shell
  docker create \
      --name osmaxx-starter
      -v "/path/to/source/repo:/app" \
      -v "/var/run/docker.sock:/var/run/docker.sock" \
      -e "COMPOSE_PROJECT_NAME=osmaxx" \
      "dduportal/docker-compose:1.2.0"
  ```
  
  b. Build osmaxx containers:
  
  ```shell
  docker start osmaxx-starter build --no-cache
  ```
  
5. Run migrations and add create super user, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
  For docker-compose container run:

  ```shell
  docker exec -ti osmaxx-starter /usr/local/bin/docker-compose \
    run webapp /bin/bash -c "python3 manage.py migrate && python3 manage.py createsuperuser"
  ```
6. Load data container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
7. Load database container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
8. Add a system startup script running `docker-compose up`
  E.g. /etc/systemd/system/osmaxx.service:

  ```shell

  [Unit]
  Description=Start osmaxx application

  [Service]
  ExecStart=/usr/bin/docker start -a osmaxx-starter
  ExecStop=/usr/bin/docker exec osmaxx-starter /usr/local/bin/docker-compose stop --timeout 60
  ExecStop=/usr/bin/docker kill --signal=INT osmaxx-starter
  ExecStop=/usr/bin/docker stop -t 10 osmaxx-starter
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
  **important**: osmax-starter container needs to be created before!
  
9. Enable startup service  
  ```shell
  sudo systemctl enable docker-osmaxx.service
  ```
  
10. Start the containers
  ```shell
  sudo systemctl start docker-osmaxx.service
  ```
