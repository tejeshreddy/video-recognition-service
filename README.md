# Cloud Computing Project 3

Group Project 3: Hybrid Cloud

## Overview
In our implementation, a user is asked to upload an MP4 file. The video is uploaded into an S3 bucket (input-bucket-video). Once the video is uploaded successfully, a Lamba function is triggered. This function is created out of an image containing the face recognition functionality, also known as the Lambda handler function. It extracts a frame from the video and stores it as an image. A facial recognition module is run on this image, which creates an encoding. The encoding is matched with a known encoding file to retrieve the name of the student. Finally, we use this name to query a DynamoDB, which contains all the relevant information of every student. Based on the query, the details retrieved are stored in CSV format and sent to another S3 bucket. This bucket serves as the output bucket (output-bucket-vid).


## Group Members and Task

## AWS Credentials and Accesses

- ECR Details
  - Region: us-east-1
  - URI: `arn:aws:lambda:us-east-1:595548125787:function:smart-classroom`
  - ECR Push Commands
  
    ```Retrieve an authentication token and authenticate your Docker client to your registry.
    Use the AWS CLI:

    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 595548125787.dkr.ecr.us-east-1.amazonaws.com
    
    Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.
    
    Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

    docker build -t smart-classroom .
    After the build completes, tag your image so you can push the image to this repository:

    docker tag smart-classroom:latest 595548125787.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
    Run the following command to push this image to your newly created AWS repository:

    docker push 595548125787.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
    ```

- Lambda Details
  - Region: us-east-1
  - Function ARN: `arn:aws:lambda:us-east-1:595548125787:function:smart-classroom`
  - Architecture: arm64
  - ENTRYPOINT: `/entry.sh`
  - CMD: `handler.face_recognition_handler`
  - WORKDIR: `/home/app/`

- DyanmoDB Details
  - Region: us-east-1
  - Function Name: student_table
  - ARN: `arn:aws:dynamodb:us-east-1:595548125787:table/student-table`

- SQS 
  - input-notification: 
    - URL: https://sqs.us-east-1.amazonaws.com/595548125787/input-notification
  - output-notification
    - URL: https://sqs.us-east-1.amazonaws.com/595548125787/output-notification

- EC2 Instance
  - Instance ID: i-0f53f8d352abdcf0b
  - Public IP: 54.210.6.58
  
- OpenStack VM
  - Image Name: centos
  - IP Address: 172.31.24.229
  - Region: Nova


## Resources

- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- https://www.serverless.com/framework/docs/providers/aws/cli-reference/deploy
