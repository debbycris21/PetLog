import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_clientes')
def delete_function(cliente):
    table.delete_item( Key={
      "Nome":f'{cliente}'
    })
    logger.info("INFO DELETED")


def lambda_handler(event, context):
    delete_function(event['pathParameters']['name'])
    return {
        'statusCode': 200,
        'body': {'status':'entry deleted'}
    }
