<div align="center" markdown="1">

# Model Compression Toolkit (MCT)

**Quantize and compress production-ready deep learning vision models for efficient edge deployment.**
#### Version 2.2.1 is out! Notebooks have been updated!
______________________________________________________________________

</div>  
<div align="center">
<p align="center">
  <a href="#getting-started">Getting Started</a> •
  <a href="#high-level-features-and-techniques">High level features and techniques</a> •
  <a href="#resources">Resources</a> • 
 <a href="#community">Community</a> •
  <a href="#license">License</a> •
</p>
<p align="center">
  <a href="https://sony.github.io/model_optimization#prerequisites"><img src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue" /></a>
  <a href="https://sony.github.io/model_optimization#prerequisites"><img src="https://img.shields.io/badge/pytorch-1.9%20%7C%201.10-blue" /></a>
  <a href="https://pypi.org/project/super-gradients/"><img src="https://img.shields.io/pypi/v/super-gradients" /></a>
  <a href="https://github.com/Deci-AI/super-gradients/blob/master/documentation/source/model_zoo.md" ><img src="https://img.shields.io/badge/pre--trained%20models-34-brightgreen" /></a>
  <a href="https://github.com/Deci-AI/super-gradients/releases"><img src="https://img.shields.io/github/v/release/Deci-AI/super-gradients" /></a>
  <a href="https://github.com/sony/model_optimization/discussions"><img src="https://img.shields.io/badge/discussions-blue" /></a>
  <a href="https://github.com/Deci-AI/super-gradients/blob/master/LICENSE.md"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" /></a>
 </p>    
</div>

__________________________________________________________________________________________________________


## Quantize with MCT
__________________________________________________________________________________________________________

Open-source project for neural network model optimization, providing researchers, developers, and engineers with advanced quantization and compression tools for deploying state-of-the-art neural networks on efficient, constrained hardware.

### Support various computer vision tasks
<p align="center">
<img src="/docsrc/images/Classification.png" width="200">
<img src="/docsrc/images/SemSeg.png" width="200">
<img src="/docsrc/images/PoseEst.png" width="200">
<img src="/docsrc/images/ObjDet.png" width="200">


