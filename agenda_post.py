import boto3
import logging
import json
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_agenda')

def get_id():
    response = table.scan()
    return response['Count']
    
def get_if_userId_exists(userId):
    table = dynamodb.Table('table_contas')
    response = table.query(KeyConditionExpression=Key('User').eq(f'{userId}'))
    return response['Count']

def get_if_owner_exists(nome):
    table = dynamodb.Table('table_clientes')
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    return response['Count']

def get_if_animal_exists(nome):
    table = dynamodb.Table('table_animais')
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    return response['Count']

def post_function(data, horas, acao, dono, animal, userId):
    id = get_id()
    table.put_item( Item={
        'Id':id+1,
        'Data':f'{data}',
        'Horas':f'{horas}',
        'Acao':f'{acao}',
        'Dono':f'{dono}',
        'Animal':f'{animal}',
        'UserId':f'{userId}'
    })
    logger.info("INFO ENTRY MADE")


def lambda_handler(event, context):
    userId_exists = get_if_userId_exists(event['body']['userId'])
    owner_exists = get_if_owner_exists(event['body']['owner'])
    animal_exists = get_if_animal_exists(event['body']['animal'])
    if ((userId_exists != 0) and (owner_exists != 0)) and (animal_exists != 0):
        post_function(event['body']['date'], event['body']['hours'], event['body']['action'], event['body']['owner'], event['body']['animal'],event['body']['userId'])
        return {
            'statusCode': 200,
            'body': {'status':'entry made'}
        }
    else:
        return {
            'statusCode': 400,
            'body': {'status':'User/Owner/Client does not exist'}
        }
