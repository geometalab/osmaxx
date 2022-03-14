The version downloaded apparently doesn't yield the correct version when using releases, therefore 
a change in `gdal/docker/ubuntu-full/bh-gdal.sh` might be needed:


```bash
# ...

# comment out
# wget -q "https://github.com/${GDAL_REPOSITORY}/archive/${GDAL_VERSION}.tar.gz" \
#     -O - | tar xz -C gdal --strip-components=1

# removes the "v"
GDAL_V=${GDAL_VERSION#?}
wget -q "https://github.com/${GDAL_REPOSITORY}/releases/download/v${GDAL_V}/gdal-${GDAL_V}.tar.gz" \
    -O - | tar xz -C gdal --strip-components=1

# ...
```

**and replace** in `ubunutu-full/Dockerfile`:

```dockerfile
ARG WITH_FILEGDB=
```

with

```dockerfile
ARG WITH_FILEGDB=1
```


**if issues with libjxl, checkout specific version**:

ie. -> `&& git checkout v0.6.1`

```dockerfile
# Build libjxl
RUN . /buildscripts/bh-set-envvars.sh \
    && git clone https://github.com/libjxl/libjxl.git \
    && cd libjxl \
    && git checkout v0.6.1 \
    && git submodule update --init --recursive \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF .. \
    && make -j$(nproc) \
    && make -j$(nproc) install \
    && make install DESTDIR="/build_thirdparty" \
    && cd ../.. \
    && rm -rf libjxl
```