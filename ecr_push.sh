aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 704676190155.dkr.ecr.us-east-1.amazonaws.com
docker build -t smart-classroom .
docker tag smart-classroom:latest 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
docker push 704676190155.dkr.ecr.us-east-1.amazonaws.com/smart-classroom:latest
