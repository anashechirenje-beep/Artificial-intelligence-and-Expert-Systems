# CS50 AI: Traffic

## Overview

For this project, I built a neural network that learns to recognize 43 different kinds of traffic signs. The program reads images from a dataset, prepares them, and trains a convolutional neural network (CNN) to predict the correct traffic sign category.

The images are resized to 30 × 30 pixels, and the model learns to recognize patterns that help it identify each of the 43 categories. The goal is to make accurate predictions on images that were not used during training.

## How the System Works

The program in `traffic.py` goes through each category folder, numbered from `0` to `42`. It loads the images, skips any image that OpenCV cannot read, and resizes each valid image to 30 × 30 pixels. The images are also converted from OpenCV's BGR format to RGB before being stored.

The labels are converted into categorical values representing the 43 possible classes. The images and labels are then divided into training and testing sets using `train_test_split`, with 40% of the data used for testing and 60% for training.

The model is trained for 10 epochs and then evaluated using the test data. The program can also save the trained model in a `.keras` file.

## Neural Network Architecture

The CNN takes images with a shape of 30 × 30 × 3. The three values in the last dimension represent the RGB color channels.

The model has the following layers:

1. A rescaling layer that changes pixel values from 0–255 to 0–1.
2. A convolutional layer with 32 filters and ReLU activation.
3. A 2 × 2 max-pooling layer.
4. A second convolutional layer with 64 filters and ReLU activation.
5. Another 2 × 2 max-pooling layer.
6. A flatten layer.
7. A dense hidden layer with 128 units and ReLU activation.
8. A dropout layer that turns off 50% of the hidden units during training.
9. A dense output layer with 43 units and softmax activation.

The convolutional layers help the model find patterns in the images, such as edges, shapes, and other visual features. Max pooling reduces the size of the information while keeping important features. The dense layer combines the features learned by the earlier layers, while dropout helps reduce overfitting.

The final output layer has 43 units because there are 43 traffic sign categories. Softmax converts the outputs into probabilities, and the category with the highest probability becomes the model's prediction.

The model uses the Adam optimizer, categorical cross-entropy loss, and accuracy as its evaluation metric. It is trained for 10 epochs.

## Experiments and Modifications

I first trained a CNN using convolutional, pooling, flatten, dense, dropout, and output layers. The first run achieved approximately 96.81% test accuracy.

In another experiment, the model performed very poorly, achieving approximately 5.43% test accuracy. When I examined its predictions, I found that it was predicting category 1 for every image. This meant that the model was not properly distinguishing between the 43 traffic sign categories.

After further improvements, I trained the model again and achieved approximately 98.70% test accuracy. The improved version included pixel rescaling and the final CNN architecture described above.

## What Worked and What Did Not Work

The 30 × 30 image size gave the model a consistent input and kept training manageable. Rescaling the pixel values to a range of 0–1 also helped prepare the images for training.

The two convolutional layers helped the model identify visual patterns, while max pooling reduced the amount of information the model had to process. The 128-unit dense layer helped combine the features, and dropout helped reduce overfitting.

What did not work was the experiment in which the model kept predicting category 1 for every image. It failed to distinguish between the different traffic signs and achieved only about 5.43% test accuracy. This showed me how important it is to check the model's predictions rather than looking at accuracy alone.

The improved model performed much better, reaching 98.70% test accuracy compared with the initial result of 96.81%.

## Results and Observations

The recorded test results were:

| Experiment | Test Accuracy |
|---|---:|
| Initial run | Approximately 96.81% |
| Poor-performing experiment | Approximately 5.43% |
| Final improved run | **Approximately 98.70%** |

The initial model already performed well, but the improved model achieved a higher test accuracy. The poor-performing experiment also showed how badly a model can perform when it fails to learn the differences between categories.

In an earlier experiment, I also evaluated a model across the entire dataset and obtained approximately 99% accuracy. However, this evaluation included images that had been used during training, so it is not an independent test result. It should not be compared directly with the final held-out test accuracy.

The final test accuracy of approximately 98.70% is the more appropriate result for judging how well the model performs on data it did not use during training.

Overall, I found that the improved CNN was able to recognize and distinguish between the different traffic sign categories much more effectively.

## How to Run the Project

Install the packages listed in `requirements.txt`, then run:

```bash
python traffic.py gtsrb
```

To train the model and save it in a `.keras` file, run:

```bash
python traffic.py gtsrb traffic_model.keras
```