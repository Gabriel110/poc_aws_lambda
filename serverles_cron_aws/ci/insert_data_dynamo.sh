#!/usr/bin/env bash
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name my_table --item  file://json/registro1.json
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name my_table --item  file://json/registro2.json
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name my_table --item  file://json/registro3.json
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name my_table --item  file://json/registro4.json
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name my_table --item  file://json/registro5.json

