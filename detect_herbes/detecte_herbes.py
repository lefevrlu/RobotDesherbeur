import cv2


l = 0.1

# read image from file
Img = cv2.imread("cylindre3.jpg")

# get dimensions
imageHeight, imageWidth, imageChannels = Img.shape

# lire image en HSV
hsv = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)

# interval HSV of green
#(120,100,50)
greenLow = (40, 40,40) #(36,0,0) 
greenUp = (70, 255,255) #(86,255,255) 

#construct a mask
mask = cv2.inRange(hsv, greenLow, greenUp)

#Contours
contours= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

#choisir le contoure a le plus grand surface
contour = max(contours, key = cv2.contourArea)

cv2.drawContours(Img, [contour], -1, 255, -1)

cv2.imwrite('detectee.png',Img)

M = cv2.moments(contour)
center  = (M["m10"]/M["m00"],M["m01"]/M["m00"])
area = cv2.contourArea(contour)

(x, y, w, h) = cv2.boundingRect(contour)
print((x, y, w, h))

