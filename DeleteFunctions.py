import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')

def check_if_item_exist(item):
    response = table.get_item(
        Key={
            'regno': item
        }
    )
    return True if ('Item' in response) else False


def lambda_handler(event, context):
    errors=[]
    resp={
    "success":False ,
    "StatusCode":400 ,
    "message":""
    }
    regno = event.get('regno', None)
    if regno==None or not regno:
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]=' Registration Number is Primary Key must be Entered First'
        errors.append( 'errormessage : Invalid registration number ')
        errors.append( 'errormessage : Registration Number is not Entered ')
    else:    
        if(check_if_item_exist(str(regno).upper())):
            response = table.delete_item(
                Key={
                    'regno' : str(regno).upper()
                    })
            resp["success"]=True
            resp["StatusCode"]=200
            resp["message"]='Date Delted Successfully ' 
  
    
        else: 
            resp["success"]=False
            resp["StatusCode"]=404
            resp["message"]='Data not found'
            errors.append('errormessage : Data is not present regarding  ' + regno) 
    resp.setdefault("errors", []).append(errors)            
    return resp
            