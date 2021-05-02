# Importing required libraries, obviously
import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image


# Loading pre-trained parameters for the cascade classifier
try:
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Face Detection
    classifier =load_model('Final_model.h5')  #Load model
    emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']  # Emotion that will be predicted
except Exception:
    st.write("Error loading cascade classifiers")


def detect():
    '''
    Function to detect emotions of faces passed to this function.
    '''
    cap = cv2.VideoCapture(0)
    #print("WebCam is Working.Proceed")
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)
    #print("WebCam is Working.Proceed")
    if not cap.isOpened():
    #print("WebCam isnot Working.")
        raise IOError("Cannot use webcam")
    while True:
        _, frame = cap.read()
        labels = []
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)  ##Face Cropping for prediction



            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0) ## reshaping the cropped face image for prediction

                prediction = classifier.predict(roi)[0]   #Prediction
                label=emotion_labels[prediction.argmax()]
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)   # Text Adding
            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow('Emotion Detector',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    


def about():
	st.write(
		'''
		**Haar Cascade** is an object detection algorithm.
		It can be used to detect objects in images or videos.
        
		The algorithm has four stages:
            
			1. Haar Feature Selection
            
			2. Creating  Integral Images
            
			3. Adaboost Training
            
			4. Cascading Classifiers
            
Read more :
    point_right: 
        https://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html
https://sites.google.com/site/5kk73gpu2012/assignment/viola-jones-face-detection#TOC-Image-Pyramid
		''')


def main():
    
    activities = ["Introduction","Home", "Check Camera","About","Contact Us"]
    choice = st.sidebar.selectbox("Pick something Useful", activities)
    

    if choice == "Home":
        html_temp = """
    <body style="background-color:red;">
    <div style="background-color:teal ;padding:10px">
    <h2 style="color:white;text-align:center;">Face Emotion Recognition WebApp</h2>
    </div>
    </body>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        st.title(":angry::dizzy_face::fearful::smile::pensive::open_mouth::neutral_face:")
        st.write("**Using the Haar cascade Classifiers**")
        st.write("Go to the About section from the sidebar to learn more about it.")
        st.write("**Instructions while using the APP**")
        st.write('''
                 1. Click on the Proceed button to start.
                 
                  2. WebCam window will open with a name of Emotion Detector automatically.If not found then, Have a look at the Taskbar.
                  
                  3. Make sure that camera shouldn't be used by any other app.
                  
                  4. Press "q" key to end the webcam window.
                  
                  5. Still webcam window didnot open,  go to Check Camera from the sidebar.''')
        
        if st.button("Proceed"):
            detect()
    
    
    elif choice == "Check Camera":
        html_temp = """
    <body style="background-color:red;">
    <div style="background-color:teal ;padding:10px">
    <h2 style="color:white;text-align:center;">Check Webcam is working or not</h2>
    </div>
    </body>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        st.write("**Instructions while Checking Camrea**")
        st.write('''
                  1. Tick on  Run  to start.
                 
                  2. If get "Cannot use webcam " error, Then Change your webcam number from System Setting.
                  
                  3. Untick on  Run  to end.
                  
                  4. Still webcam window didnot open,  Contact Us.''')
        
        
        
        
        if st.checkbox('Run'):
            
            
            FRAME_WINDOW = st.image([])
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                cap = cv2.VideoCapture(1)
                
            if not cap.isOpened():
                raise IOError("Cannot use webcam")
                ## Opening webcam 

            while True:
                _, frame = cap.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(frame)
        
    elif choice == "About":
        
        html_temp = """
    <body style="background-color:red;">
    <div style="background-color:teal ;padding:10px">
    <h2 style="color:white;text-align:center;">Haar Cascade Object Detection</h2>
    </div>
    </body>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        about()
    elif choice=="Contact Us":
        with st.form(key='my_form'):
            text_input = st.text_input(label='Enter some text')
            submit_button = st.form_submit_button(label='Submit')
        st.write('''
                  Email:- soumya1999rta@gmail.com.
                 
                  Linkedin:-https://www.linkedin.com/in/soumya-ranjan-mishra-715674180/
                  
                  ''')
        
        html_temp = """
    <body style="background-color:red;">
    <div style="background-color:teal ;padding:0.25px">
    <h2 style="color:white;text-align:center;">Copyright © 2021 | Soumya Ranjan Mishra </h2>
    </div>
    </body>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
    elif choice=="Introduction":
         html_temp = """
    <body style="background-color:red;">
    <div style="background-image: url('https://images.unsplash.com/photo-1542281286-9e0a16bb7366');padding:150px">
    <h2 style="color:red;text-align:center;">YOUR EMOTION REFLECTS YOUR PERSONALITY.</h2>
    <h2 style="color:white;text-align:center;">To Know your emotion proceed to Home from the side bar.</h2>
    </div>
    </body>
        """
         st.markdown(html_temp, unsafe_allow_html=True)
        
        
  

if __name__ == "__main__":
    main()

