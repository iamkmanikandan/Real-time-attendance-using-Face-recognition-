import cv2

# Load the JPEG image
img = cv2.imread('resource/mode/4.jpg')

# Resize the image to 414x633 pixels
imgResized = cv2.resize(img, (414, 633))

# Change the color depth of the image to 32-bit color
# imgResized = cv2.cvtColor(imgResized, cv2.COLOR_BGR2RGBA)

# Save the image as a PNG file
cv2.imwrite('4.png', imgResized)
