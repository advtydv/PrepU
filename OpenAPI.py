import openai 
import os

def lambda_handler(event, context):
    openai.api_key = os.getenv('API_KEY')
    location = "New York, NY"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Tell me an interesting fact about {location} in less than 200 characters"}
    ]
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    gpt_response = chat.choices[0].message.content
    print("GPT response: ", gpt_response)
    return {
        "statusCode": 200,
        "body": gpt_response
    }

# Example usage:
# Set your OpenAI API key in the environment variable API_KEY before invoking this function.
# You can test the lambda_handler function by calling it with any test event, as the event data is not used in this function.
