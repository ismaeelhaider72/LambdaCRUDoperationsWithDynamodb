
import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')
def lambda_handler(event, context):
        # regno = event['regno']
        
        response = table.scan()
        items = response['Items']
        return {
        'statusCode': 200,
        'body': (items)
        }
