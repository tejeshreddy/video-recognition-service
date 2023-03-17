# smart-classroom-face-recognition
Developing a smart classroom assistant for educators as part of CSE 546 project.



aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 704676190155.dkr.ecr.us-east-1.amazonaws.com    

aws ecr create-repository --repository-name smart-classroom --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE


docker tag  smart-classroom:latest 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
docker push 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest


aws lambda create-function \
--function-name smart-classroom-function \
--region us-east-1 \
--code ImageUri=704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest \
--role arn:aws:iam::704676190155:role/cc-project-2-lambda-access \
--handler lambdaHandler \
--runtime python3.9


aws lambda create-function \
--function-name smart-classroom-function \
--region us-east-1 \
--code ImageUri=704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest \
--role arn:aws:iam::704676190155:role/cc-project-2-lambda-access \
--package-type Image
