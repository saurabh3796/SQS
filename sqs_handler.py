import boto3
import time

# Replace these values with your AWS credentials and SQS URL
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
region_name = 'YOUR_REGION'
queue_url = 'YOUR_SQS_URL'

# Create an SQS client
sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def send_message(message_body):
    # Send a message to the SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    print(f"Sent message with MessageId: {response['MessageId']}")

def receive_message():    
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    messages = response.get('Messages', [])

    if not messages:
        print("No messages in the queue.")
        return

    message = messages[0]
    
    message_body = message['Body']

    print(f"Received message: {message_body}")

    return message

def delete_msg(event):
    try:
        receipt_handle = event['ReceiptHandle']
        sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)
        print(f"Deleted message with ReceiptHandle: {receipt_handle}")
    except Exception as err:
        print(f"Error while deleting message from sqs {err}")

if __name__ == '__main__':
    # Example usage
    send_message("Hello, SQS!")

    # Wait for a while to allow the message to be processed by SQS
    time.sleep(2)

    # Receive messages from the queue one by one
    while True:
        message = receive_message()
        print(f"Message received is {message['Body']}")
        #process the msg
        delete_msg(message)
