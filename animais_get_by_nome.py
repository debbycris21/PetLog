import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_animais')

def get_function(nome):
    answ = {}
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    print(response)
    for number in range(response['Count']):
        entry = {f'{response['Items'][number]['Id']}':{
            'Nome':f'{response['Items'][number]['Nome']}',
            'Dono':f'{response['Items'][number]['Dono']}',
            'Nasc':f'{response['Items'][number]['Nasc']}'
        }
        }
        answ.update(entry)
    return answ

def lambda_handler(event, context):
    response = get_function(event['body']['animalName'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
