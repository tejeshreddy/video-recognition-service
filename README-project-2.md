# Cloud Computing Project 2

Group Project 2: PaaS

## Overview

1. A workload uploads a file to an S3 bucket. This could be done through the AWS Management Console or through an API call.
2. S3 detects the file upload and sends an event notification to an SQS queue. This event contains information about the file that was uploaded, such as its name and location in the S3 bucket.
3. OpenStack code periodically polls the SQS queue to check its length. If the length is greater than 0, it invokes a Lambda function and passes the event from the queue as an argument to the function.
4. The Lambda function receives the event and processes it by querying the DyanmoDB for the user information. This output is later uploaded to S3 as a text file which has the output information from the function as CSV file. And, also upload the same output to the output queue
5. The OpenStack VM periodically polls the output SQS queue to check for new messages. When a new message is received, the VM writes the output event to a file on the disk.

## Group Members and Task

## AWS Credentials and Accesses

- ECR Details
  - Region: us-east-1
  - URI: `704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom`
  - ECR Push Commands
  
    ```Retrieve an authentication token and authenticate your Docker client to your registry.
    Use the AWS CLI:

    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 704676190155.dkr.ecr.us-east-1.amazonaws.com
    
    Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.
    
    Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

    docker build -t smart-classroom .
    After the build completes, tag your image so you can push the image to this repository:

    docker tag smart-classroom:latest 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
    Run the following command to push this image to your newly created AWS repository:

    docker push 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
    ```

- Lambda Details
  - Region: us-east-1
  - Function ARN: `arn:aws:lambda:us-east-1:704676190155:function:smart-classroom`
  - Architecture: arm64
  - ENTRYPOINT: `/entry.sh`
  - CMD: `handler.face_recognition_handler`
  - WORKDIR: `/home/app/`

- DyanmoDB Details
  - Region: us-east-1
  - Function Name: student_table
  - ARN: `arn:aws:dynamodb:us-east-1:704676190155:table/student_table`

## Resources

- <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html>
- <https://www.serverless.com/framework/docs/providers/aws/cli-reference/deploy>
- <https://docs.openstack.org/networking-ovn/latest/contributor/testing.html>