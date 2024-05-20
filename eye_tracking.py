import cv2

cap=cv2.VideoCapture("eye_recording.mp4")

while True:
    ret,frame=cap.read()
    if (ret==False):
        break

    frame=cv2.resize(frame,(800,600))

    gri=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #kareyi griye çevirdik

    blur=cv2.GaussianBlur(gri,(7,7),0) #köşeleri yumuşatmak için blur

    _,thresh=cv2.threshold(blur,10,200,cv2.THRESH_BINARY_INV) # göz bebeği siyah olduğu için diğer kısımlardan thresh ettim

    contours,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # binary siyah beyaz görüntünün içerisinde ki şekillerin sınırlarını bulmak için kullanılır birbirine bağlı şekillerin ayrı ayrı
    # konturların listesini ve hiyerarşisini belirler

    contours=sorted(contours,key=cv2.contourArea,reverse=True) # bu konturları büyükten küçüğe sıralar

    print(contours)

    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(cnt)

        if area>100:
            (x,y,w,h)=cv2.boundingRect(cnt) #kontuların şekillerini bir diktörgene alır ve bu diktörgenin konumlarını verir
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            cv2.line(frame,(x+int(w/2),0),(x+int(h/2),frame.shape[0]),(0,255,0),2)
            cv2.line(frame,(0,y+int(h/2)),(frame.shape[1],y+int(h/2)),(0, 255, 0), 2)

    cv2.imshow("goz",thresh)
    cv2.imshow("canligoz",frame)

    if cv2.waitKey(5) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()