{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Let's load a Handwritten Digit classifier we'll be building very soon!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Using TensorFlow backend.\n"
     ]
    }
   ],
   "source": [
    "import cv2\n",
    "import numpy as np\n",
    "from keras.datasets import mnist\n",
    "from keras.models import load_model\n",
    "\n",
    "classifier = load_model('/home/deeplearningcv/DeepLearningCV/Trained Models/mnist_simple_cnn.h5')\n",
    "\n",
    "# loads the MNIST dataset\n",
    "(x_train, y_train), (x_test, y_test)  = mnist.load_data()\n",
    "\n",
    "def draw_test(name, pred, input_im):\n",
    "    BLACK = [0,0,0]\n",
    "    expanded_image = cv2.copyMakeBorder(input_im, 0, 0, 0, imageL.shape[0] ,cv2.BORDER_CONSTANT,value=BLACK)\n",
    "    expanded_image = cv2.cvtColor(expanded_image, cv2.COLOR_GRAY2BGR)\n",
    "    cv2.putText(expanded_image, str(pred), (152, 70) , cv2.FONT_HERSHEY_COMPLEX_SMALL,4, (0,255,0), 2)\n",
    "    cv2.imshow(name, expanded_image)\n",
    "\n",
    "for i in range(0,10):\n",
    "    rand = np.random.randint(0,len(x_test))\n",
    "    input_im = x_test[rand]\n",
    "\n",
    "    imageL = cv2.resize(input_im, None, fx=4, fy=4, interpolation = cv2.INTER_CUBIC) \n",
    "    input_im = input_im.reshape(1,28,28,1) \n",
    "    \n",
    "    ## Get Prediction\n",
    "    res = str(classifier.predict_classes(input_im, 1, verbose = 0)[0])\n",
    "    draw_test(\"Prediction\", res, imageL) \n",
    "    cv2.waitKey(0)\n",
    "\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Testing our classifier on a real image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The number is: 13540\n"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "import cv2\n",
    "from preprocessors import x_cord_contour, makeSquare, resize_to_pixel\n",
    "       \n",
    "image = cv2.imread('images/numbers.jpg')\n",
    "gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)\n",
    "cv2.imshow(\"image\", image)\n",
    "cv2.waitKey(0)\n",
    "\n",
    "# Blur image then find edges using Canny \n",
    "blurred = cv2.GaussianBlur(gray, (5, 5), 0)\n",
    "#cv2.imshow(\"blurred\", blurred)\n",
    "#cv2.waitKey(0)\n",
    "\n",
    "edged = cv2.Canny(blurred, 30, 150)\n",
    "#cv2.imshow(\"edged\", edged)\n",
    "#cv2.waitKey(0)\n",
    "\n",
    "# Find Contours\n",
    "_, contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n",
    "\n",
    "#Sort out contours left to right by using their x cordinates\n",
    "contours = sorted(contours, key = x_cord_contour, reverse = False)\n",
    "\n",
    "# Create empty array to store entire number\n",
    "full_number = []\n",
    "\n",
    "# loop over the contours\n",
    "for c in contours:\n",
    "    # compute the bounding box for the rectangle\n",
    "    (x, y, w, h) = cv2.boundingRect(c)    \n",
    "\n",
    "    if w >= 5 and h >= 25:\n",
    "        roi = blurred[y:y + h, x:x + w]\n",
    "        ret, roi = cv2.threshold(roi, 127, 255,cv2.THRESH_BINARY_INV)\n",
    "        roi = makeSquare(roi)\n",
    "        roi = resize_to_pixel(28, roi)\n",
    "        cv2.imshow(\"ROI\", roi)\n",
    "        roi = roi / 255.0       \n",
    "        roi = roi.reshape(1,28,28,1) \n",
    "\n",
    "        ## Get Prediction\n",
    "        res = str(classifier.predict_classes(roi, 1, verbose = 0)[0])\n",
    "        full_number.append(res)\n",
    "        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)\n",
    "        cv2.putText(image, res, (x , y + 155), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)\n",
    "        cv2.imshow(\"image\", image)\n",
    "        cv2.waitKey(0) \n",
    "        \n",
    "cv2.destroyAllWindows()\n",
    "print (\"The number is: \" + ''.join(full_number))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Training this Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Using TensorFlow backend.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "x_train shape: (60000, 28, 28, 1)\n",
      "60000 train samples\n",
      "10000 test samples\n",
      "Number of Classes: 10\n",
      "_________________________________________________________________\n",
      "Layer (type)                 Output Shape              Param #   \n",
      "=================================================================\n",
      "conv2d_1 (Conv2D)            (None, 26, 26, 32)        320       \n",
      "_________________________________________________________________\n",
      "conv2d_2 (Conv2D)            (None, 24, 24, 64)        18496     \n",
      "_________________________________________________________________\n",
      "max_pooling2d_1 (MaxPooling2 (None, 12, 12, 64)        0         \n",
      "_________________________________________________________________\n",
      "dropout_1 (Dropout)          (None, 12, 12, 64)        0         \n",
      "_________________________________________________________________\n",
      "flatten_1 (Flatten)          (None, 9216)              0         \n",
      "_________________________________________________________________\n",
      "dense_1 (Dense)              (None, 128)               1179776   \n",
      "_________________________________________________________________\n",
      "dropout_2 (Dropout)          (None, 128)               0         \n",
      "_________________________________________________________________\n",
      "dense_2 (Dense)              (None, 10)                1290      \n",
      "=================================================================\n",
      "Total params: 1,199,882\n",
      "Trainable params: 1,199,882\n",
      "Non-trainable params: 0\n",
      "_________________________________________________________________\n",
      "None\n",
      "Train on 60000 samples, validate on 10000 samples\n",
      "Epoch 1/5\n",
      "60000/60000 [==============================] - 189s 3ms/step - loss: 0.2667 - acc: 0.9187 - val_loss: 0.0556 - val_acc: 0.9819\n",
      "Epoch 2/5\n",
      "60000/60000 [==============================] - 170s 3ms/step - loss: 0.0889 - acc: 0.9740 - val_loss: 0.0396 - val_acc: 0.9864\n",
      "Epoch 3/5\n",
      "60000/60000 [==============================] - 192s 3ms/step - loss: 0.0670 - acc: 0.9805 - val_loss: 0.0350 - val_acc: 0.9884\n",
      "Epoch 4/5\n",
      "60000/60000 [==============================] - 194s 3ms/step - loss: 0.0553 - acc: 0.9838 - val_loss: 0.0321 - val_acc: 0.9897\n",
      "Epoch 5/5\n",
      "60000/60000 [==============================] - 204s 3ms/step - loss: 0.0464 - acc: 0.9856 - val_loss: 0.0282 - val_acc: 0.9907\n",
      "Test loss: 0.028205487172584982\n",
      "Test accuracy: 0.9907\n"
     ]
    }
   ],
   "source": [
    "from keras.datasets import mnist\n",
    "from keras.utils import np_utils\n",
    "import keras\n",
    "from keras.datasets import mnist\n",
    "from keras.models import Sequential\n",
    "from keras.layers import Dense, Dropout, Flatten\n",
    "from keras.layers import Conv2D, MaxPooling2D\n",
    "from keras import backend as K\n",
    "\n",
    "# Training Parameters\n",
    "batch_size = 128\n",
    "epochs = 5\n",
    "\n",
    "# loads the MNIST dataset\n",
    "(x_train, y_train), (x_test, y_test)  = mnist.load_data()\n",
    "\n",
    "# Lets store the number of rows and columns\n",
    "img_rows = x_train[0].shape[0]\n",
    "img_cols = x_train[1].shape[0]\n",
    "\n",
    "# Getting our date in the right 'shape' needed for Keras\n",
    "# We need to add a 4th dimenion to our date thereby changing our\n",
    "# Our original image shape of (60000,28,28) to (60000,28,28,1)\n",
    "x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)\n",
    "x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)\n",
    "\n",
    "# store the shape of a single image \n",
    "input_shape = (img_rows, img_cols, 1)\n",
    "\n",
    "# change our image type to float32 data type\n",
    "x_train = x_train.astype('float32')\n",
    "x_test = x_test.astype('float32')\n",
    "\n",
    "# Normalize our data by changing the range from (0 to 255) to (0 to 1)\n",
    "x_train /= 255\n",
    "x_test /= 255\n",
    "\n",
    "print('x_train shape:', x_train.shape)\n",
    "print(x_train.shape[0], 'train samples')\n",
    "print(x_test.shape[0], 'test samples')\n",
    "\n",
    "# Now we one hot encode outputs\n",
    "y_train = np_utils.to_categorical(y_train)\n",
    "y_test = np_utils.to_categorical(y_test)\n",
    "\n",
    "# Let's count the number columns in our hot encoded matrix \n",
    "print (\"Number of Classes: \" + str(y_test.shape[1]))\n",
    "\n",
    "num_classes = y_test.shape[1]\n",
    "num_pixels = x_train.shape[1] * x_train.shape[2]\n",
    "\n",
    "# create model\n",
    "model = Sequential()\n",
    "\n",
    "model.add(Conv2D(32, kernel_size=(3, 3),\n",
    "                 activation='relu',\n",
    "                 input_shape=input_shape))\n",
    "model.add(Conv2D(64, (3, 3), activation='relu'))\n",
    "model.add(MaxPooling2D(pool_size=(2, 2)))\n",
    "model.add(Dropout(0.25))\n",
    "model.add(Flatten())\n",
    "model.add(Dense(128, activation='relu'))\n",
    "model.add(Dropout(0.5))\n",
    "model.add(Dense(num_classes, activation='softmax'))\n",
    "\n",
    "model.compile(loss = 'categorical_crossentropy',\n",
    "              optimizer = keras.optimizers.Adadelta(),\n",
    "              metrics = ['accuracy'])\n",
    "\n",
    "print(model.summary())\n",
    "\n",
    "history = model.fit(x_train, y_train,\n",
    "          batch_size=batch_size,\n",
    "          epochs=epochs,\n",
    "          verbose=1,\n",
    "          validation_data=(x_test, y_test))\n",
    "\n",
    "score = model.evaluate(x_test, y_test, verbose=0)\n",
    "print('Test loss:', score[0])\n",
    "print('Test accuracy:', score[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
