# import the json utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3


# create a DynamoDB object using the AWS SDk
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')


def lambda_handler(event, context):

    regno = event.get('regno', None)
    if regno==None or not regno:
        return{
            'statusCode': 403,
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
                
        if(check_if_item_exist(str(regno).upper())):
            response = table.delete_item(
                Key={
                    'regno' : str(regno).upper()
                    })
        # return a properly formatted JSON object
            return {
                'statusCode': 200,
                'body':('Data about '+regno+ "  is delete")
            }    
    
        else: 
            return {
                'statusCode': 404,
                'body':('Data about '+regno+ " Not Found")
            }             
