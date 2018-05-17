# Tech-Task

Infrastructure Requirements:
- AWS Lambda Function with the Python code in this repo
- API Gateway with a resource and a POST method for the resources
- Binary Support enabled on the API for Content-Type multipart/form-data
- Integration Request Body Mapping for Content-Type multipart/form-data
- API Gateway Integration to the Lambda Function 
- S3 Bucket for Output Files
- S3 Bucket for Keywords Text File
- Dynamo DB Table for tracking API requests

API Request Header Requirements:
- x-api-key: Valid API Key
- x-requester: username of the submitter
- Content-Type: multipart/form-data

API Method: POST
POST Body: binary (file upload)

Known Limitations:
- Max text file size: 10MB
- Max execution time: 5 minutes