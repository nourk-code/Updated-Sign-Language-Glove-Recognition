# Smart Glove System for Gesture Recognition

## Overview

This repository contains the implementation of a Smart Glove System for real-time gesture recognition using multiple machine learning models. The glove collects data from flex sensors and an accelerometer/gyroscope, processes it, and predicts hand gestures using machine learning. The final prediction is determined through a majority voting mechanism across models and outputted via a text-to-speech system.

## Features

* Real-time gesture data collection via Arduino.

Integration of multiple machine learning models:

* K-Nearest Neighbors (KNN)

* Random Forest

* Naive Bayes

* Support Vector Machines (SVM)

* Logistic Regression

* Decision Tree

* Majority voting mechanism for robust prediction.

* Text-to-speech feedback for user interaction.

* Modular and extensible pipeline for future enhancements.

## Dataset

## Data Collection:

Sensors Used:

* Flex Sensors: Captures bending angles (angle1 through angle5).

* MPU-6050: Records accelerometer (X, Y, Z) and gyroscope data.


Data Format:

* Each gesture is represented by 500 samples.

* Dataset contains 10 features: angle1, angle2, angle3, angle4, angle5, X, Y, Z.

* Data stored in .csv format and later processed into NumPy arrays.     

## Future Work

Expand the dataset to include more gestures.

Integrate more advanced models like LSTMs for improved sequential gesture recognition.

Optimize the real-time prediction pipeline for faster processing.



