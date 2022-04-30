aws --endpoint-url=http://localhost:4566 dynamodb describe-table --table-name my_table 
aws --endpoint-url=http://localhost:4566 dynamodb put-item --table-name my_table --item '{\"id\":{\"S\":\"1\"},\"Nome\": {\"S\": \"Gabriel\"}}' 
serverless deploy --stage local 
serverless info --stage local 
serverless invoke local -f hello 
aws --endpoint-url=http://localhost:4566 sns create-topic --name test-sns 
aws --endpoint-url=http://localhost:4566 sns list-subscriptions 
aws --endpoint-url=http://localhost:4566 sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:test-sns --protocol sqs --notification-endpoint http://localhost:4566/000000000000/test-sqs
aws --endpoint-url=http://localhost:4566 sns list-topics 
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name test-sqs 
aws --endpoint-url=http://localhost:4566 sqs list-queues
aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/test-sqs
