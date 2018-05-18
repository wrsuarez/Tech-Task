# Tech-Task

Implementation Steps:
- Clone the repo locally
- Upload the process_file.zip file from the dependencies directory to a holding bucket
- Deploy the Cloudformation template inputting the bucket name where you uploaded the zip file
- In the keywords bucket upload the Keywords.txt file from the dependencies directory
- In the API Gateway confirm/reset the Body Mapping for the Integration request. This should be generated from the Method Request Passthrough template
- Make any other adjustments desired and deploy the API to a new stage

API Request Header Requirements:
- x-api-key: Valid API Key
- x-requester: username of the submitter
- Content-Type: multipart/form-data

- API Method: POST
- Body: binary (file upload)

Known Limitations:
- Max text file size: 10MB
- Max execution time: 5 minutes