## Getting Started
### Quick Installation
Pip install the model compression toolkit package in a Python>=3.9 environment with PyTorch>=2.1 or Tensorflow>=2.12.
```
pip install model-compression-toolkit
```
For installing the nightly version or installing from source, refer to the [installation guide](https://github.com/sony/model_optimization/blob/main/INSTALLATION.md).

In order to use MCT, you’ll need to provide a floating point .pt or .keras model as an input.

### Supported Quantization flows</div>  
MCT supports various quantization flows as appears below. 
<div align="center">
<p align="center">

Quantization Method  | Complexity | Computational Cost | Tutorial
-------------------- | -----------|--------------------|---------
PTQ (Post Training Quantization)  | Low | Low (~1-10 CPU minutes) | Tutorial
GPTQ (parameters fine-tuning using gradients)  | Mild | Mild (~2-3 GPU hours) | Tutorial
QAT (Quantization Aware Training)  | High | High (~12-36 GPU hours) | Tutorial
</p>    
</div>

For each flow, **Quantization core** utilizes various algorithms and hyper-parameters for optimal [hardware-aware](https://github.com/sony/model_optimization/blob/main/model_compression_toolkit/target_platform_capabilities/README.md) quantization results. 
For further details, please see [Supported features and algorithms](#supported-features). User can either provide their own representative dataset, or utilize the [Data Generation](#data-generation-) capability.

<div align="center">
<p align="center">

<img src="/docsrc/images/mctFlow.png" width="800">
</p>    
</div>


### Tutorials and Examples 

Our [tutorials](https://github.com/sony/model_optimization/blob/main/tutorials/README.md) section will walk you through the basics of deploying your first model; Covering various compression techniques for both Keras and PyTorch models. 
Access interactive notebooks for hands-on learning with popular models/tasks, for example:

<details id="keras-ptq">
  <summary>Keras</summary>
[![Open In Colab](https://colab.research.google.com/github/sony/model_optimization/blob/main/tutorials/notebooks/imx500_notebooks/keras/example_keras_mobilenetv2_for_imx500.ipynb) [MobileNetV2](https://github.com/sony/model_optimization/blob/main/tutorials/notebooks/imx500_notebooks/keras/example_keras_mobilenetv2_for_imx500.ipynb) 
  
  <a 
  href="https://colab.research.google.com/github/sony/model_optimization/blob/main/tutorials/notebooks/imx500_notebooks/keras/example_keras_mobilenetv2_for_imx500.ipynb"><img src="/docsrc/images/colab-badge.svg" /></a>   [MobileNetV2 PTQ](https://github.com/sony/model_optimization/blob/main/tutorials/notebooks/imx500_notebooks/keras/example_keras_mobilenetv2_for_imx500.ipynb)

</details>


See [tutorials](https://github.com/sony/model_optimization/blob/main/tutorials/README.md) for more examples or move on to Resources section.
  <a href="NOTEBOOK UR""><imag src="/docsrc/images/colab-badge.svg>

### Supported Versions

Currently, MCT is being tested on various Python, Pytorch and TensorFlow versions:


|             |  PyTorch 2.1                                                                                                                                                                                                               | PyTorch 2.2                                                                                                                                                                                                              | PyTorch 2.3                                                                                                                                                                                                              | PyTorch 2.4                                                                                                                                                                                                              |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python 3.9  | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch21.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch21.yml)   | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch22.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch22.yml)   | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch23.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch23.yml)   | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch24.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_pytorch24.yml)   |
| Python 3.10 | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch21.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch21.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch22.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch22.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch23.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch23.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch24.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_pytorch24.yml) |
| Python 3.11 | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch21.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch21.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch22.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch22.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch23.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch23.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch24.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_pytorch24.yml) |



|             | TensorFlow 2.12                                                                                                                                                                                                                        | TensorFlow 2.13                                                                                                                                                                                                                        | TensorFlow 2.14                                                                                                                                                                                                                        | TensorFlow 2.15                                                                                                                                                                                                        |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Python 3.9  | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras212.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras212.yml)   | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras213.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras213.yml)   | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras214.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras214.yml)   | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras215.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python39_keras215.yml)   |
| Python 3.10 | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras212.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras212.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras213.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras213.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras214.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras214.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras215.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python310_keras215.yml) |
| Python 3.11 | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras212.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras212.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras213.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras213.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras214.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras214.yml) | [![Run Tests](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras215.yml/badge.svg)](https://github.com/sony/model_optimization/actions/workflows/run_tests_python311_keras215.yml) |


## Supported Features
MCT offers a range of powerful features to optimize neural network models for efficient deployment. These supported features include:

### Data Generation [*](https://github.com/sony/model_optimization?tab=readme-ov-file#experimental-features)
MCT provides tools for generating synthetic images based on the statistics stored in a model's batch normalization layers. These generated images are valuable for various compression tasks where image data is required, such as quantization and pruning. 
You can customize data generation configurations to suit your specific needs. [Go to the Data Generation page.](https://github.com/sony/model_optimization/blob/main/model_compression_toolkit/data_generation/README.md)

### Quantization
MCT supports different quantization methods:
* Post-training quantization (PTQ): [Keras API](https://sony.github.io/model_optimization/docs/api/api_docs/methods/keras_post_training_quantization.html), [PyTorch API](https://sony.github.io/model_optimization/docs/api/api_docs/methods/pytorch_post_training_quantization.html)
* Gradient-based post-training quantization (GPTQ): [Keras API](https://sony.github.io/model_optimization/docs/api/api_docs/methods/keras_gradient_post_training_quantization.html), [PyTorch API](https://sony.github.io/model_optimization/docs/api/api_docs/methods/pytorch_gradient_post_training_quantization.html)
* Quantization-aware training (QAT) [*](https://github.com/sony/model_optimization?tab=readme-ov-file#experimental-features)


| Quantization Method                           | Complexity | Computational Cost          |
|-----------------------------------------------|------------|-----------------------------|
| PTQ                                           | Low        | Low (order of minutes)      |
| GPTQ (parameters fine-tuning using gradients) | Mild       | Mild (order of 2-3 hours)   |
| QAT                                           | High       | High (order of 12-36 hours) |


In addition, MCT supports different quantization schemes for quantizing weights and activations:

* Power-Of-Two (hardware-friendly quantization [1])
* Symmetric
* Uniform

Main features:
* <ins>Graph optimizations:</ins> Transforming the model to an equivalent (yet, more efficient) model (for example, batch-normalization layer folding to its preceding linear layer).
* <ins>Quantization parameter search:</ins> Different methods can be used to minimize the expected added quantization-noise during thresholds search (by default, we use Mean-Square-Error, but other metrics can be used such as No-Clipping, Mean-Average-Error, and more).
* <ins>Advanced quantization algorithms:</ins> To prevent a performance degradation some algorithms are applied such as: 
  * <ins>Shift negative correction:</ins> Symmetric activation quantization can hurt the model's performance when some layers output both negative and positive activations, but their range is asymmetric. For more details please visit [1].
  * <ins>Outliers filtering:</ins> Computing z-score for activation statistics to detect and remove outliers.
* <ins>Clustering:</ins> Using non-uniform quantization grid to quantize the weights and activations to match their distributions.[*](https://github.com/sony/model_optimization?tab=readme-ov-file#experimental-features)
* <ins>Mixed-precision search:</ins> Assigning quantization bit-width per layer (for weights/activations), based on the layer's sensitivity to different bit-widths.
* <ins>Visualization:</ins> You can use TensorBoard to observe useful information for troubleshooting the quantized model's performance (for example, the model in different phases of the quantization, collected statistics, similarity between layers of the float and quantized model and bit-width configuration for mixed-precision quantization). For more details, please read the [visualization documentation](https://sony.github.io/model_optimization/docs/guidelines/visualization.html).   
* <ins>Target Platform Capabilities:</ins> The Target Platform Capabilities (TPC) describes the target platform (an edge device with dedicated hardware). For more details, please read the [TPC README](https://github.com/sony/model_optimization/blob/main/model_compression_toolkit/target_platform_capabilities/README.md).   

### Enhanced Post-Training Quantization (EPTQ)
As part of the GPTQ we provide an advanced optimization algorithm called EPTQ.

The specifications of the algorithm are detailed in the paper: _"**EPTQ: Enhanced Post-Training Quantization via Label-Free Hessian**"_ [4].

More details on the how to use EPTQ via MCT can be found in the [EPTQ guidelines](https://github.com/sony/model_optimization/blob/main/model_compression_toolkit/gptq/README.md).


### Structured Pruning [*](https://github.com/sony/model_optimization?tab=readme-ov-file#experimental-features)
MCT introduces a structured and hardware-aware model pruning.
This pruning technique is designed to compress models for specific hardware architectures, 
taking into account the target platform's Single Instruction, Multiple Data (SIMD) capabilities. 
By pruning groups of channels (SIMD groups), our approach not only reduces model size 
and complexity, but ensures that better utilization of channels is in line with the SIMD architecture 
for a target Resource Utilization of weights memory footprint.
[Keras API](https://sony.github.io/model_optimization/docs/api/api_docs/methods/keras_pruning_experimental.html)
[Pytorch API](https://sony.github.io/model_optimization/docs/api/api_docs/methods/pytorch_pruning_experimental.html) 

#### Experimental features 

Some features are experimental and subject to future changes. 
 
For more details, we highly recommend visiting our project website where experimental features are mentioned as experimental.


## Results
### Keras
Graph of [MobileNetV2](https://keras.io/api/applications/mobilenet/) accuracy on ImageNet vs average bit-width of weights, using 
single-precision quantization, mixed-precision quantization, and mixed-precision quantization with GPTQ.

<img src="https://github.com/sony/model_optimization/raw/main/docsrc/images/mbv2_accuracy_graph.png">

For more results, please see [1]

### Pytorch
We quantized classification networks from the torchvision library. 
In the following table we present the ImageNet validation results for these models:

| Network Name              | Float Accuracy  | 8Bit Accuracy   | Data-Free 8Bit Accuracy |
|---------------------------|-----------------|-----------------|-------------------------|
| MobileNet V2 [3]          | 71.886          | 71.444          |71.29|
| ResNet-18 [3]             | 69.86           | 69.63           |69.53|
| SqueezeNet 1.1 [3]        | 58.128          | 57.678          ||


#### Pruning Results

Results for applying pruning to reduce the parameters of the following models by 50%:

| Model           | Dense Model Accuracy | Pruned Model Accuracy |
|-----------------|----------------------|-----------------------|
| ResNet50 [2]    | 75.1                 | 72.4                  |
| DenseNet121 [3] | 74.44                | 71.71                 |


## Trouble Shooting

If the accuracy degradation of the quantized model is too large for your application, check out the [Quantization Troubleshooting](https://github.com/sony/model_optimization/tree/main/quantization_troubleshooting.md)
for common pitfalls and some tools to improve quantization accuracy.

Check out the [FAQ](https://github.com/sony/model_optimization/tree/main/FAQ.md) for common issues.


## Contributions
MCT aims at keeping a more up-to-date fork and welcomes contributions from anyone.

*You will find more information about contributions in the [Contribution guide](https://github.com/sony/model_optimization/blob/main/CONTRIBUTING.md).


## License
[Apache License 2.0](https://github.com/sony/model_optimization/blob/main/LICENSE.md).

## References 

[1] Habi, H.V., Peretz, R., Cohen, E., Dikstein, L., Dror, O., Diamant, I., Jennings, R.H. and Netzer, A., 2021. [HPTQ: Hardware-Friendly Post Training Quantization. arXiv preprint](https://arxiv.org/abs/2109.09113).

[2] [Keras Applications](https://keras.io/api/applications/)

[3] [TORCHVISION.MODELS](https://pytorch.org/vision/stable/models.html) 

[4] Gordon, O., Habi, H. V., & Netzer, A., 2023. [EPTQ: Enhanced Post-Training Quantization via Label-Free Hessian. arXiv preprint](https://arxiv.org/abs/2309.11531)
