import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_contas')
def delete_function(user):
    table.delete_item( Key={
      "User":f'{user}'
    })
    logger.info("INFO DELETED")

def post_function(user, mail, passw):
    table.put_item( Item={
        'User':f'{user}',
        'Mail':f'{mail}',
        'Passw':f'{passw}'
    })
    logger.info("INFO ENTRY MADE")


def lambda_handler(event, context):
    delete_function(event['pathParameters']['user'])
    post_function(event['body']['user'], event['body']['email'],event['body']['password'])
    
    return {
        'statusCode': 200,
        'body': {'status':'entry altered'}
    }
