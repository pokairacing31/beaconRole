import json
import boto3
from boto3.dynamodb.conditions import Key, Attr, And

def auth_check(event):
    dynamodb = boto3.resource('dynamodb')
    auth_table = dynamodb.Table('authentication')
    query_auth = auth_table.get_item(
        Key={
        'access_token': event.header.access_token
        }
    )
    try:
        if len(query_auth)!=0:
            #user_id = query_auth['Item']['access_token']
            handle_role_event(event, query_auth['userId'])
    except:  
        return {
            "statusCode": 403,
            "data" : json.dumps({
                "statusCode": 403,
                "data": "Missing Authentication Token"
                }),
            "isBase64Encoded": False
        }
def handle_role_event(event, userId):
    dynamodb = boto3.resource('dynamodb')
    personal_table = dynamodb.Table('LineService')
    personal_query = personal_table.query(
        KeyConditionExpression=Key('userId').eq(userId) & Key('funcId').eq('beacon')
    )
    personal_role = personal_query['Items'][0]['role']['Beacon']
    personal_role_keys = list(personal_role.keys())
    stores = [store.split('#')[0] for store in personal_role_keys]
    branches = [branch.split('#')[1] for branch in personal_role_keys]
    personal_role_values = list(personal_role.values())
    print(personal_role_values)
    print(stores, branches)
    method = event.body.method
    branch_id = event.body.branchId
    role_type = event.body.role_type
    ch_userId = event.body.ch_userId
    beacon_table = dynamodb.Table('LineService')
    for i in range(len(personal_role_values)):
        if personal_role_values[i] == "headManager":
            manage_store =  beacon_table.query(
                KeyConditionExpression=Key('userId').eq(stores[i]) & Key('funcId').eq('beacon')
            )
            if method == 'ADD':
                beacon_table.update_item(
                    Key={
                        "userId":stores[i],
                        "funcId":"beacon"
                    }
                    UpdateExpression = "SET branchRole.#Role = :",
                    ExpressionAttributeName={
                        "#Role":role_type,
                        
                    }

                )
            elif method == 'DELETE':

            elif method == 'CHANGE':
                
            
            
            manage_branchManger = manage_store['Items'][0]['branch#'+branches[i]]['branchRole']['branchManager']
            print(manage_branchManger)

    
    
    
    
    # if role == 'HeadManager':
    #     email = event.body.email
    #     role_type = event.body.role_type
    #     ch_user_id = event.body.branch_id
    #     info_table.update_iem(
    #         Key={
    #             "userid":ch_user_id
    #         },
    #         UpdateExpression='SET role = :newRole',
    #         ExpressionAttributeValues={
    #             ':newRole':role_type
    #         },
    #         ReturnValues="UPDATED_NEW"
    #     )
    #     return "change_finish"
    # else:
    #     return "unchage"

# event = {"body":{"email":"test_email","role_type":"BranchManager","ch_user_id":"role_test"}}
handle_role_event("event",'Ub59c41d4adf7d043b489aa60d4faad01')

# dynamodb = boto3.resource('dynamodb')
# info_table = dynamodb.Table('LineService')
# info_table.update_item(
#             Key={
#                 "userid":"role_test",
#                 "funcId":"beacon"
#             },
#             UpdateExpression='SET #role.#role = :s',
#             ExpressionAttributeNames={
#                 '#role':'role'
#             },
#             ExpressionAttributeValues={
#                 ':s': 'BranchManager'
#             },
#             ReturnValues="UPDATED_NEW"
#         )
# get_info = info_table.get_item(
#     Key={
#         "userId":"role_test",
#         "funcId":"beacon"
#     }
# )
#print(get_info)

{'Item': {'funcId': 'beacon', 'role': {'role': 'BranchStaff'},
 'userId': 'role_test'}
, 'ResponseMetadata': {'RequestId': 'KOGIHOH1U4FM2DJ13B8NRLNAKBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Mon, 05 Dec 2022 00:20:43 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '109', 'connection': 'keep-alive', 'x-amzn-requestid': 'KOGIHOH1U4FM2DJ13B8NRLNAKBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '653488135'}, 'RetryAttempts': 0}}


{
  "userId": {
    "S": "role_test"
  },
  "funcId": {
    "S": "beacon"
  },
  "role": {
    "M": {
      "role": {
        "S": "BranchStaff"
      }
    }
  }
}