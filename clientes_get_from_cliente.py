import boto3
import logging
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_clientes')

def get_function(cliente_nome):
    response = table.query(
        KeyConditionExpression=Key('Nome').eq(f'{cliente_nome}')
    )
    answ = {
        'Cliente':response['Items'][0]['Nome'],
        'telefone':response['Items'][0]['Telefone'],
        'User':response['Items'][0]['UserId']
    }
    return answ

def lambda_handler(event, context):
    response = get_function(event['body']['name'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
