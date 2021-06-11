
import boto3
import json
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')

update_expression_values = []
expression_attribute_values = {}

######################################################## Method that return True if data against given registration number exist of not  ########################

def check_if_item_exist(item):
    response = table.get_item(
        Key={
            'regno': item
        }
    )
    return True if ('Item' in response) else False

############################################################# Method to make update pattern #######################################################################
    
def process_event_key(event, key,regno,update_expression_values,expression_attribute_values):

    if key in event:
        section3=str(event.get('section', None))
        if  section3 =='None'  :
            response = table.get_item(Key={'regno': str(regno).upper()})
            if not "section" in response:
                update_expression_values.append(key + ' = :val_' + key)
                expression_attribute_values[':val_' + key] = event[key]
                update_expression_values.append('#section  = :' + 'section')
                expression_attribute_values[':section'] = "null"
                update_expression_values = list(dict.fromkeys(update_expression_values))
            else:
                section2=(response["Item"]["section"])
                update_expression_values.append(key + ' = :val_' + key)
                expression_attribute_values[':val_' + key] = event[key]
                update_expression_values.append('#section  = :' + 'section')
                expression_attribute_values[':section'] = section2
                update_expression_values = list(dict.fromkeys(update_expression_values))

        elif 'section' in key:
            update_expression_values.append('#'+key + ' = :' + key)
            expression_attribute_values[':' + key] = event[key]
            

        elif section3 !='None'  :
            update_expression_values.append(key + ' = :val_' + key)
            expression_attribute_values[':val_' + key] = event[key]   
            
############################################################### validate input method #####################################################################
def validatesInput(firstname,lastname,section,errors,resp):
    
    if (firstname!=None and not firstname):
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]='Requested Inputs are not completes'                
        errors.append("errormessage : firstname not valid/Firstname is empty")
        
    if (lastname!=None and not lastname):
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
            
            
######################################################################## Main Lamdba Functions ###########################################################
    
def lambda_handler(event, context):
    errors=[]
    resp={
    "success":False ,
    "StatusCode":400 ,
    "message":""
    }    
    
    global update_expression_values
    global expression_attribute_values
    
    update_expression_values = []
    expression_attribute_values = {}
    regno = event['regno']
    firstname =str(event.get('firstname', None))
    lastname = str(event.get('lastname', None))
    section = str(event.get('section', None))
    
    if regno==None or  not regno :
        resp["success"]=False
        resp["StatusCode"]=400
        resp["message"]=' Registration Number is Primary Key must be Entered First'
        errors.append( 'errormessage : Invalid registration number ')
        errors.append( 'errormessage : Registration Number is not Entered ')
        
    elif(check_if_item_exist(str(regno).upper())):
        if(validatesInput(firstname,lastname,section,errors,resp)):
        # if not errors:    
                process_event_key(event, 'firstname',regno,update_expression_values,expression_attribute_values)
                process_event_key(event, 'lastname',regno,update_expression_values,expression_attribute_values)
                process_event_key(event, 'section',regno,update_expression_values,expression_attribute_values)
                if(update_expression_values):
                    seperator = ','
                    
                    update = table.update_item(
                        Key={
                            'regno': regno
                        },
                        UpdateExpression='SET ' + seperator.join(update_expression_values),
                        ExpressionAttributeValues=expression_attribute_values
                        ,
                        ExpressionAttributeNames= {
                            "#section": "section"
                        })
                    resp["success"]=True
                    resp["StatusCode"]=200
                    resp["message"]='Data update Successfully'
                else:
                    resp["success"]=False
                    resp["StatusCode"]=400
                    resp["message"]='Request is empty'
                    errors.append("errormessage :don't have any parameter to update / ExpressionAttributeValues is empty")
                    
    else:
        resp["success"]=False
        resp["StatusCode"]=404
        resp["message"]='Data Not Found try again with correct regno first'
        errors.append("errormessage : Requested Input key does not match the Data primary key")
        
        
    resp.setdefault("errors", []).append(errors)            
    return resp

 
            
        



            
        