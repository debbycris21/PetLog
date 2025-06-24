import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_clientes')

def get_last_id():
    response = table.scan()
    return response['Count']

def get_if_userId_exists(userId):
    table = dynamodb.Table('table_')
    response = table.query(KeyConditionExpression=Key('User').eq(f'{userId}'))
    return response['Count']
    
def post_function(name, phone, userId):
    id = get__id()
    table.put_item( Item={
            'Id':id+1,
            'Nome':f'{name}',
            'Telefone':f'{phone}',
            'UserId':f'{userId}'
        
    })
    logger.info("INFO ENTRY MADE")


def lambda_handler(event, context):
    userId_exists = get_if_userId_exists(event['body']['userId'])
    if userId_exists != 0:
        response = post_function(event['body']['name'], event['body']['phone'],event['body']['userId'])
        return {
            'statusCode': 200,
            'body': {'status':json.dumps(response)}
        }
    else:
        return {
            'statusCode': 400,
            'body': {'status':'userId does not exist'}
        }
