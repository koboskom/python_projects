# Import the modules
import cv2
import numpy as np
from PIL import Image, ImageFilter


def imageprepare(argv):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    im = (argv).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((28.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 28), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 0))  # paste resized image on white canvas

    tv = list(newImage.getdata())  # get pixel values

    # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    tva = [(255-x) * (1.0) / 255.0 for x in tv]
    # print(tva)
    return tva


def chooseImage(arg, net=None):
    # Read the input image
    im = cv2.imread(arg)

    # Convert to grayscale and apply Gaussian filtering
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

    # Threshold the image
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the image
    ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get rectangles contains each contour
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]

    #data_list = []
    test_data = []
    for i, rect in enumerate(rects):
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
        leng = int(rect[3] * 1.6)
        pt1 = int(rect[1] + 1 + rect[3] // 2 - leng // 2)
        pt2 = int(rect[0] + 1 + rect[2] // 2 - leng // 2)
        roi = im_th[pt1:pt1 + leng, pt2:pt2 + leng]
        roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
        roi = cv2.dilate(roi, (3, 3))
        bnr = np.array(np.reshape(roi,(28, 28)), dtype=np.float32)
        for x in range(28):
            for y in range(5):
                bnr[x][-y] = 0
                bnr[x][y] = 0
        img = Image.fromarray(bnr, 'CMYK')
        x = imageprepare(img)
        arr_x = np.array(x, dtype=np.float32)
        test_data.append(arr_x)
        if net:
            test_data = [np.reshape(x, (784, 1))]
            result = net.network_result(test_data=test_data)[0]
            cv2.putText(im, str(int(result)), (rect[0], rect[1]), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
    if net:
        cv2.imshow("Resulting Image with Rectangular ROIs", im)
        cv2.waitKey()
    test_data.reverse()
    test_data = [np.reshape(x, (784, 1)) for x in test_data]
    return test_data

# chooseImage("../data/image.png")
