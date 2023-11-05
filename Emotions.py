import boto3
import cv2

client = boto3.client('rekognition')

def lambda_handler(event, context):

    s3_bucket_name = 'face-detection-vid'
    video_filename = 'AdvaitEmotions.mp4'
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    
    # Download the video from the S3 bucket
    with open('video.mp4', 'wb') as f:
        s3_client.download_fileobj(s3_bucket_name, video_filename, f)
        
    video_capture = cv2.VideoCapture('video.mp4')

    while True:
        # Capture the current frame
        ret, frame = video_capture.read()
    
        if not ret:
            break
    
        # Detect and analyze faces in the frame
        response = client.detect_faces(Image={'Bytes': frame.tobytes()})
        faces = response['FaceDetails']
    
        # Analyze emotions for each detected face
        for face in faces:
            emotions = face['Emotions']
    
            # Extract the most prominent emotion
            most_prominent_emotion = max(emotions, key=lambda emotion: emotion['Confidence'])
            emotion_type = most_prominent_emotion['Type']
            emotion_confidence = most_prominent_emotion['Confidence']
    
            print(f"Emotion: {emotion_type}, Confidence: {emotion_confidence}")
    
    emotion_counts = {}

    for emotion in emotions:
        emotion_type = emotion['Type']
        emotion_confidence = emotion['Confidence']
    
        if emotion_type not in emotion_counts:
            emotion_counts[emotion_type] = 0
    
        emotion_counts[emotion_type] += emotion_confidence
        
    most_prominent_emotion = max(emotion_counts, key=lambda emotion: emotion_counts[emotion])
    overall_mood = most_prominent_emotion
    
    print(f"Overall Mood: {overall_mood}")
