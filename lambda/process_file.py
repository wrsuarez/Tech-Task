import datetime
from base64 import b64decode
import boto3
import os
import uuid

#Define Global Variables
KEYWORD_TEXT_BUCKET = os.environ['KEYWORD_TEXT_BUCKET']
KEYWORD_TEXT_KEY = os.environ['KEYWORD_TEXT_KEY']
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
TRACKING_DYNAMODB_TABLE = os.environ['TRACKING_DYNAMO_TABLE']


def lambda_handler(event, context):
    # Decode the binary object passed into the API
    try:
        content = b64decode(event['body-json'])

        # Fetch and load the keywords text file from S3
        s3 = boto3.resource('s3')
        s3.Object(KEYWORD_TEXT_BUCKET, KEYWORD_TEXT_KEY).download_file('/tmp/' + KEYWORD_TEXT_KEY)
        keywords_file = open('/tmp/' + KEYWORD_TEXT_KEY, mode='r')

        # Iterate over the Keywords text file and replace the relevant strings in the passed in text file
        completed_items = []
        for item in keywords_file:
            item = item.rstrip()
            if item not in completed_items:
                content = content.replace(item, item + u"\u24c7")
                completed_items.append(item)

        # Set up and output the new text document to S3, pass a pre-signed URL to download the object as the response
        output_document_key_name = str(event['params']['header']['x-requester']) + str(uuid.uuid4()) + ".txt"
        s3.Object(OUTPUT_BUCKET, output_document_key_name).put(Body=content, ContentType='multipart/form-data')
        s3_client = boto3.client('s3')
        download_url = s3_client.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': OUTPUT_BUCKET,
                                                                                           'Key': output_document_key_name})

        # Log the request in DynamoDB for tracking
        dynamodb = boto3.resource('dynamodb')
        dynamo_table = dynamodb.Table(TRACKING_DYNAMODB_TABLE)
        dynamo_table.put_item(Item={'outputid': output_document_key_name, 'timestamp': str(datetime.datetime.now())})

        # Send the link to download the completed file
        response_object = {
            "status": "success",
            "download_url": download_url
        }
        return response_object

    except Exception as e:
        response_object = {
            "status": "error",
            "error_message": str(e)
        }
        return response_object



