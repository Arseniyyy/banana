import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
i = 1
delta_time = 0
#W = 400
img_size = [80, 80]
cap = cv.VideoCapture(0)
x = []
y = []
t = 0
ret, frame = cap.read()
frame = cv.resize(frame, (img_size[1], img_size[0]))
prvs = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
#hsv = np.zeros_like(frame1)
#hsv[...,0] = 255
#hsv[...,1] = 255
# Create black empty images
#size = W, W, 3
#rook_image = np.zeros(size, dtype=np.uint8)
#rook_window = "Drawing 2: Rook"
def my_line(img, start, end):
     thickness = 2
     line_type = 8
     cv.line(img,
              start,
              end,
              (255, 0, 0),
              thickness,
              line_type)
def my_line_red(img, start, end):
     thickness = 2
     line_type = 8
     cv.line(img,
              start,
              end,
              (255, 255, 0),
              thickness,
              line_type)

 #####Initialize the plot#####
fig = plt.figure()
ax1 = fig.add_subplot() #Set up basic plot attributes


plt.ion() #Set interactive mode

i=0 #initialize counter variable (this will help me to limit the number of points displayed on graph
while True:
    start_time = time.time()
    ret, frame = cap.read()

    frame2 = cv.resize(frame, (img_size[1], img_size[0]))

    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    
    
    flow = cv.calcOpticalFlowFarneback(prvs,next, None, 0.5, 1, 15, 1, 5, 1.2, 0)
    
    # mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])
    # hsv[...,2] = ang*180/np.pi/2
    # hsv[...,2] = cv.normalize(mag,None,100,255,cv.NORM_MINMAX)
    # bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    # cv.imshow('frame2',bgr)
    #a = np.ma.array(flow[...,1])
    dvx = -np.ma.average(flow[...,0])
    dvy = -np.ma.average(flow[...,1])
    my_line(rook_image, (200, 200), (200+int((500*dvx)//10), 200+int((500*dvy)//10)))
    my_line(rook_image, (200, 200), (200, 200+int((500*dvy)//10)))
    my_line_red(rook_image, (200, 200), (200+int((500*dvx)//10), 200))
    if i>1:
        
       rook_image = np.zeros(size, dtype=np.uint8)
       cv.imshow(rook_window, rook_image)
       i=0
       cv.imshow(rook_window, rook_image)
       cv.moveWindow(rook_window, W, 200)
       i+=1
       k = cv.waitKey(30) & 0xff
    if k == 27:
       break
    elif k == ord('s'):
       cv.imwrite('opticalfb.png',frame2)
       cv.imwrite('opticalhsv.png',bgr)
    prvs = next


    x.append(t)
    y.append(dvy)
    i+=1

    if t>10:
        break
    print(dvy, delta_time, t)
    delta_time = time.time() - start_time
    if t > 10:  # Limit displayed points to save memory (hopefully...)
        del ax1.lines[0]  # After 300 points, start deleting the first point each time
    else:
        i += 1
    if dvy > 2:  # Plot green points if current is above threshold
        ax1.plot(t, dvy, marker='o', linestyle='--', c='g')
    else:  # Plot red points if current has fallen off
        ax1.plot(t, dvy, marker='o', linestyle='--', c='r')
    plt.axis([0, 10, None, None])  # Set xmin/xmax to limit displayed data to a reasonable window
    plt.draw()
    time.sleep(2)  # Update every 2 seconds
    delta_time = time.time() - start_time
    t += delta_time
cap.release()
cv.destroyAllWindows()
