from django.http import response
from django.contrib.auth.hashers import make_password, check_password
import boto3
from botocore.exceptions import ClientError
import requests
from pathlib import Path
import os
from boto3.dynamodb.conditions import Key

# import requests

dynamodb_client = boto3.client("dynamodb")
# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
dynamodb = boto3.resource("dynamodb")
s3_resource = boto3.resource("s3")

# get table
def get_table(ty,tbName):
    if ty == "table":
        try:
            response = dynamodb_client.describe_table(TableName=tbName)
            return response
        except dynamodb_client.exceptions.ResourceNotFoundException:
            return False
    if ty == "s3":
        s3 = boto3.client("s3")
        response = s3.list_buckets()
        if len(response["Buckets"]) > 0:
            data = response["Buckets"]
            for i in data:
                if i["Name"] == tbName:
                    return True
            else: 
                return False
        else:
            return False      

# create music tables
def create_table(ty,tbName):
    if ty == "table":
        table = dynamodb_client.create_table(
            # title, artist, year, web_url, image_url
            TableName=tbName,
            AttributeDefinitions=[
                {"AttributeName": "artist", "AttributeType": "S"},
                {"AttributeName": "title", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "artist", "KeyType": "HASH"},
                {"AttributeName": "title", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        return table
    else:
        return False

# create bucket
def create_bucket(ty,tbName):
    if ty == "s3":
        s3_resource = boto3.resource('s3')
        res = s3_resource.create_bucket(Bucket= tbName)
        if res:
            if res.name == tbName:
                return "true"
            else:
                return False
        else:
            return False
    return False


# get all the users
def get_users_data():
    table = dynamodb.Table("login")
    response = table.scan()
    if response["Count"]:
        items = response["Items"]
        data = []
        for item in items:
            data.append({"email": item["email"], "user_name": item["user_name"]})
        return data
    else:
        return False


# upload json data
def upload_data(jsondata):
    songs = jsondata["songs"]
    table = dynamodb.Table("music")
    for song in songs:
        title = song["title"]
        year = int(song["year"])
        artist = song["artist"]
        web_url = song["web_url"]
        img_url = song["img_url"]
        data = {
            "title": title,
            "year": year,
            "artist": artist,
            "web_url": web_url,
            "img_url": img_url,
        }
        response = table.put_item(Item=data)
        if (int(response["ResponseMetadata"]["HTTPHeaders"]["content-length"]) > 0) & (
            response["ResponseMetadata"]["HTTPStatusCode"] == 200
        ):
            msg = "true"
        else:
            msg = "false"
    return msg


# collect images from url
def collect_images_data():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    if response["Buckets"]:
        imageUrlList = get_images_list()
        staticFolder = ((Path(__file__).resolve().parent.parent))
        imgSavePath = (str(staticFolder)+'/static/images/singers')
        try:
            for imageUrl in imageUrlList:
                response = requests.get(imageUrl,stream = True)
                imgName = ((imageUrl.split('/'))[-1])
                imgData = os.path.join(imgSavePath,imgName)
                file = open(imgData, 'wb')
                file.write(response.content)
                file.close()
            return upload_file()
        except ClientError as e:
                return False
    else:
        return "false"
# get images list 
def get_images_list():
    table = get_table_data("music")
    if table:
        imgList = []
        for img in table:
            imgList.append(img['img_url'])
        if(len(imgList)>0):
            staticFolder = ((Path(__file__).resolve().parent.parent))
            imgSavePath = (str(staticFolder)+'/static/images/singers')
            if(os.path.exists(imgSavePath) != True):
                os.mkdir(imgSavePath)
            return imgList
        else:
            return False
    else:
        return False
# scan table
def get_table_data(tbName):
    table = dynamodb.Table(tbName)
    response = table.scan()
    if response["Count"]:
        items = response["Items"]
        data = []
        for item in items:
            # data.append({"email": item["email"], "user_name": item["user_name"]})
            data.append(
                {
                    "title": item["title"],
                    "artist": item["artist"],
                    "web_url": item["web_url"],
                    "img_url": item["img_url"],
                    "year": int(item["year"]),
                }
            )
        return data
    else:
        return False


# register user
def register_user(data):
    p = make_password(data["ps"])
    em = data["email"]
    nm = data["nm"]
    table = dynamodb.Table("login")
    try:
        response = table.get_item(
            Key={
                "email": em,
            }
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        if "Item" in response:
            return "User Already exists"
        else:
            # add user
            response = table.put_item(
                Item={"email": em, "user_name": nm, "password": p}
            )
            if "ResponseMetadata" in response:
                return "User Added"
            else:
                return False


# login user
def login_user(data):
    table = dynamodb.Table("login")
    p = data["ps"]
    em = data["email"]
    try:
        response = table.get_item(
            Key={
                "email": em,
            }
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        if "Item" in response:
            resp = check_password(p, response["Item"]["password"])
            if resp:
                return response["Item"]
            else:
                return False
        else:
            return False


# query data
def query_data(data):
    table = dynamodb.Table("music")
    artist = data["artist"].title()
    if "title" in data:
        title = data["title"].title()
        response = table.query(
            KeyConditionExpression=Key("artist").eq(artist)
            & Key("title").begins_with(title)
        )
    else:
        response = table.query(KeyConditionExpression=Key("artist").eq(artist))
    if response["Count"]:
        items = response["Items"]
        data = []
        for item in items:
            # data.append({"email": item["email"], "user_name": item["user_name"]})
            data.append(
                {
                    "title": item["title"],
                    "artist": item["artist"],
                    "web_url": item["web_url"],
                    "img_url": item["img_url"],
                    "year": int(item["year"]),
                }
            )
        return data
    else:
        return False


# if __name__ == "__main__":
#     s3_resource = boto3.resource('s3')
#     res = s3_resource.create_bucket(Bucket= 'rominabucket')

#     print(res)


# upload to s3 bucket
def upload_file():
    s3_client = boto3.client('s3')
    staticFolder = ((Path(__file__).resolve().parent.parent))
    imgSavePath = (str(staticFolder)+'/static/images/singers')
    imgList = os.listdir(imgSavePath)
    response = False
    try:
        for img in imgList:
            imgData = os.path.join(imgSavePath,img)
            response = s3_resource.Object('romibucket',img).upload_file(Filename=imgData)
        return "uploaded"
    except ClientError as e:
        return False




#subscribe song
def subscribe_song(data):
    table = dynamodb.Table("subscribe")
    uId = data['uId']
    songId = data['songId']
    artist = data['artist']
    response = table.query(
            KeyConditionExpression=Key("uId").eq(uId)
    )
    if(response['Count']==0):
        response = table.put_item(
                Item={"uId": uId, "songList": [{'songId':songId, 'artist':artist}],}
            )
    else:
        sl = response['Items'][0]['songList']
        i = 0
        ind = -1
        for item in sl:
            if(item['songId'] == songId):
                ind = i
                break
            i = i+1
        if(ind == -1):
            result = table.update_item(
                Key={
                    'uId': uId,
                    },
                UpdateExpression="SET songList = list_append(songList, :i)",
                ExpressionAttributeValues={
                        ':i': [{"songId":songId,"Artist":artist}],
                },
                    ReturnValues="UPDATED_NEW"
            )
            if result['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Attributes' in result:
                return "sub"
        else:
            result = table.update_item(
                Key={
                    'uId': uId,
                    },
                UpdateExpression='REMOVE songList['+str(ind)+']',
                ReturnValues="UPDATED_NEW"
            )
            if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                return "unsub"
    return 'sub'


def get_sub_list(id):
    uId = id
    table = dynamodb.Table("subscribe")
    response = table.query(
            KeyConditionExpression=Key("uId").eq(uId)
    )
    if(response['Count']>0):
        return response['Items'][0]['songList']
    else:
        return False
if __name__ == "__main__":
    pass    
