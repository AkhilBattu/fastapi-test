from fastapi import FastAPI
import boto3
import asyncio
import logging

# Initialize FastAPI app
app = FastAPI()

# Configure SQS client with LocalStack endpoint
sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",         # dummy AWS access key
    aws_secret_access_key="test" 
)
queue_url = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-queue"

# Logger setup
logging.basicConfig(level=logging.INFO)

async def poll_sqs():
    """Continuously poll the SQS queue and process messages."""
    while True:
        try:
            # Receive messages from SQS
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10  # Long polling
            )

            messages = response.get("Messages", [])
            if messages:
                for message in messages:
                    logging.info(f"Received message: {message['Body']}")
                    # Process the message
                    process_message(message)
                    
                    # Delete the message after processing
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    logging.info("Message deleted from the queue")
            else:
                logging.info("No messages available")
        except Exception as e:
            logging.error(f"Error polling SQS: {e}")
        await asyncio.sleep(5)  # Wait before polling again

def process_message(message):
    """Custom logic to process a message."""
    logging.info(f"Processing message: {message['Body']}")

@app.on_event("startup")
async def startup_event():
    """Start polling SQS when the server starts."""
    asyncio.create_task(poll_sqs())

@app.get("/")
async def root():
    return {"message": "FastAPI server is running and polling SQS"}