import cv2
import numpy as np

img = cv2.imread('./house.jpg')
width, height = img.shape[0], img.shape[1]

r = np.zeros((width, height))
g = np.zeros((width, height))
b = np.zeros((width, height))
mid = np.zeros((width, height))

for i in range(width):
    for j in range(height):
        r[i, j] = img[i, j, 0]
        g[i, j] = img[i, j, 1]
        b[i, j] = img[i, j, 2]
        mid[i, j] = (b[i, j] * 0.299 + r[i, j] * 0.587 + g[i, j] * 0.114)

conv_rix = np.zeros((width-2, height-2))

for i in range(1, width-2):
    for j in range(1, height-2):
        buf = np.abs(mid[i, j] - mid[i + 1, j])
        conv_rix[i, j] = buf

conv_rixx = np.zeros((width-2, height-2))

for i in range(1, width-4):
    for j in range(1, height-4):
        buf = np.abs(conv_rix[i, j] - conv_rix[i + 1, j])
        conv_rixx[i, j] = buf

conv_riy = np.zeros((width-2, height-2))

for i in range(1, width-4):
    for j in range(1, height-4):
        buf = np.abs(mid[i, j] - mid[i, j + 1])
        conv_riy[i, j] = buf

conv_riyy = np.zeros((width-2, height-2))

for i in range(1, width-4):
    for j in range(1, height-4):
        buf = np.abs(conv_riy[i, j] - conv_riy[i, j + 1])
        conv_riyy[i, j] = buf

conv_rixy = np.zeros((width-2, height-2))

for i in range(1, width-4):
    for j in range(1, height-4):
        buf = np.abs(conv_rix[i, j] - conv_rix[i, j + 1])
        conv_rixy[i, j] = buf

T = -500000*0.1
k = 0.06
R = np.zeros((width-1, height-1))

for i in range(width - 4):
    for j in range(height - 4):
        det = conv_rixx[i, j] * conv_riyy[i, j] - conv_rixy[i, j] ** 2
        tr = (conv_rixx[i, j] * conv_riyy[i, j])
        R[i, j] = det - k * (tr) ** 2

        if R[i, j] < T:
            r[i, j] = 0
            g[i, j] = 255
            b[i, j] = 0
            # r[i+1, j] = 0
            # g[i+1, j] = 255
            # b[i+1, j] = 0
            # r[i-1, j] = 0
            # g[i-1, j] = 255
            # b[i-1, j] = 0
            # r[i, j+1] = 0
            # g[i, j+1] = 255
            # b[i, j+1] = 0
            # r[i, j-1] = 0
            # g[i, j-1] = 255
            # b[i, j-1] = 0

#rgb_array = np.dstack((conv_rixy.astype(np.uint8), conv_rixy.astype(np.uint8), conv_rixy.astype(np.uint8)))
rgb_array = np.dstack((r.astype(np.uint8), g.astype(np.uint8), b.astype(np.uint8)))

cv2.imwrite('output.png', rgb_array)
cv2.imshow('Narozniki', rgb_array)
cv2.waitKey(0)
cv2.destroyAllWindows()
