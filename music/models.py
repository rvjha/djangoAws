from django.http import request, response
from django.http.response import HttpResponse
from accounts.models import (
    get_table,
)

# Create your models here.
import boto3
from botocore.exceptions import ClientError

dynamodb_client = boto3.client("dynamodb")
dynamodb = boto3.resource("dynamodb")

# subscribe artist
def subscribe_func(data):
    t = get_table("subscribe")
    songId = print(data["songId"])
    userId = data["uId"]
    if "Table" in t:
        table = dynamodb.Table("subscribe")
        try:
            response = table.get_item(
                Key={
                    "uId": userId,
                }
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            if "Item" in response:
                response = table.update_item(
                    Key={
                        "uId": userId,
                    },
                    UpdateExpression="set sIds=:nd",
                    ExpressionAttributeValues={
                        ":nd": {"sId": songId},
                    },
                    ReturnValues="UPDATED_NEW",
                )
                print(response)
                return HttpResponse("added")
            else:
                response = table.put_item(
                    Item={
                        "uId": userId,
                        "sIds": {"sId": songId},
                    },
                )
                if "ResponseMetadata" in response:
                    response = table.update_item(
                        Key={
                            "uId": userId,
                        },
                        UpdateExpression="set sIds.sId=:nd",
                        ExpressionAttributeValues={
                            ":nd": {"S": [songId]},
                        },
                        ReturnValues="UPDATED_NEW",
                    )
                    print(response)
                    return HttpResponse("added")
                else:
                    return False
    else:
        return HttpResponse(False)