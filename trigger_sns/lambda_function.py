import json
import boto3
from PIL import Image
import io


def lambda_handler(event, context):
    # TODO implement
    output = [
        {
            "Object Name": record["s3"]["object"]["key"],
            "Object Size": record["s3"]["object"]["size"],
            "Object Type": record.get("s3").get("object").get("key").split(".")[-1],
            "S3 URI": f"s3://{record['s3']['bucket']['name']}/{record['s3']['object']['key']}",
            "Bucket Name":record['s3']['bucket']['name']
        }
        for record in event["Records"]
    ]
    print(output)


    if output[0]['Object Type'] in ('png', 'jpg', 'jpeg'):
        s3 = boto3.client('s3')
        image = Image.open(s3.get_object(Bucket = output[0]['Bucket Name'], Key = output[0]['Object Name'])['Body'])
        in_mem_file = io.BytesIO()
        size = (100, 100)
        image.thumbnail(size)
        image.save(in_mem_file,format=image.format)
        in_mem_file.seek(0)
        s3.upload_fileobj(in_mem_file,Bucket=output[0]['Bucket Name'],Key=f'raw_reduced/{dict(output[0]).get("Object Name").split("/")[-1]}')

    
    sns_client = boto3.client('sns')
    
    sns_client.publish(TopicArn='arn:aws:sns:us-east-1:801355498549:s3_event_notification',Message=json.dumps(output[0]))

    return {"statusCode": 200, "body": json.dumps(output[0])}