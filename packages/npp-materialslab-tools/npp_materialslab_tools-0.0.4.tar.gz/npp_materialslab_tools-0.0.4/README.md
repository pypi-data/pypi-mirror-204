# npp_materialslab_tools

This is a repository for the materials lab at HMU.

It contains a number of utilities for the easier (and verified) calcualation of properties from the tests that are normally carried out. 

It contains:
- Tensile testing with the Imada MX2 universal testing machine
  - a quick utility based on a matplotlib window
  - a tk mvc controller window with more capabilities
- Digital image correlation:
  - a complete dic solution for processing and syncing data
- Tektronix dmm 4020 Digital multimeter function
  - for logging data (simple script) 

Plans:

- add a OOP DIC processing .
- 
Author: Nikolaos Papadakis



# installation

cd to the directory and execute

> python setup.py install
> python setup.py develop

or (when loaded to pypi)

> pip install npp_materialslab_tools

to use it import:

> import npp_materialslab_tools as mlt

#  Installation procedure using Conda

## creating a new environment (recommended)

This is the recommended method.

```bash
> conda create -n materialslab python=3
> conda activate materialslab 

```

Alternatively *if you are running low on space on a SSD * drive you can use the prefix option (**IMPORTANT:** read through the following [StackOverflow Question: how to specify new environment location for conda create](https://stackoverflow.com/questions/37926940/how-to-specify-new-environment-location-for-conda-create))


## Install dependencies

Activate the new conda environment and install the following:

```bash
> conda activate materialslab
> conda install opencv numpy scipy
> conda install matplotlib  pandas seaborn
> conda install ipython jupyter
> conda install openpyxl
```


## Install materialslab package.

### from source

Clone the repository from online to <hmu.materialslab.tools>.

Change directory into **<hmu.materialslab.tools>/pypkg/**

> cd ./pypkg

Install the package locally:

> python setup.py install

### from pypi (not yet implemented)

This will be simpler but not yet implemented

```bash
> pip install materialslab-whatevername
```
