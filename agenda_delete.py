import boto3
import logging
import json
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_agenda')

def delete_function(id):
    table.delete_item( Key={
      "Id":int(id)
    })
    logger.info("INFO DELETED")

def lambda_handler(event, context):
    delete_function(event['pathParameters']['id'])
    return {
        'statusCode': 200,
        'body': json.dumps('entry deleted!')
    }
