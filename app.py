import boto3
import botocore.config
import json
from datetime import datetime
import traceback

def blog_generation(topic:str) -> str:
    prompt = f"""<s>[INST]Human: Write a 250 word blog on the topic {topic}
    Assistant: [/INST]
    """ 
    body = {
        "prompt": prompt,
        "top_p": 0.9,
        "temperature":0.6
    }

    try:
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1",
                             config=botocore.config.Config(read_timeout=300, retries={'max_attempts':3}))
        
        model_id = "arn:aws:bedrock:us-east-1:XXXXXXXXXXXX:inference-profile/us.meta.llama3-2-1b-instruct-v1:0"
        response = bedrock.invoke_model(
            body=json.dumps(body), 
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        print(response_data)
        if 'outputs' in response_data and len(response_data['outputs']) > 0:
            blog_details = response_data['outputs'][0]['text']
        else:
            blog_details = "No response generated."
        return blog_details
    
    except Exception as e:
        print(f"Error generating the blog for topic '{topic}': {str(e)}")
        print(traceback.format_exc())  # Logs full error details
        return ""
    
def save_blog_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = generate_blog )
        print("Code saved to s3")
    except Exception as e:
        print("Error when saving the code to s3")

def lambda_handler(event, context):
    event = json.loads(event['body'])
    blogtopic = event['topic']
    generate_blog = blog_generation(topic=blogtopic)

    if generate_blog:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'aws-bedrock-blog-generation'
        save_blog_s3(s3_key,s3_bucket,generate_blog)
    else:
        print("No blog was generated")

    return {
        'statusCode':200,
        'body':json.dumps('Blog Generation is completed')
    }
