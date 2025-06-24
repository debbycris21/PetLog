import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_animais')

def get_last_id():
    response = table.scan()
    return response['Count']
    

def get_id(nome):
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    return response['Items'][0]['Id']

def delete_function(nome):
    id = get_id(nome)
    table.delete_item( Key={
      "Id":f'{id}'
    })
    logger.info("INFO DELETED")


def post_function(name, own, nasc, userId):
    id = get_last_id()
    table.put_item( Item={
        'Id':str(id+1),
        'Nome':f'{name}',
        'Dono':f'{own}',
        'Nasc':f'{nasc}',
        'UserId':f'{userId}'
    })
    logger.info("INFO ENTRY MADE")

def lambda_handler(event, context):
    delete_function(event['pathParameters']['name'])
    post_function(event['body']['name'], event['body']['owner'], event['body']['birth'],event['body']['userId'])
    return {
        'statusCode': 200,
        'body': {'status':'entry altered'}
    }
