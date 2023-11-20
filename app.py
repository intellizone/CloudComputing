import json
import boto3
import matplotlib.image as image

def lambda_handler(event, context):
    print("Event triggered this function...")
    client = boto3.client('sns')
    objName = event['Records'][0]['s3']['object']['key']
    objSize = event['Records'][0]['s3']['object']['size']/1024/1024
    response = client.publish(
    TopicArn= 'arn:aws:sns:us-east-1:169345577104:s3Mail',
    Message= json.dumps({
        "S3 Uri": f's3://{event["Records"][0]["s3"]["bucket"]["name"]}/{objName}',
        "Object Name": objName,
        "Object Size": f'{objSize:.4f} MB',
        "Object Type": objName.split('.')[-1]
    }),
    Subject='File Upload notify'
    )
    print(json.dumps({
        "S3 Uri": f's3://{event["Records"][0]["s3"]["bucket"]["name"]}/{objName}',
        "Object Name": objName,
        "Object Size": f'{objSize:.4f} MB',
        "Object Type": objName.split('.')[-1]
    }))
    if objName.split('.')[-1] in ['jpg','jpeg','png']:
        client = boto3.client('s3')
        client.download_file(event["Records"][0]["s3"]["bucket"]["name"], objName, f'/tmp/{objName}')
        print("download complete")
        
        fig = image.thumbnail(f'/tmp/{objName}', f'/tmp/{objName}', scale=0.15)
        print("thumbnail created")
        response = client.upload_file(f'/tmp/{objName}',event["Records"][0]["s3"]["bucket"]["name"],objName)
    print("push success")
    return response
