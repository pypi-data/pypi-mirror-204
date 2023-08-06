# smartonnx

Tool to convert a ONNX model to Cairo smart contract

## Installation 

Make sure you have the correct Python version (>= 3.7.11 , < 3.9). We recommend [Pyenv](https://github.com/pyenv/pyenv) or similar Python version management tools. 


This project uses [Poetry](https://github.com/python-poetry/poetry) for project management. Install Poetry using the [installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer)

It is preffered to install the dependencies within a virtual environment for the project

Check the current virtual environment (and the alternatives) with 

```Shell
$ poetry env list
```

Select the correct one with 

```Shell
$ poetry env use [name]
```

If the virtual environment is correct, install the dependencies with 

```Shell
$ poetry install
```
and update them if needed with 

```Shell
$ poetry update 
```