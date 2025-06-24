import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_clientes')

def get_function(userId):
    answ = {}
    response = table.scan(FilterExpression=Attr('UserId').eq(f'{userId}'))
    print(response)
    for number in range(response['Count']):
        entry = {f'{response['Items'][number]['Id']}':{
            'Nome':f'{response['Items'][number]['Nome']}',
            'Telefone':f'{response['Items'][number]['Telefone']}',
        }
        }
        answ.update(entry)
    return answ

def lambda_handler(event, context):
    response = get_function(event['pathParameters']['userId'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
