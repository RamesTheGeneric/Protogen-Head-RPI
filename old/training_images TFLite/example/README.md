# Getting Started - TensorFlow Lite

There are 2 key elements in the main export directory. Your model in TFLite format (.tflite) and signature.json which contains information about your Lobe project. With these, you are ready to use your model! If you want to see an example of how to use this model, there are instructions below for running a quick test script.

## Example Contents

`signature.json` is created by Lobe and contains information about the model such as label names and the image size and shape the model expects.

`tflite_example.py` is a simple script to quickly test your exported model. It takes a path to an image on your file system, prepares the image and returns the predicted class and confidence level.

`requirements.txt` is where the Python libraries and version information required to run the script are found.

## Run Example

You will need Python 3.6 and the path to an image on your machine to test.

Create a virtual environment

`python -m venv tflite-venv`

Activate the virtual environment

macOS `source tflite-venv/bin/activate`

Windows `tflite-venv/Scripts/activate`

Install the the dependencies for the example

`python -m pip install --upgrade pip && pip install -r requirements.txt`

Pip with the `requirements.txt` file should install the Tensorflow Lite runtime appropriate to your OS version if you are on Windows, Mac, or Linux.
Please double check to make sure that `tflite_runtime` was installed via pip. If you have a different Linux distribution (such as Raspberry Pi),
or find that the runtime was not installed from pip, then please install the appropriate [Tensorflow Lite runtime](https://www.tensorflow.org/lite/guide/python#install_just_the_tensorflow_lite_interpreter) wheel based on your OS and Python version.
For example, if you are on Windows 10 with Python 3.6:

`pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-win_amd64.whl`

Finally, run the example and see the model output

`python tflite_example.py path/to/image/for/testing`

### Notes

If you see the error "OSError: image file is truncated", you may need to add the following lines the sample code due to an issue with PIL (Python Image Library)

```python
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
```
