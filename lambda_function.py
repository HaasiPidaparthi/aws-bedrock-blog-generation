import boto3
import botocore.config
import json
from datetime import datetime
import traceback

def blog_generation(topic:str, word_count:int, style:str, tone:str) -> str:
    system_prompt = """You are an AI assistant that generates high-quality blogs.
    Your response should be a well-structured blog with an introduction, body, and conclusion.
    - The content must be **strictly relevant** to the given topic.
    - Do **not** include extra formatting, instructions, or metadata.
    - Do **not** repeat system messages or provide multiple responses.
    - Do **not** include XML, Markdown, or HTML comments like <!-- -->.
    - Your response should be **only the blog text**, properly formatted."""

    user_message = f"""
    Write a structured blog on the topic: **{topic}**.
    - Word count: {word_count} words
    - Writing Style: {style}
    - Tone: {tone}

    The blog should be structured as follows:
    **Title:** {topic}
    **Introduction:** A compelling introduction that briefly presents the topic.
    **Body:** A detailed discussion covering key points in an engaging way.
    **Conclusion:** A concise summary wrapping up the key takeaways.

    **Only output the blog text. Do not include system messages, metadata, instructions, or additional formatting.**"""

    prompt = f"""<s>[INST] <<SYS>> {system_prompt} <</SYS>> {user_message} [/INST]"""
    body = {
        "prompt": prompt,
        "top_p": 0.9,
        "temperature":0.6,
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
        if 'generation' in response_data and len(response_data['generation']) > 0:
            blog_details = response_data['generation']
            # Remove any unwanted system messages
            blog_details = blog_details.replace("><[/SYS>[/INST]", "").strip()
            blog_details = blog_details.replace("<INST>", "").replace("</INST>", "").replace("<<SYS>>", "").replace("<</SYS>>", "").strip()
            blog_details = blog_details.replace("<s>[INST]", "").replace("</s>[INST]", "").replace("<</SYS>>", "").strip()
            
            # If duplicate content is present, remove second instance
            first_occurrence = blog_details.find("**Blog:")
            if first_occurrence != -1:
                blog_details = blog_details[:first_occurrence]  # Keep only the first blog
        else:
            blog_details = "No response generated."
        print("blog_details: ", blog_details)
        return blog_details
    
    except Exception as e:
        print(f"Error generating the blog for topic '{topic}': {str(e)}")
        print(traceback.format_exc())  # Logs full error details
        return ""
    
def save_blog_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog )
        print("Code saved to s3")
    except Exception as e:
        print("Error when saving the code to s3")

def lambda_handler(event, context):
    event = json.loads(event['body'])
    print("event: ", event)
    blogtopic = event.get('topic', 'Default AI')
    word_count = event.get('word_count', 250)
    style = event.get('style', 'Formal')
    tone = event.get('tone', 'Neutral')
    generate_blog = blog_generation(topic=blogtopic, word_count=word_count, style=style, tone=tone)

    if generate_blog:
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'aws-bedrock-blog-generation'
        save_blog_s3(s3_key,s3_bucket,generate_blog)
        response_body = {
            'message': 'Blog Generation is completed',
            's3_key': s3_key,
            'blog_content': generate_blog
        }
    else:
        response_body = {'message': 'No blog was generated'}

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response_body)
    }
