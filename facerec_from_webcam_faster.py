import face_recognition
import cv2
import numpy as np
import os
import time

def recog_procedure(person):

    encodings = []
    names = []

    # Create arrays of known face encodings and their names
    person_path = f'./stored/{person}/'
    person_dir = os.listdir(person_path)

    # Loop through each training image for the current person
    for person_img in person_dir:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file(person_path + person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        # If training image contains exactly one face
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(person)
        else:
            print(person + "/" + person_img + " was skipped and can't be used for training")


    video_capture = cv2.VideoCapture(0)
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    recognized_time = 0.0
    elapsed_time = 0.0
    exit_time = 5.0
    threshold = 3.0
    recon_success = False

    while elapsed_time < exit_time:
        checkpoint = time.time()
        recognized = False
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = names[first_match_index]
                    recognized = True

                # Or instead, use the known face with the smallest distance to the new face
                # face_distances = face_recognition.face_distance(encodings, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                #     name = names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        diff = time.time() - checkpoint
        elapsed_time += diff
        if (recognized):
            recognized_time += diff

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if (recognized_time > threshold):
            recon_success = True
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return recon_success

if __name__ == "__main__":
    print(recog_procedure("201910336"))