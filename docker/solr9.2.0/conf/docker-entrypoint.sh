#!/bin/bash
set -e
unset SOLR_USER SOLR_UID SOLR_GROUP SOLR_GID \
      SOLR_CLOSER_URL SOLR_DIST_URL SOLR_ARCHIVE_URL SOLR_DOWNLOAD_URL SOLR_DOWNLOAD_SERVER SOLR_KEYS SOLR_SHA512
if [[ "$VERBOSE" == "yes" ]]; then
  set -x
fi
if ! [[ ${SOLR_PORT:-} =~ ^[0-9]+$ ]]; then
 SOLR_PORT=8986
 export SOLR_PORT
fi
init-var-solr
if [ "${1:0:1}" == '-' ]; then
 set -- solr-foreground "$@"
fi
exec "$@"