#!/usr/bin/env bash
aws --endpoint-url=http://localhost:4566 sns create-topic --name test-sns
aws --endpoint-url=http://localhost:4566 sns list-topics
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name test-sqs
aws --endpoint-url=http://localhost:4566 sqs list-queues
aws --endpoint-url=http://localhost:4566 sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:test-sns --protocol sqs --notification-endpoint http://localhost:4566/000000000000/test-sqs
aws --endpoint-url=http://localhost:4566 sns list-subscriptions
aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/test-sqs

aws --endpoint-url=http://localhost:4566 sns publish --topic-arn arn:aws:sns:us-east-1:000000000000:test-sns --message 'Bem-vindo ao Onexlab!'