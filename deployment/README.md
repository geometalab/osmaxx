# Deployment container for Docker

## Build & run container

1. Be sure your kernel version is 3.10 or newer and wget is installed
2. Install docker: 
    ```shell
    wget -qO- https://get.docker.com/ | sh
    ```
3. Copy current source to docker data:
    ```shell
    git archive master --format tar --output deployment/source.tar
    ```
4. Build image:
    ```shell
    docker build -t osmaxx deployment/
    ```
5. Run container:
    ```shell
    docker run -d -P osmaxx
    ```
    
    
## Management

Run container interactive:
```shell
(sudo) docker run -i -t osmaxx /bin/bash
```