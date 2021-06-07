import json
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentInfomationDB')

def lambda_handler(event, context):
    regno = event.get('regno', None)
    firstname =str(event.get('firstname', None))
    lastname = str(event.get('lastname', None))
    section = str(event.get('section', None))
    
    if  regno==None or not regno or lastname !=None and not lastname or firstname !=None and not firstname or section !=None and not section :
        
        return {
                'statusCode': 400,
                'body': ('invalid event ')
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
            
            response = table.get_item(Key={'regno': str(regno).upper()})
            firstname2=(response["Item"]["firstname"])
            lastname2=(response["Item"]["lastname"])
            section2=(response["Item"]["section"])
            
            def getupdate(lastname,firstname,section):
                response=table.update_item(
                    Key={
                        "regno": str(regno).upper()
                                
                    },
                    
                    UpdateExpression="set lastname=:newlastname , firstname=:newfirstname , #section = :section",
                    ExpressionAttributeValues={
                        ":newlastname": lastname,
                        ":newfirstname": firstname,
                        ":section": section
                    },
                    ExpressionAttributeNames= {
                        "#section": "section"
                        
                      
                    })
            if  firstname!='None' and lastname=='None' and section=='None' :
                print("y x x")

                getupdate(lastname2,firstname,section2)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                }   
                
                

            elif  firstname!='None' and lastname!='None' and section=='None' :
                print("y y x")

                getupdate(lastname,firstname,section2)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                } 
                


            elif  firstname=='None' and lastname!='None' and section=='None' :
                print("x y x")

                getupdate(lastname,firstname2,section2)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                }            
            


            elif  firstname=='None' and lastname=='None' and section!='None' :
                print("x x y")
              
                getupdate(lastname2,firstname2,section)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                        
                }


            elif  firstname=='None' and lastname!='None' and section!='None' :
                print("x y y")
              
                getupdate(lastname,firstname2,section)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                        
                }
                
                
            elif  firstname!='None' and lastname=='None' and section!='None' :
                print("y x y")
              
                getupdate(lastname2,firstname,section)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                        
                }                
                
                

            elif  firstname!='None' and lastname!='None' and section!='None' :
                print("y y y")
              
                getupdate(lastname,firstname,section)
                return{
                            'statusCode': 200,
                            'body':('Data updated successfully')                
                        
                }                 

        else:
            return{
                    'statusCode': 404,
                    'body':('Data about '+regno + ' Not Found')                
                
            }

        
    
    
        

 