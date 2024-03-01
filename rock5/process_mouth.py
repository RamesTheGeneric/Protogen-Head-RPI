import cv2

def Func(rknn_lite, img):
    img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype('float32')
    img /= 255.0
    img = img.reshape(1, 1, 256, 256)
    outputs = rknn_lite.inference(inputs=[img])
    array = outputs[0][0]
    for i in range(len(array)):  # Clip values between 0 - 1
        array[i] = max(min(array[i], 1), 0)
    return array
