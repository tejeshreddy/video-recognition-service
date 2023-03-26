# Cloud Computing Project 2

Group Project 2: PaaS

## Overview

## Group Members and Task

## AWS Credentials and Accesses

- ECR Details
  - Region: us-east-1
  - URI: 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom

- Lambda Details
  - Region: us-east-1
  - Function ARN: arn:aws:lambda:us-east-1:704676190155:function:smart-classroom
  - Architecture: arm64
  - ENTRYPOINT: /entry.sh
  - CMD: handler.face_recognition_handler
  - WORKDIR: /home/app/

- DyanmoDB Details
  - Region: us-east-1
  - Function Name: student_table
  - ARN: arn:aws:dynamodb:us-east-1:704676190155:table/student_table  

## Resources

- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- https://www.serverless.com/framework/docs/providers/aws/cli-reference/deploy
