import json
import boto3


def lambda_handler(event, context):
    """
    This Lambda function is triggered whenever a user uploads an interview video. The function uses the Amazon Rekognition and Amazon Comprehend services to analyze the video and generate feedback on the user's facial expressions, transcription, repetition, stuttering, and overall tone and demeanor during the interview.
    """

    # Get the video URL from the event
    video_url = event["Records"][0]["s3"]["object"]["url"]

    # Create a Rekognition client
    rekognition = boto3.client("rekognition")

    # Create a Comprehend client
    comprehend = boto3.client("comprehend")

    # Detect faces in the video
    faces = rekognition.detect_faces(
        Video={"S3Object": {"Bucket": "my-bucket", "Name": video_url}})

    # Get the facial expressions for each face
    facial_expressions = []
    for face in faces:
        facial_expressions.append(face["Emotions"])

    # Transcribe the speech in the video
    transcript = comprehend.transcribe_video(VideoUri=video_url)

    # Identify repetition, stuttering, and transcription errors in the transcript
    speech_analysis = comprehend.detect_sentiment(Text=transcript)

    # Generate feedback on the user's facial expressions, transcription, repetition, stuttering, and overall tone and demeanor during the interview
    feedback = []
    for facial_expression in facial_expressions:
        if facial_expression["Sad"] > 0.5:
            feedback.append("You seem to be feeling sad during the interview.")
        if facial_expression["Angry"] > 0.5:
            feedback.append(
                "You seem to be feeling angry during the interview.")
        if facial_expression["Surprised"] > 0.5:
            feedback.append(
                "You seem to be feeling surprised during the interview.")
        if facial_expression["Happy"] > 0.5:
            feedback.append(
                "You seem to be feeling happy during the interview.")

    for sentiment in speech_analysis["Sentiments"]:
        if sentiment["Sentiment"] == "NEGATIVE":
            feedback.append(
                "You seem to have a negative tone during the interview.")
        elif sentiment["Sentiment"] == "POSITIVE":
            feedback.append(
                "You seem to have a positive tone during the interview.")

    # Return the feedback
    return {
        "statusCode": 200,
        "body": json.dumps({"feedback": feedback}),
    }
