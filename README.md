# Cloud Computing Project 2

Group Project 2: PaaS

## Overview

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

- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- https://www.serverless.com/framework/docs/providers/aws/cli-reference/deploy
