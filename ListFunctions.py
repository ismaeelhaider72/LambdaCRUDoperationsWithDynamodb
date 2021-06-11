
import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')
def lambda_handler(event, context):
        
        errors=[]
        result=[]
        resp={
        "success":False ,
        "StatusCode":400 ,
        "message":""
        }
                
        response = table.scan()
        items = response['Items']
        result.append(items)
        if result[0]:
                resp["success"]=True
                resp["StatusCode"]=200
                resp["message"]=' Successfully get complete data'
                resp.setdefault("data",[]).append(result)
        else:
                resp["success"]=False
                resp["StatusCode"]=404
                resp["message"]=' Data not Found'
                errors.append( 'errormessage : Database is empty ') 
    
        resp.setdefault("errors", []).append(errors)            
        return resp                        
                

                
        