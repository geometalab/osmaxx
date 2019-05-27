FROM nginx:alpine

COPY ./docker_entrypoint/nginx/default.conf.template /etc/nginx/conf.d/default.conf.template
CMD DOMAIN_NAMES=$(echo $VIRTUAL_HOST | sed 's/,/ /g') envsubst '$DOMAIN_NAMES' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf \
    && cat /etc/nginx/conf.d/default.conf \
    && nginx -g 'daemon off;'
