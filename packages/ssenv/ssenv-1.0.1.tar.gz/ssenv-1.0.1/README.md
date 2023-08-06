# Super Simple Environment

![Release](https://shields.io/github/v/release/asheswook/Environment?display_name=tag&sort=semver) ![build](https://img.shields.io/github/actions/workflow/status/asheswook/Environment/docker-workflow.yml?branch=main)

Super Duper Simple, Super Duper Easy dotenv (.env) package in Python.

## Feature

- Handle dotenv (.env)
- Import, Load, and Use it now!

## Installation

### Requirements

- Python 3.X

You can just install Environment package by using pip:

```bash
pip install ssenv
```

## Usage

**Import the package**

First, you should import the package and create an instance of Environment class.

```python
import ssenv

env = ssenv.Environment()
```

**Load the dotenv**

You can load the dotenv file by using `load_dotenv()` method. If you want to reload the dotenv file, you can just use `load_dotenv()` method again.

```python
env.load_dotenv()
```

**Use it!**

You can use the dotenv file by using `get()` method. If you want to get the value of the dotenv, you can just use `get()` method with the key of the dotenv. If the dotenv file doesn't have the key, it will return `None`.

```python
pwd = env.get('MY_PASSWORD')
```
