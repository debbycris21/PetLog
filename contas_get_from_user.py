import boto3
import logging
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_contas')

def get_function(user):
    response = table.query(
        KeyConditionExpression=Key('User').eq(f'{user}')
    )
    answ = {
        'User':response['Items'][0]['User'],
        'Mail':response['Items'][0]['Mail']
    }
    return answ

def lambda_handler(event, context):
    response = get_function(event['body']['user'])
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
