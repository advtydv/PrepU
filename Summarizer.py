import json
import boto3

def get_transcription(s3_client, bucket_name, object_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    transcription_data = json.loads(response['Body'].read().decode('utf-8'))
    return transcription_data['results']['transcripts'][0]['transcript']

def invoke_sagemaker_endpoint(endpoint_name, text):
    client = boto3.client('runtime.sagemaker')
    response = client.invoke_endpoint(
        EndpointName=endpoint_name, 
        ContentType='application/x-text', 
        Body=text.encode('utf-8')
    )
    return response

def parse_response(response):
    model_predictions = json.loads(response['Body'].read())
    return model_predictions['summary_text']

def lambda_handler(event, context):
    bucket_name = 'prepudata'
    object_key = 'samplejob.json'

    s3_client = boto3.client('s3')
    sagemaker_endpoint_name = 'jumpstart-dft-hf-summarization-distilbart-xsum-1-1'
    
    try:
        # Fetch transcription from S3
        transcript_text = get_transcription(s3_client, bucket_name, object_key)
        
        # Invoke SageMaker endpoint to get summary
        response = invoke_sagemaker_endpoint(sagemaker_endpoint_name, transcript_text)
        
        # Parse the response and print summary
        summary_text = parse_response(response)
        print(f"Summary: {summary_text}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(summary_text)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps("Error processing the request")
        }
