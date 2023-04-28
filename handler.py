from boto3 import client as boto3_client
import face_recognition
import pickle
import json
import cv2
import face_recognition
import numpy as np
import pickle
import boto3

print("Imports done")

input_bucket = "input-bucket-vid"
output_bucket = "output-bucket-vids"

input_notification_queue = "https://sqs.us-east-1.amazonaws.com/595548125787/input-notification"
output_notification_queue = "https://sqs.us-east-1.amazonaws.com/595548125787/output-notification"

known_face_names = []
known_face_encodings = []
unknown_image = np.load("encoding", allow_pickle=True)
print("loaded encoding")

known_face_names = unknown_image['name']
known_face_encodings = unknown_image['encoding']

# Function to read the 'encoding' file

def upload_output_to_s3(filename, contents):
	with open('/tmp/' + filename, "w") as fp:
		fp.write(",".join(contents))
	
	s3_client = boto3_client('s3')

	s3_client.upload_file(
		Filename='/tmp/' + filename,
		Bucket=output_bucket,
		Key=filename
	)
	print(filename +" uploaded to s3")

def get_item_ddb(key):
	dynamodb_client = boto3_client('dynamodb', region_name="us-east-1")
	response = dynamodb_client.get_item(
    TableName="student-table",
    Key={
        'name': {'S': key}
    })
	item = response['Item']
	return [item['name']['S'], item['major']['S'], item['year']['S']]

def get_name(event):
	try:
		name = ""
		print(event)
		print(type(event))
		event = json.loads(event)
		file_name = event['Records'][0]['s3']['object']['key'].split(".")[0]
		print(file_name)
		event_type = event['Records'][0]['eventName']
		print(event_type)
		video_link = "https://input-bucket-vid.s3.amazonaws.com/" + event['Records'][0]['s3']['object']['key']

		print(event_type)
		print(video_link)

		if event_type == "ObjectCreated:Put":
			print("In event")
			print(event_type)
			print(video_link)
			video = cv2.VideoCapture(video_link)
			ret, frame = video.read()
			rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			face_locations = face_recognition.face_locations(rgb_frame)
			frame_count = 1
			while True:
				ret, frame = video.read()
				if not ret:
					break

				rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				face_locations = face_recognition.face_locations(rgb_frame)
				if len(face_locations) > 0:
					top, right, bottom, left = face_locations[0]
					face_image = rgb_frame[top:bottom, left:right]
					face_encodings = face_recognition.face_encodings(rgb_frame, [face_locations[0]])
					if len(face_encodings) > 0:
						match_results = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
						matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
						if True in matches:
								first_match_index = matches.index(True)
								name = known_face_names[first_match_index]
						else:
								name = ""

						if match_results[0]:
							break;
						else:
							break;
					else:
						pass
				else:
					pass

				frame_count += 1

			video.release()
			cv2.destroyAllWindows()
			return name, file_name
	except Exception as e:
		print(e)

def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def get_and_delete_sqs_message(queue_url):
    """
    This function is not used
    Get and delete one message from an SQS queue.
    
    Args:
        queue_url (str): The URL of the SQS queue.
        
    Returns:
        dict: The message that was retrieved from the queue, including its attributes.
    """
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return message
    else:
        return None

def send_sqs_message(queue_url, message_body):
    """
    Send a message to an SQS queue.
    
    Args:
        queue_url (str): The URL of the SQS queue.
        message_body (str): The body of the message to send.
        
    Returns:
        dict: The response from the SQS API after the message is sent.
    """
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response


def face_recognition_handler(event, context):
	try:
		if event != None:
			name, file_name = get_name(event)
			upload_content = get_item_ddb(name)
			upload_output_to_s3(filename=file_name, 
					contents=upload_content)
			upload_content.append(file_name)
			print(upload_content)
			send_sqs_message(output_notification_queue, ",".join(upload_content))

	except Exception as e:
		print("Exception Occured")
		print(e)
	return {
        'headers': {'Content-Type' : 'application/json'},
        'statusCode': 200,
        'body': json.dumps({"message": "All services completed"})
    }

