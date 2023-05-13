## Comando terraform
- terraform init
- terraform plan
- terraform apply --auto-approve 
- terraform plan -destroy --auto-approve
- terraform apply -destroy --auto-approve 

## Comando aws
  - aws lambda --endpoint http://localhost:4566 get-function --function-name lambda-process
  - aws lambda invoke --function-name gabriel --endpoint-url=http://localhost:4566 --payload 'eyJxdWFudGl0eSI6IDJ9' output.txt
  - aws --endpoint-url=http://localhost:4566 lambda list-functions
  - aws --endpoint-url=http://localhost:4566 sns list-subscriptions
  - aws --endpoint-url=http://localhost:4566 sns publish --topic-arn arn:aws:sns:us-east-1:000000000000:sns-lambda --message 'Bem-vindo ao labda Gacodes!'
  - aws --endpoint-url=http://localhost:4566 sqs list-queues
  - aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/sqs-lambda --message-body 'Welcome to SQS queue by Gacodes'
  - aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/sqs-lambda