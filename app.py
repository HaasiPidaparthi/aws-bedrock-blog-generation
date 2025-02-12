import streamlit as st
import requests
import json

# API Gateway URL for invoking the Lambda function
API_URL = "https://XXXXXXXXXX.execute-api.us-east-1.amazonaws.com/dev/blog-generation"

# Streamlit UI
st.title("📝 AI-Powered Blog Generator")
st.write("Generate high-quality blogs using AWS Bedrock.")

# User Input
topic = st.text_input("Enter Blog Topic", placeholder="Example: Future of AI")
word_count = st.slider("Select Word Count", min_value=100, max_value=1000, step=50, value=250)
style = st.selectbox("Select Writing Style", ["Formal", "Casual", "Technical", "Storytelling"])
tone = st.selectbox("Select Tone", ["Neutral", "Positive", "Informative", "Engaging"])

# Submit Button
if st.button("Generate Blog"):
    if not topic:
        st.error("Please enter a blog topic!")
    else:
        st.info("Generating your blog... Please wait.")
        
        # Prepare API request payload
        payload = {
            "topic": topic,
            "word_count": word_count,
            "style": style,
            "tone": tone
        }

        # Call API Gateway
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            try:
                response_data = json.loads(response.text)  # Ensure response is parsed as JSON
                print(response_data)
                generated_blog = response_data.get("blog_content", "No content generated.")
            except json.JSONDecodeError:
                st.error("Error: Failed to parse API response. Check the API output.")
                generated_blog = "No content generated."
            # Display the blog
            st.subheader("📝 Generated Blog:")
            st.write(generated_blog)
            
            # Provide download option
            st.download_button("Download Blog", generated_blog, file_name="generated_blog.txt")
        else:
            st.error(f"Failed to generate blog. Error: {response.text}")

