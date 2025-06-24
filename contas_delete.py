import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_contas')
def delete_function(user):
    table.delete_item( Key={
      "User":f'{user}'
    })
    logger.info("INFO DELETED")


def lambda_handler(event, context):
    delete_function(event['body']['user'])
    return {
        'statusCode': 200,
        'body': {'status':'entry deleted'}
    }
