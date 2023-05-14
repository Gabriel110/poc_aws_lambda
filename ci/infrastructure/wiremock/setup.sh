#!/bin/bash

if [[ -z "${MARS_TEST_PROJECT_GIT}" ]]; then
  DATA_DIR=/mocks/mappings
  HOST_URL=http://wiremock:${WIREMOCK_PORT}
else
  DATA_DIR=$(pwd)/mocks/mappings
  HOST_URL=http://localhost:${WIREMOCK_PORT}
fi

echo '---------------------------------- AGUARDE 1SEG'
sleep 15
/usr/bin/curl -v -X POST -d @$DATA_DIR/redelabs/proposal-offers.json $HOST_URL/__admin/mappings
/usr/bin/curl -v -X POST -d @$DATA_DIR/redelabs/proposal-post.json $HOST_URL/__admin/mappings
/usr/bin/curl -v -X POST -d @$DATA_DIR/redelabs/proposal-prices.json $HOST_URL/__admin/mappings
/usr/bin/curl -v -X POST -d @$DATA_DIR/redelabs/proposal-query.json $HOST_URL/__admin/mappings
/usr/bin/curl -v -X POST -d @$DATA_DIR/get-health.json $HOST_URL/__admin/mappings
echo 'Etapa do Wiremock concluída!'