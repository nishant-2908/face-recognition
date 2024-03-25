import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
from prettytable import PrettyTable

t = PrettyTable()

t.field_names = [
    "Name",
    "Father Name",
    "DOB",
    "Crime Recorded Date",
    "Type of crime",
    "Remarks",
    "Arrestment/Fine",
    "Completed",
    "Date of Completion",
]
# Directory containing the known persons' images
known_persons_directory = "known_persons/"

# Initialize lists to store face encodings and names
known_face_encodings = []
known_face_names = []
recognized_data = pd.DataFrame()
detected_names = set()
# Initialize variables for face recognition
face_locations = []
face_encodings = []
face_names = []

# Initialize a DataFrame to store recognized names and timestamps
recognized_data = pd.DataFrame(columns=["Name", "Timestamp"])

# Reading the csv
crime_history = pd.read_csv(
    "C:/Users/NISHANT/Desktop/Face_Recognition/crime_history_samples.csv"
)


def image_to_encoding(filename):
    name = os.path.splitext(filename)[0]
    # Load the image and compute the face encoding
    known_image = face_recognition.load_image_file(
        os.path.join(known_persons_directory, filename)
    )
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Append the face encoding and name to the respective lists
    known_face_encodings.append(known_face_encoding)
    known_face_names.append(name)


for filename in os.listdir(known_persons_directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_to_encoding(filename=filename)

# Open the webcam
video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Initialize lists to store recognized face names and confidence scores
    face_names = []
    confidence_scores = []

    # Compare face encodings with known persons
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding, tolerance=0.6
        )
        name = "Unknown"

        # Calculate confidence scores for recognized faces
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding
        )
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        confidence_score = 1 - face_distances[best_match_index]

        face_names.append(name)
        confidence_scores.append(confidence_score)
        person_crime_history = crime_history[crime_history["Name"] == name]
        if (
            not person_crime_history.empty
            and person_crime_history["Punishment Completed"].values[0] == "No"
        ):
            # Check if the name is already detected
            if name not in detected_names:
                t.add_row(
                    name,
                    person_crime_history["Name"].values[0],
                    person_crime_history["Father Name"].values[0],
                    person_crime_history["DOB"].values[0],
                    person_crime_history["Crime recorded Date"].values[0],
                    person_crime_history["Type of crime"].values[0],
                    person_crime_history["Remarks"].values[0],
                    person_crime_history["Arrestment/Fine"].values[0],
                    person_crime_history["Punishment Completed"].values[0],
                    person_crime_history["Date of Completion"].values[0],
                )
                print(t)
                # Add the name to the detected names set
                detected_names.add(name)

    # Draw rectangles, labels, and confidence scores on the frame
    for (top, right, bottom, left), name, confidence_score in zip(
        face_locations, face_names, confidence_scores
    ):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the person's name and confidence score
        label = f"{name} ({confidence_score:.2f})"
        cv2.rectangle(
            frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Check if confidence is greater than 80%
        if confidence_score > 0:
            # Add recognized name and timestamp to the DataFrame
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            df = pd.DataFrame(recognized_data)
            recognized_data = pd.concat(
                [
                    recognized_data,
                    pd.DataFrame({"Name": [name], "Timestamp": [timestamp]}),
                ],
                ignore_index=True,
            )

    recognized_data.to_csv("recognized_data.csv", index=False)

    # Display the frame with rectangles, labels, and confidence scores
    cv2.imshow("Video", frame)

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
