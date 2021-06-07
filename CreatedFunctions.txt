import json
import boto3
from datetime import date

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')

def lambda_handler(event, context):
    now = str(date.today())
    print("date and time2 is ",now)
    regno = event.get('regno', None)
    firstname = event.get('firstname', None)
    lastname = event.get('lastname', None)
    section = event.get('section', None)
    
    if firstname==None or not firstname or  regno==None or not regno or lastname==None or not lastname or section!=None and not section :
        return {
                    'statusCode': 404,
                    'body': ('Input Events  Not Found')
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
            return {
                'statusCode': 403,
                'body': ('Data is already uploaded for ' + regno+" already")
            }

    
        else:    
      # write name and time to the DynamoDB table using the object we instantiated and save response in a variable
            response = table.put_item(
                Item={
                    'regno': str(regno).upper(),
                    'firstname':firstname,
                    'lastname':lastname,
                    'section':section,
                    'LatestGreetingTime':now
                    })
        # return a properly formatted JSON object
            return {
                'statusCode': 200,
                'body': ('Data uploaded Successfully for  ' + regno)
            }
