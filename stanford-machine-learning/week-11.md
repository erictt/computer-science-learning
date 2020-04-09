# Week 11 - Application Example: Photo OCR

\[TOC\]

## Problem Description and Pipeline

* Photo OCR: Photo Optical Character Recognition. 
* Photo OCR Pipeline\(a machine learning pipeline\):
  * ![](../.gitbook/assets/15134246854400.jpg)
  * ![](../.gitbook/assets/15134257884572%20%281%29.jpg)
* **Pipelines** are common terms in machine learning
  * Separate modules which may each be a machine learning component or data processing component

### Sliding Windows Classifier

* In order to talk about detecting things in images let's start with a simpler example of **pedestrian detection**.
  * ![](../.gitbook/assets/15134298585353.jpg)

#### Supervised Learning for Pedestrian Detection

* Given the training set:
  * \\(x\\) = pixels in 82x36 image patches
  * ![](../.gitbook/assets/15134299758172%20%281%29.jpg)
* Now we have a new image - how do we find pedestrians in it?
  * ![](../.gitbook/assets/15134981071831.jpg)
    * Start by taking a rectangular 82x36 patch in the image
    * Keep stepping rectangle along all the way to the right with 4 pixels/step\(always 5-8 pixels\).
    * Then move back to the left hand side but step down a bit too. 
    * Keep the steps until the last line.
  * ![](../.gitbook/assets/15134982376433%20%281%29.jpg)
    * Now we initially start with a larger image patch \(of the same aspect ratio\)
    * Each time we process the image patch, we're resizing the larger patch to a smaller image, then running that smaller image through the classifier.
  * Hopefully, we will eventually get this:
    * ![](../.gitbook/assets/15134985480977.jpg)
* **Back to Text Detection**
  * ![](../.gitbook/assets/15134988946460.jpg)
  * Like pedestrian detection, we generate a labeled training set with
    * Positive examples \(some kind of text\) 
    * Negative examples \(not text\)
  * Having trained the classifier we apply it to an image
    * So, run a sliding window classifier at a fixed rectangle size
    * If you do that end up with something like this
      * ![](../.gitbook/assets/15134988507588%20%281%29.jpg)
      * Black - no text
      * White - text
    * For text detection, we want to draw rectangles around all the regions where there is text in the image
    * Take classifier output and apply an **expansion algorithm**
      * Takes each of white regions and expands it
      * ![](../.gitbook/assets/15135005982016.jpg)
    * Look at connected white regions in the image above

### Character Segmentation

* Look in a defined image patch and decide, is there a split between two characters?
* ![](../.gitbook/assets/15135007906121.jpg)
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
   * ![](../.gitbook/assets/15135012525417%20%281%29.jpg)  
3. **Synthesizing data by introducing distortions**: Speech recognition
   * We can add noisy background to the original audio to make it unclear

## Getting More Data

* When do we need to get more data?
  * Make sure we have a low bias classifier. \(Plot learning curves\)
* When we really need it, ask ourselves: "How much work would it be to get 10x as much data as we currently have?"
  * Artificial data synthesis

    ­\* Collect/label it yourself 

  * "Crowd source" \(E.g. Amazon Mechanical Turk\)

## Ceiling Analysis

* Estimating the errors due to each component.
* Decide what part of the pipeline we should spend the most time trying to improve.
* Take the Photo OCR pipeline as the example:
  * ![](../.gitbook/assets/15134246854400.jpg)
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
  * ![](../.gitbook/assets/15135020893319%20%281%29.jpg)
  * Base on the analysis, we know which module to improve.

## Refers

* [http://www.holehouse.org/mlclass/18\_Application\_Example\_OCR.html](http://www.holehouse.org/mlclass/18_Application_Example_OCR.html)

