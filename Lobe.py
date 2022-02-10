from lobe import ImageModel

model = ImageModel.load('model/training_images TensorFlow')

# OPTION 1: Predict from an image file
result = model.predict_from_file('training_images/New folder/test1.png')

# OPTION 2: Predict from an image url
#result = model.predict_from_url('http://url/to/file.jpg')

# OPTION 3: Predict from Pillow image
from PIL import Image
img = Image.open('training_images/New folder/test1.png')
result = model.predict(img)

# Print top prediction
print(result.prediction)

# Print all classes
for label, confidence in result.labels:
    print(f"{label}: {confidence*100}%")

# Visualize the heatmap of the prediction on the image 
# this shows where the model was looking to make its prediction.
heatmap = model.visualize(img)
heatmap.show()