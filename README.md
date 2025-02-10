To Run this app:

1. ```pip3 install -r requirements.txt```
2. download docker and pull localstack image and run the server locally
     ```docker run -d -p 4566:4566 -p 4571:4571 -e SERVICES=sqs -e AWS_ACCESS_KEY_ID=test -e AWS_SECRET_ACCESS_KEY=test localstack/localstack```
3. create a sqs queue on localstack by exec into the image and run
    ```awslocal sqs create-queue --queue-name localstack-queue```
4. Now run the app using:
    ```uvicorn server:app --port 8080 --workers 4 (threads you want to run)```
