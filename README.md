# Blog Generation using AWS Bedrock

## 🚀 Overview
This project enables AI-powered blog generation using AWS Bedrock, AWS Lambda, API Gateway, and S3. Users provide a topic, and the system generates a structured blog, storing it in an S3 bucket for later access.

## 📌 Features
* **Automated Blog Generation**: Uses AWS Bedrock (Llama 3) to generate a customizable blog.
* **Customizable Writing**: Users can specify word count, writing style (formal, casual, technical, storytelling), and tone (neutral, positive, informative, engaging).
* **Serverless Architecture**: Implemented using AWS Lambda and API Gateway.
* **Storage on S3**: Blogs are saved in an S3 bucket for retrieval.
* **API-based Interaction**: Trigger blog generation via a POST request with user-defined parameters.
* **Streamlit Frontend**: A user-friendly web UI to interact with the API and generate blogs visually.

## 🏗️ Architecture
![architecture diagram](https://github.com/HaasiPidaparthi/aws-bedrock-blog-generation/blob/main/architecture_diagram.png)

1. **Streamlit Frontend**: Users input blog parameters via a web UI.
2. **API Gateway**: Receives HTTP POST requests containing blog topic, word count, style, and tone.
3. **AWS Lambda**: Processes the request, calls AWS Bedrock, and generates structured blog content.
4. **AWS Bedrock**: Uses Llama 3 to generate the blog based on the provided parameters.
5. **AWS S3**: Stores the generated blog in a structured format.
6. **Response**: The API responds with a success message and posts the blog content on the web UI.

## 📸 Sample Output
![streamlit sample output](https://github.com/HaasiPidaparthi/aws-bedrock-blog-generation/blob/main/sample_output.png)
