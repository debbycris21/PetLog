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

def post_function(nome, telefone, user):
    table.put_item( Item={
        'Nome':f'{nome}',
        'Telefone':f'{telefone}',
        'UserId':f'{user}'
    })
    logger.info("INFO ENTRY MADE")


def lambda_handler(event, context):
    delete_function(event['pathParameters']['name'])
    post_function(event['body']['name'], event['body']['phone'],event['body']['userId'])
    
    return {
        'statusCode': 200,
        'body': {'status':'entry altered'}
    }
