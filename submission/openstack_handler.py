import os
import boto3
import time
from mylogger import logger
import json

logger.info("Import complete")

input_queue_url = 'https://sqs.us-east-1.amazonaws.com/595548125787/input-notification'
output_queue_url = 'https://sqs.us-east-1.amazonaws.com/595548125787/output-notification'
lambda_arn = 'arn:aws:lambda:us-east-1:595548125787:function:smart-classroom'

sqs = boto3.client('sqs')
lambda_client = boto3.client('lambda')

folder_path = './datafolder/'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

while True:
    response = sqs.receive_message(
        QueueUrl=input_queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    logger.info(response)
    # Check if a message was retrieved
    if 'Messages' in response:
        message = response['Messages'][0]
        message_body = message['Body']
        message_receipt_handle = message['ReceiptHandle']

        # Delete the retrieved message from the SQS queue
        sqs.delete_message(
            QueueUrl=input_queue_url,
            ReceiptHandle=message_receipt_handle
        )

        # Send the latest message to the Lambda function
        payload = json.dumps(message_body)
        logger.info(payload)

        response = lambda_client.invoke(
            FunctionName=lambda_arn,
            InvocationType='RequestResponse',
            Payload=payload
        )

    # Poll output queue for messages
    output_queue_attributes = sqs.get_queue_attributes(QueueUrl=output_queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    output_message_count = int(output_queue_attributes['Attributes']['ApproximateNumberOfMessages'])
    if output_message_count > 0:
        messages = sqs.receive_message(QueueUrl=output_queue_url, MaxNumberOfMessages=10)
        if 'Messages' in messages:
            for message in messages['Messages']:
                # print(f'Received message: {message["Body"]}')
                sqs.delete_message(QueueUrl=output_queue_url, ReceiptHandle=message['ReceiptHandle'])
                file_name, file_message = message["Body"].split(",")[-1], ",".join(message["Body"].split(",")[:-1])
                with open (folder_path + file_name + ".txt", "w") as fp:
                    fp.write(file_message)
    # Sleep for 1 second before checking again
    time.sleep(1)
