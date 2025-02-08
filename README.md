# Blog Generation using AWS Bedrock

## 🚀 Overview
This project enables AI-powered blog generation using AWS Bedrock, AWS Lambda, API Gateway, and S3. Users provide a topic, and the system generates a structured blog, storing it in an S3 bucket for later access.

## 📌 Features
* **Automated Blog Generation**: Uses AWS Bedrock (Llama 3) to generate a 250-word blog.
* **Serverless Architecture**: Implemented using AWS Lambda and API Gateway.
* **Storage on S3**: Blogs are saved in an S3 bucket for retrieval.
* **API-based Interaction**: Trigger blog generation via a POST request.

## 🏗️ Architecture
![architecture diagram](https://github.com/HaasiPidaparthi/aws-bedrock-blog-generation/blob/main/architecture-diagram.png)

* **API Gateway**: Receives HTTP POST requests containing a blog topic.
* **AWS Lambda**: Processes the request, calls AWS Bedrock, and generates content.
* **AWS Bedrock**: Uses Llama 3 to generate the blog based on the provided topic.
* **AWS S3**: Stores the generated blog in a structured format.
* **Response**: The API responds with a success message and S3 location.
