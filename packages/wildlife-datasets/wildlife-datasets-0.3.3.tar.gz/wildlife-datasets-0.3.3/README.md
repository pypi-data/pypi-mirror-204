# Wildlife Re-Identification (Re-ID) Datasets

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/WildlifeDatasets/wildlife-datasets/blob/main/LICENSE)
[![](https://img.shields.io/badge/docs-stable-blue.svg)](https://wildlifedatasets.github.io/wildlife-datasets/)

The aim of the project is to provide comprehensive overview of datasets for wildlife individual re-identification and an easy-to-use package for developers of machine learning methods. The core functionality includes:

- overview of 31 publicly available wildlife re-identification datasets.
- utilities to mass download and convert them into a unified format.
- default splits for several machine learning tasks including the ability create additional splits.
- evaluation metrics for closed-set and open-set classification.


## Summary of datasets

The package is able to handle the following datasets. We include basic characteristics such as publication years, number of images, number of individuals, dataset time span (difference between the last and first image taken) and additional information such as source, number of poses, inclusion of timestamps, whether the animals were captured in the wild and whether the dataset contain multiple species.

Graphical summary of datasets is located in a [Jupyter notebook](notebooks/dataset_descriptions.ipynb). Due to its size, it may be necessary to view it via [nbviewer](https://nbviewer.org/github/WildlifeDatasets/wildlife-datasets/blob/main/notebooks/dataset_descriptions.ipynb).

![](images/Datasets_Summary.png)


<table border="0" cellspacing="100">
  <tbody style="font-size: 6px" >
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr style="height:8px">
    <td>AAUZebraFishID</td>
    <td>2020</td>
    <td>6672</td>
    <td>6</td>
    <td>1 day</td>
    <td>video</td>
    <td>double</td>
    <td>✔</td>
    <td>✔</td>
    <td>✔</td>    
  </tr>
  <tr style="height:8px">
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr style="height:8px">
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr style="height:8px">
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  </tbody>
</table> 


## Installation

The installation of the package is simple by
```
pip install wildlife-datasets
```


## Basic functionality

We show an example of downloading, extracting and processing the MacaqueFaces dataset.

```
from wildlife_datasets import analysis, datasets

datasets.MacaqueFaces.get_data('data/MacaqueFaces')
dataset = datasets.MacaqueFaces('data/MacaqueFaces')
```

The class `dataset` contains the summary of the dataset. The content depends on the dataset. Each dataset contains the identity and paths to images. This particular dataset also contains information about the date taken and contrast. Other datasets store information about bounding boxes, segmentation masks, position from which the image was taken, keypoints or various other information such as age or gender.

```
dataset.df
```

![](images/MacaqueFaces_DataFrame.png)

The dataset also contains basic metadata including information about the number of individuals, time span, licences or published year.

```
dataset.metadata
```

![](images/MacaqueFaces_Metadata.png)

This particular dataset already contains cropped images of faces. Other datasets may contain uncropped images with bounding boxes or even segmentation masks.

```
analysis.plot_grid(dataset.df, 'data/MacaqueFaces')
```

![](images/MacaqueFaces_Grid.png)

## Additional functionality

For additional functionality including mass loading, datasets splitting or evaluation metrics we refer to the [documentation](https://wildlifedatasets.github.io/wildlife-datasets/).




<div class="foo">

|                                  | <font size="2">Release | <font size="2">#Imgs | <font size="2">#Ind | <font size="2">Span      | <font size="2">Source | <font size="2">Pose   | <font size="2">Timestamp | <font size="2">Wild | <font size="2">MultiSpecies |
|----------------------------------|------------------------|---------------------:|--------------------:|--------------------------|-----------------------|-----------------------|--------------------------|---------------------|-----------------------------|
| <font size="1">AAUZebraFishID    | <font size="1">2020    |  <font size="1">6672 |    <font size="1">6 | <font size="1">1 day     | <font size="1">video  | <font size="1">double | <font size="1">✔         |                     |                             |
| <font size="1">AerialCattle 2017 | <font size="1">2017    | <font size="1">46340 |   <font size="1">23 | <font size="1">1 day     | <font size="1">video  | <font size="1">single | <font size="1">✔         |                     |                             |
| <font size="1">ATRW              | <font size="1">2019    |  <font size="1">5415 |  <font size="1">182 | <font size="1">short     | <font size="1">video   | <font size="1">double | <font size="1">✔         |                     |                             |
| <font size="1">BelugalD          | <font size="1">2022    |  <font size="1">5902 |  <font size="1">788 | <font size="1">2.1 years | <font size="1">photo  | <font size="1">single | <font size="1">✔         |                     |                             |
</div>