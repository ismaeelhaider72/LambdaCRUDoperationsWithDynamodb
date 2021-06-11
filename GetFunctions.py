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
    
    regno=event.get('regno', None)
    # reg=
    if (regno==None or not regno) :
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]=' Registration Number is Primary Key must be Entered First'
        errors.append( 'errormessage : Invalid registration number ')
        errors.append( 'errormessage : Registration Number is not Entered ')       


    else:
        if(check_if_item_exist(str(regno.upper())) ):        
                    # name = 'ismaeel haider'
            response = table.get_item(Key={'regno': str(regno).upper()})
            result=(response["Item"])
            print("resssss is ",result)
            resp["success"]=True
            resp["StatusCode"]=200
            resp["message"]=' Data Get Successfully'
            resp.setdefault("data",[]).append(result)
            # result.insert(1, "Status Code : 200")
            # result.append(response["Item"])

        else:
            resp["success"]=False,
            resp["StatusCode"]=404
            resp["message"]=' Data is not present'
            errors.append( 'errormessage : Data not found / registration no does not match the any data primary key')
                  

            
    resp.setdefault("errors", []).append(errors)            
    return resp


  