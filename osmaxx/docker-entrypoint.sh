#!/bin/bash

set -ex

# Add local user
# Either use the LOCAL_USER_ID if passed in at runtime or
# fallback

USER_ID=${USER_ID:-2222}
GROUP_ID=${GROUP_ID:-100}

echo "Starting with UID : $USER_ID as user ${USERNAME}"

useradd -s /bin/bash --uid ${USER_ID}  --no-create-home --gid ${GROUP_ID} -d ${HOME} ${USERNAME}

chown -R ${USERNAME} ${HOME}

gosu ${USERNAME} "$@"
