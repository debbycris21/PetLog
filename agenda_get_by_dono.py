import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_agenda')

def get_function(cliente_nome, userId):
    answ = {}
    response = table.scan(FilterExpression=Attr('Dono').eq(f'{cliente_nome}'))
    my_kwargs = {
    'FilterExpression': Attr('Dono').eq(f'{cliente_nome}') and Attr('UserId').eq(f'{userId}')
}
    response = table.scan(**my_kwargs)
    for number in range(response['Count']):
        entry = {f'{response['Items'][number]['Id']}':{
            'Animal':f'{response['Items'][number]['Animal']}',
            'Acao':f'{response['Items'][number]['Acao']}',
            'Dono':f'{response['Items'][number]['Dono']}',
            'Data':f'{response['Items'][number]['Data']}',
            'Horas':f'{response['Items'][number]['Horas']}'
        }
        }
        answ.update(entry)
    return answ

def lambda_handler(event, context):
    response = get_function(event['body']['owner'], event['body']['userId'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
