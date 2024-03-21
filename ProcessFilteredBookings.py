import boto3
from io import StringIO
from datetime import datetime
import json

def lambda_handler(event, context):
    print("Starting SQS Batch Process")
    # Specify your SQS queue URL
    queue_url = 'https://sqs.us-east-1.amazonaws.com/905418247818/AirbnbBookingQueue'

    # Create SQS client
    sqs = boto3.client('sqs')

    #target s3
    fdt = datetime.now().strftime("%Y%m%d%H%M%S")
    tgtbucket='airbnb-booking-records-vj'
    tgtkey='processed_filtered_bookings' + fdt + '.json'
    s3_client = boto3.client('s3')

    # Receive messages from the SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # Adjust based on your preference
        WaitTimeSeconds=2       # Use long polling
    )


    messages = response.get('Messages', [])
    print("Total messages received in the batch : ",len(messages))
    print("messages : ",messages)
    
      
    #response = s3_client.put_object(Body=filetoupload.getvalue(), Bucket=tgtbucket, Key=tgtkey, )
    bookings_data={}
    for message in messages:
        # Process message
        print("Processing message: ", message['Body'])
        bookings_data = bookings_data.update(json.loads(message['Body']))

        # Delete message from the queue
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from the queue")
    #wrtting the msg to file
       
    s3_client.put_object(
        Bucket=tgtbucket,
        Body=(json.dumps(bookings_data)),
        Key=tgtkey
    )     
    print("Ending SQS Batch Process")

    return {
        'statusCode': 200,
        'body': f'{len(messages)} messages processed and deleted successfully'
    }