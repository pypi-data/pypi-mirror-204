<p align="center">
  <img src="https://cdn.imgbin.com/10/3/23/imgbin-breast-cancer-senology-mammography-diego-JcEW147fdbivCyrvC5vykSPj3.jpg" height="200">
</p>

# MamToolKit
### A Comprehensive Deep Learning Library for Mammogram Assessment
[![PyPI version](https://badge.fury.io/py/mktoolkit.svg)](https://badge.fury.io/py/mktoolkit)
![GitHub](https://img.shields.io/github/license/mktoolkit/mktoolkit)
[![Downloads](https://static.pepy.tech/badge/mktoolkit)](https://pepy.tech/project/mktoolkit)

**[[Documentation]](https://github.com/uefcancer/mamtoolkit/)**
| **[[Paper]]()** 
| **[[Notebook examples]]()** 
| **[[Web applications]]()** 

**Welcome to `MamToolKit` Repository!** `MamToolKit` is a python-based library designed to facilitate the creation of mammogram image analysis pipelines . The library includes plug-and-play modules to perform:
- Standard mammogram image pre-processing (e.g., *normalization*, *bounding box cropping*, and *DICOM to jpeg conversion*)
- Mammogram assessment pipelines (e.g., *breast area segmentation*, *dense tissue segmentation*, and *percentage density estimation*)
- Modeling deep learning architectures for various downstream tasks  (e.g., *micro-calcification* and *mass detection*)
- Feature attribution-based interpretability techniques (e.g., *GradCAM*, *GradCAM++*, and *LRP*)
- Visualization 

All the functionalities are grouped under a user-friendly API. 

If you encounter any issue or have questions regarding the library, feel free to [open a GitHub issue](https://github.com/uefcancer/mamtoolkit/issues). We'll do our best to address it. 

# Installation 

## PyPI installer (recommended)

`pip install -U mamtoolkit`

## Development setup 

- Clone the repo:

```
git clone https://github.com/uefcancer/mktoolkit/mamtoolkit.git && cd mamtoolkit
```

- Create a conda environment:

```
conda env create -f environment.yml
```
**NOTE**: To use GPUs, install GPU compatible [Pytorch](https://pytorch.org/get-started/locally/), [Torchvision](https://pytorch.org/get-started/locally/) packages according to your OS, package manager, and CUDA.

- Activate it:

```
conda activate mamtoolkit
```

- Add `MamToolKit` to your python path:

```
export PYTHONPATH="<PATH>/mamtoolkit:$PYTHONPATH"
```

# Using MamToolKit 

The `MamToolKit` library provides a set of helpers grouped in different modules, namely `preprocessing`, `assessment`, `interpretability`, and  `visualization`.  

For instance, with  `MamToolKit` library, we can load percentage mammogram density model (described in the [[Paper]](https://www.nature.com/articles/s41598-022-16141-2) ) and predict the non-dense area, dense tissue area, and estimate percentage density:
```python
import mamtoolkit as mg

model = mg.load_model("base")
result = mg.percentage_density(model, image_path) #path to mammogram image
print(result)
```
The `percentage_density()` method is a part of `assessment` module, which pre-processes the input image and converts it into the appropriate format and dimension accepted by the model. Then the model provides the analysis in forms of a dictionary with keys: non_dense_area, dense_area, and density.

Notice: The non_dense_area and dense_area are calculated in cm^2 

```
result['non_dense_area'] = 
result['dense_area'] = 
result['density']
```

## License

The MamToolKit library is released under the MIT License. See [LICENSE] (https://github.com/openai/whisper/blob/main/LICENSE) for further details.

If you use this library, please consider citing:
```
@article{gudhe2022area,
  title={Area-based breast percentage density estimation in mammograms using weight-adaptive multitask learning},
  author={Gudhe, Naga Raju and Behravan, Hamid and Sudah, Mazen and Okuma, Hidemi and Vanninen, Ritva and Kosma, Veli-Matti and Mannermaa, Arto},
  journal={Scientific reports},
  volume={12},
  number={1},
  pages={12060},
  year={2022},
  publisher={Nature Publishing Group UK London}
}
```
