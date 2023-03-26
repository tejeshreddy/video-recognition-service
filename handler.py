from boto3 import client as boto3_client
import face_recognition
import pickle
import json
import cv2
import face_recognition
import numpy as np
import pickle

print("Imports done")

input_bucket = "input-bucket-video"
output_bucket = "output-bucket-vid"

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
    TableName="student_table",
    Key={
        'name': {'S': key}
    })
	item = response['Item']
	return [item['name']['S'], item['major']['S'], item['year']['S']]

def get_name(event):
	name = ""
	event_type = event['Records'][0]['eventName']
	video_link = "https://input-bucket-video.s3.amazonaws.com/" + event['Records'][0]['s3']['object']['key']

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
				face_encodings = face_recognition.face_encodings(face_image)
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
		return name

def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):	
	name = get_name(event)
	upload_output_to_s3(filename=event['Records'][0]['s3']['object']['key'].split(".")[0], 
		     contents=get_item_ddb(name))
	return {
        'headers': {'Content-Type' : 'application/json'},
        'statusCode': 200,
        'body': json.dumps({"message": "All services completed"})
    }

