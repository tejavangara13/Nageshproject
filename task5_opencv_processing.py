import cv2
import numpy as np

def enhance_image(image):
    """Enhances image contrast and detects edges."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # 2. Canny Edge Detection
    edges = cv2.Canny(enhanced, 100, 200)
    
    return enhanced, edges

def detect_faces(image):
    """Detects faces and eyes using OpenCV Haar Cascades."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    output = image.copy()
    for (x, y, w, h) in faces:
        # Draw green bounding box around face
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(output, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Region of Interest for eyes
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = output[y:y + h, x:x + w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
        for (ex, ey, ew, eh) in eyes:
            # Draw blue box around eyes
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
            
    return output, len(faces)

def run_webcam_detection():
    """Applies real-time face detection from the webcam (Press 'q' to exit)."""
    cap = cv2.VideoCapture(0)
    print("Starting webcam... Press 'q' in the video window to quit.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        processed_frame, count = detect_faces(frame)
        cv2.putText(processed_frame, f"Faces Detected: {count}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("OpenCV Real-Time Face Detection", processed_frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Choose mode:
    # 1. Run real-time webcam detection:
    run_webcam_detection()
    
    # 2. To test with a static image instead, comment above and uncomment below:
    # img = cv2.imread("test_image.jpg")
    # if img is not None:
    #     enhanced, edges = enhance_image(img)
    #     detected_img, count = detect_faces(img)
    #     cv2.imshow("Detected Faces", detected_img)
    #     cv2.imshow("Edges", edges)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()