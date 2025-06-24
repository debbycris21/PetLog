import boto3
import logging
import json
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table= dynamodb.Table('table_agenda')

def alter_function(id, data, horas, acao, dono, animal, userId):
    table.update_item(Key={Key('Id').eq(f'{id}')}, AttributeUpdates={
        'Data':f'{data}',
        'Horas':f'{horas}',
        'Acao':f'{acao}',
        'Dono':f'{dono}',
        'Animal':f'{animal}',
        'UserId':f'{userId}'
    })


def get_id():
    response = table.scan()
    return response['Count']
    
def get_if_userId_exists(userId):
    table = dynamodb.Table('table_contas')
    response = table.query(KeyConditionExpression=Key('User').eq(f'{userId}'))
    return response['Count']

def get_if_owner_exists(nome):
    table = dynamodb.Table('table_clientes')
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    return response['Count']

def get_if_animal_exists(nome):
    table = dynamodb.Table('table_animais')
    response = table.scan(FilterExpression=Attr('Nome').eq(f'{nome}'))
    return response['Count']

def post_function(data, horas, acao, dono, animal, userId):
    id = get_id()
    table.put_item( Item={
        'Id':id+1,
        'Data':f'{data}',
        'Horas':f'{horas}',
        'Acao':f'{acao}',
        'Dono':f'{dono}',
        'Animal':f'{animal}',
        'UserId':f'{userId}'
    })
    logger.info("INFO ENTRY ALTERED")


def get_function_and_delete(data,hora,userId):
    list = {}
    my_kwargs = {
    'FilterExpression': Attr('Data').eq(f'{data}') and Attr('Horas').eq(f'{hora}')
}
    response = table.scan(**my_kwargs)
    for number in range(response['Count']):
        entry = {
            'Id' : f'{response['Items'][number]['Id']}',
            'Animal':f'{response['Items'][number]['Animal']}',
            'Acao':f'{response['Items'][number]['Acao']}',
            'Dono':f'{response['Items'][number]['Dono']}',
            'Data':f'{response['Items'][number]['Data']}',
            'Horas':f'{response['Items'][number]['Horas']}'
        
        }
        list.update(entry)
    print(list)
    return list['Id']
    
def delete_function(id):
    table = dynamodb.Table('table_agenda')
    table.delete_item( Key={
      "Id":int(id)
    })
    logger.info("INFO DELETED")


def lambda_handler(event, context):
    delete_function(id_for_deletion)
    userId_exists = get_if_userId_exists(event['body']['userId'])
    owner_exists = get_if_owner_exists(event['body']['owner'])
    animal_exists = get_if_animal_exists(event['body']['animal'])
    if ((userId_exists != 0) and (owner_exists != 0)) and (animal_exists != 0):
        alter_function(id, event['body']['date'], event['body']['hours'], event['body']['action'], event['body']['owner'], event['body']['animal'],event['body']['userId'])
        return {
            'statusCode': 200,
            'body': {'status':'entry altered'}
        }
    else: return {
        'statusCode': 400,
        'body': {'status':'error userId, owner, animal doesnt exist'}
    }
