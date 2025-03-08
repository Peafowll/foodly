import cv2 
photo = cv2.VideoCapture(0)

if not photo.isOpened():
    print("cant open")

ret, frame = photo.read()

if ret:
    # Save the image
    cv2.imwrite("verif.jpg", frame)
    print("Photo saved as verif.jpg")

    # Show the image
    cv2.imshow("Captured Image", frame)
    cv2.waitKey(0)  # Wait until a key is pressed

photo.release()
cv2.destroyAllWindows()