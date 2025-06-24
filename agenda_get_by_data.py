import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_agenda')

def get_function(data, userId):
    answ = {}
    my_kwargs = {
    'FilterExpression': Attr('Data').eq(f'{data}') and Attr('UserId').eq(f'{userId}')
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
    response = get_function(event['body']['date'], event['body']['userId'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
