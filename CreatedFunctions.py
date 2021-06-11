import json
import boto3
from datetime import date
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')

################################### Methods ########################################
########### Methhod (1)to Check is the given regno is already exist or not  ###############
def check_if_item_exist(item):
    response = table.get_item(
        Key={
            'regno': item
        }
    )
    return True if ('Item' in response) else False
    
    
############################################## Method to check the validation of input ################
def validatesInput(firstname,lastname,section,errors,resp):
    
    if (firstname==None or not firstname):
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]='Requested Inputs are not completes'                
        errors.append("errormessage : firstname not valid/Firstname is empty")

        
    if (lastname==None or not lastname):
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]='Requested Inputs are not completes' 
        errors.append("errormessage :lastname not valid/lastname is empty")
        
    if (section!=None and not section):
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]='Requested Inputs are not completes' 
        errors.append("errormessage : sectoin not valid/sectoin is empty")
    return True if (not errors ) else False    

################################################ main lambda function ##########################################
def lambda_handler(event, context):
    errors=[]
    resp={
    "success":False ,
    "StatusCode":400 ,
    "message":""
    }
    regno = event.get('regno', None)
    regno=str(regno.upper())
    print(regno)
    firstname = event.get('firstname', None)
    lastname = event.get('lastname', None)
    section = event.get('section', None)
    
    if  (regno==None or not regno) :
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]=' Registration Number is Primary Key must be Entered First'
        errors.append( 'errormessage : Invalid registration number ')
        errors.append( 'errormessage : Registration Number is not Entered ')

    elif(check_if_item_exist(str(regno.upper())) or check_if_item_exist(str(regno.lower())) ):
        # if (check_if_item_exist(str(regno.lower())) )
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]='Duplication of data may occur try with another registration number '
        errors.append('errormessage : Data is already uploaded for ' + regno)
            

    
    elif(validatesInput(firstname,lastname,section,errors,resp)):
        response = table.put_item(Item=event)
        resp["success"]=True
        resp["StatusCode"]=200
        resp["message"]='Date stored Successfully ' 

    else:
        resp
    # if not errors:
    #     return resp
    # else:    
    resp.setdefault("errors", []).append(errors)            
    return resp