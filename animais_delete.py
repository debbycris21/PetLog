import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_animais')

def get_id(nome):
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    return response['Items'][0]['Id']

def delete_function(nome):
    id = get_id(nome)
    table.delete_item( Key={
      "Id":f'{id}'
    })
    logger.info("INFO DELETED")


def lambda_handler(event, context):
    delete_function(event['body']['name'])
    return {
        'statusCode': 200,
        'body': {'status':'entry deleted'}
    }
