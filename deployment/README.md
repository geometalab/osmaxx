# Deployment container for Docker


## Docker installation

### Docker

See https://docs.docker.com/installation/ubuntulinux/

1. Be sure your kernel version is 3.10 or newer and wget is installed
2. Install docker:
    ```shell
    wget -qO- https://get.docker.com/ | sh
    ```
3. Create a docker group and add you
    ```shell
    sudo usermod -aG docker {yourUserName}
    ```

### Docker compose

See https://docs.docker.com/compose/install/

1. Be sure curl is installed
2. Install compose:
    ```shell
    sudo su
    curl -L https://github.com/docker/compose/releases/download/1.2.0/docker-compose-`uname \
    -s`-`uname -m` > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ```


## Build & run container


1. Create archive from source or download from GitHub:
    - From GitHub
    ```shell
    # wget -O 'deployment/osmaxx/source.tar' \
    #   'https://github.com/geometalab/osmaxx/releases/download/{releasenumber}/{release-archive}.tar'
    # Example:
    wget -O 'deployment/osmaxx/source.tar' \
        'https://github.com/geometalab/osmaxx/releases/download/0.2/osmaxx-source-0.2.tar'
    ```

    - Or create from local source or from clean repo:
    ```shell
    # use a clean repo to tar the source
    cd /tmp
    git clone git@github.com:geometalab/osmaxx.git --branch master --single-branch && cd osmaxx
    git submodule init && git submodule update
    tar -cf deployment/osmaxx/source.tar source

    # git archive not working with submodules
    # git archive master --format tar --output deployment/source.tar

    # tar from not-empty repository:
    tar -cf deployment/osmaxx/source.tar \
        --exclude='*.git' --exclude='*.od*' --exclude='*.gitignore' --exclude='*.gitmodules' \
        --exclude='*developmentEnvironment/' --exclude='*data/' --exclude='*.idea' \
        --exclude='*test_db.sqlite' --exclude='*__pycache__/' source
    ```

2. Build containers:

```shell
docker build --tag=osmaxxdatabase --no-cache=true deployment/osmaxxdatabase/
docker build --tag=osmaxx --no-cache=true deployment/osmaxx/
```

3. Run container:
    - By hand:

    ```shell
    docker run -d --name osmaxx-db -e POSTGRES_PASSWORD=***** -e POSTGRES_USER=postgres \
        -e OSMAXX_USER_PASSWORD=***** osmaxxdatabase

    docker run -d -p 8080:80 --name osmaxx --link osmaxx-db:database osmaxx
    ```

        - Debug/Access database by hand:

        ```shell
        # get ip of container
        docker inspect osmaxx-db | grep "IPAddress"
        psql -h {ip} -U postgres

        # psql list users
        \du

        # psql list databases
        \list
        ```

        - Debug application container:

        ```shell
        docker run -it -p 8080:80 --name osmaxx --link osmaxx-db:database osmaxx /bin/bash
        ```

    - Using docker compose:
    ```shell
    cd deployment
    docker-compose up
    ```

    **Note:** If you start the container with custom arguments (e.g. *docker run osmaxx /bin/bash*) you will override the CMD command to start the server.
     So you need to start the server by your self.


## Management

Run container interactive:
```shell
(sudo) docker run -i -t osmaxx /bin/bash
```

Show running containers:
```shell
docker ps
```

Stop running container:
```shell
docker stop {containerID}
```

Save docker image to file:
```shell
docker save osmaxx > /tmp/osmaxx-alpha1.docker-img.tar
```

Load docker image from file:
```shell
docker load < /tmp/osmaxx-alpha1.docker-img.tar
```
