import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')
def lambda_handler(event, context):

    regno=event.get('regno', None)
    # reg=
    if regno==None or not regno :
        return {
            'statusCode': 404,
            'body':("Input Events  Not Found")            
        }

    else:
        def check_if_item_exist(item):
            response = table.get_item(
                Key={
                    'regno': item
                }
            )
            if 'Item' in response:
               
                return True

            else:
                return False
        
        
        if(check_if_item_exist(str(regno.upper())) ):        
                    # name = 'ismaeel haider'
            response = table.get_item(Key={'regno': str(regno).upper()})
            result=(response["Item"])
            return {
                'statusCode': 200,
                'body':(result)
            }
        else:
            return {
                'statusCode': 404,
                'body':("Data Not Found")
            }
            



  