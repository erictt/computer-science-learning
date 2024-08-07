---
weight: 1
title: "Week 11 - Application Example: Photo OCR"
---

# Week 11 - Application Example: Photo OCR

## Problem Description and Pipeline

* Photo OCR: Photo Optical Character Recognition.
* Photo OCR Pipeline(a machine learning pipeline):
  * <img src="https://i.imgur.com/xRLqcUu.jpg" style="width:500px" />
  * <img src="https://i.imgur.com/QlpKisR.jpg" style="width:500px" />
* **Pipelines** are common terms in machine learning
  * Separate modules which may each be a machine learning component or data processing component

### Sliding Windows Classifier

* In order to talk about detecting things in images let's start with a simpler example of **pedestrian detection**.
  * <img src="https://i.imgur.com/Qz19sbN.jpg" style="width:300px" />

#### Supervised Learning for Pedestrian Detection

* Given the training set:
  * $x$ = pixels in 82x36 image patches
  * <img src="https://i.imgur.com/GcSVSY5.jpg" style="width:500px" />

* Now we have a new image - how do we find pedestrians in it?
  * <img src="https://i.imgur.com/btQ6fVk.jpg" style="width:400px" />

    * Start by taking a rectangular 82x36 patch in the image
    * Keep stepping rectangle along all the way to the right with 4 pixels/step(always 5-8 pixels).
    * Then move back to the left hand side but step down a bit too.
    * Keep the steps until the last line.
  * <img src="https://i.imgur.com/HGNbQ3O.jpg" style="width:400px" />

    * Now we initially start with a larger image patch (of the same aspect ratio)
    * Each time we process the image patch, we're resizing the larger patch to a smaller image, then running that smaller image through the classifier.
  * Hopefully, we will eventually get this:
    * <img src="https://i.imgur.com/qtbi8wo.jpg" style="width:400px" />

* **Back to Text Detection**

  * <img src="https://i.imgur.com/Op8qKI2.jpg" style="width:400px" />
  * Like pedestrian detection, we generate a labeled training set with
    * Positive examples (some kind of text)
    * Negative examples (not text)
  * Having trained the classifier we apply it to an image
    * So, run a sliding window classifier at a fixed rectangle size
    * If you do that end up with something like this
      * <img src="https://i.imgur.com/EMaa7JV.jpg" style="width:300px" />
      * Black - no text
      * White - text
    * For text detection, we want to draw rectangles around all the regions where there is text in the image
    * Take classifier output and apply an **expansion algorithm**
      * Takes each of white regions and expands it
      * <img src="https://i.imgur.com/Dzi5PAY.jpg" style="width:300px" />
    * Look at connected white regions in the image above

### Character Segmentation

* Look in a defined image patch and decide, is there a split between two characters?
* <img src="https://i.imgur.com/SUIdnxJ.jpg" style="width:500px" />
* Train a classifier to classify between positive and negative examples
* Use a 1-dimensional sliding window to move along text regions
  * Does each window snapshot look like the split between two characters?
    * If yes insert a split
    * If not move on

### Character Classification

* Multi-class characterization problem

## Getting Lots of Data: Artificial Data Synthesis

### Artificial Data Synthesis for Photo OCR

1. Use computer's font library, or online font libraries. Take different fonts, paste them with random backgrounds
2. Distort the exist data set
    * <img src="https://i.imgur.com/vAjuJWG.jpg" style="width:400px" />  

* **Synthesizing data by introducing distortions**: Speech recognition
  * We can add noisy background to the original audio to make it unclear

## Getting More Data

* When do we need to get more data?
  * Make sure we have a low bias classifier. (Plot learning curves)
* When we really need it, ask ourselves: "How much work would it be to get 10x as much data as we currently have?"
  * Artificial data synthesis
    ­* Collect/label it yourself
  * "Crowd source" (E.g. Amazon Mechanical Turk)

## Ceiling Analysis

* Estimating the errors due to each component.
* Decide what part of the pipeline we should spend the most time trying to improve.
* Take the Photo OCR pipeline as the example:
  * <img src="https://i.imgur.com/xRLqcUu.jpg" style="width:500px" />
  * We find that our test set has 72% accuracy.
  * Steps:
        1. Go to the first module - Text detection. Manually tell the algorithm where the text is.
            * Simulate if your text detection system was 100% accurate
            * Check how this change affects the accuracy of the overall system.
            * Accuracy goes up to 89%
        2. Next do the same for the character segmentation
            * Accuracy goes up to 90% now
        3. Finally doe the same for character recognition
            * Goes up to 100%
  * <img src="https://i.imgur.com/DXBLm7x.jpg" style="width:400px" />
  * Base on the analysis, we know which module to improve.

## Refers

* [http://www.holehouse.org/mlclass/18_Application_Example_OCR.html](http://www.holehouse.org/mlclass/18_Application_Example_OCR.html)
