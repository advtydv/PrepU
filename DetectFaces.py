import json
import boto3

client = boto3.client('rekognition')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    bucket_name = "face-detection-vid"
    file_name = "Sequence 01.mp4"
    
    response = client.start_face_detection(Video={'S3Object':{'Bucket': bucket_name, 'Name': file_name}}, NotificationChannel={
            'SNSTopicArn': 'arn:aws:sns:us-west-1:542634396410:test-sns',
            'RoleArn': 'arn:aws:iam::542634396410:role/service-role/DetectFaces-role-0ltn15t8'
        })
    
    job_id = response['JobId']
    
    sns_client.publish(
        TopicArn='arn:aws:sns:us-west-1:542634396410:test-sns',
        Message=json.dumps({'JobId': job_id}),
        Subject='Rekognition Job Started'
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'JobId': job_id})
    }

