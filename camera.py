import cv2 as cv

def get_camera():
    cam = cv.VideoCapture(0)

    frame_width = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

    while(1):
        _, frame = cam.read()
        cv.imshow("CAMERA", frame)
        if cv.waitKey(1) == ord('q'):
            break
        if cv.waitKey(32) == ord(' '):
            cv.imwrite("food.jpg",frame)


    cam.release()
    cv.destroyAllWindows()
## hello