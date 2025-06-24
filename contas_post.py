import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_contas')
def post_function(user, mail, passw):
    table.put_item( Item={
        'User':f'{user}',
        'Mail':f'{mail}',
        'Passw':f'{passw}'
    })
    logger.info("INFO ENTRY MADE")


def lambda_handler(event, context):
    post_function(event['body']['user'], event['body']['email'],event['body']['password'])
    return {
        'statusCode': 200,
        'body': {'status':'entry made'}
    }
