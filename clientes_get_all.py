import boto3
import logging
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_clientes')

def get_all():
    response = table.scan()
    ans = {}
    for entry in range(response['Count']):
        ans.update({
            f'{entry + 1}':{"data":f'{response['Items'][entry]}'}
        })
    return ans


def lambda_handler(event, context):
    response = get_all()
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
