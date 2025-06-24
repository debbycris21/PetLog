import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_animais')

def get_id():
    response = table.scan()
    return response['Count']
    
def get_if_userId_exists(userId):
    table = dynamodb.Table('table_')
    response = table.query(KeyConditionExpression=Key('User').eq(f'{userId}'))
    return response['Count']
    
def get_if_owner_exists(nome):
    table = dynamodb.Table('table_clientes')
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    print(response)
    return response['Count']

def post_function(name, own, nasc, userId):
    id = get_id()
    table.put_item( Item={
        'Id':id+1,
        'Nome':f'{name}',
        'Dono':f'{own}',
        'Nasc':f'{nasc}',
        'UserId':f'{userId}'
    })
    logger.info("INFO ENTRY MADE")


def lambda_handler(event, context):
    userId_exists = get_if_userId_exists(event['body']['userId'])
    owner_exists = get_if_owner_exists(event['body']['owner'])
    if (userId_exists != 0) and (owner_exists != 0):
        post_function(event['body']['name'], event['body']['owner'], event['body']['birth'],event['body']['userId'])
        return {
            'statusCode': 200,
            'body': {'status':'entry made'}
        }
    else:
        return {
            'statusCode': 400,
            'body': {'status':'userId or owner does not exist'}
        }
