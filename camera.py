import cv2 as cv

def get_camera():
    cam = cv.VideoCapture(0)

    frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {frame_width}x{frame_height}")

    while(1):
        _, frame = cam.read()
        cv.imshow("CAMERA", frame)
        if cv.waitKey(1) == ord('q'):
            break
        if cv.waitKey(32) == ord(' '):
            print("Photo taken")
            cv.imwrite("\\hackathon\\food.jpg",frame)
    cam.release()
    cv.destroyAllWindows()
