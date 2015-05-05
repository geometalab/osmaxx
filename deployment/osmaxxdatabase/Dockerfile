FROM near/postgis:9.4-2.1

MAINTAINER Tobias Blaser <tblaser@hsr.ch>

COPY setup-database.sh /usr/local/bin/setup-database.sh
RUN chmod +x /usr/local/bin/setup-database.sh
COPY osmaxx-entrypoint.sh /osmaxx-entrypoint.sh
RUN chmod +x /osmaxx-entrypoint.sh

ENTRYPOINT ["/osmaxx-entrypoint.sh"]
