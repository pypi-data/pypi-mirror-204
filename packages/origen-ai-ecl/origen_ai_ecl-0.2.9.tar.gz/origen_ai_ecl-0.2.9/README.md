# opm-origen
### Bulding with docker-compose

First, create an env variables file by copying `config.env.example` into `config.env`:

```bash
$> cp config.env.example config.env
```

If you wish to publish the package in pypi, you will have to obtain a pypi token and set the environment variable
`PYPI_API_TOKEN` in `config.env`.

After that, you can simply use docker-compose to run commands:

```bash
docker-compose run build 
```

### Building the package without docker/docker-compose

## Prerequisites

- Install make, cmake and g++
- Build/Install Opm-Common
- Build/Install Opm-Grid

## Install opm packages

```bash
sudo apt-add-repository ppa:opm/ppa
sudo apt-get update

sudo apt-get install libopm-common-dev
sudo apt-get install libopm-grid-dev
```

## How to build

```bash
git clone git@github.com:OriGenAI/opm-origen.git
cd opm-origen
mkdir build
cd build
cmake ..
make
```

## How to use

- Copy the binary under `build/lib` folder
- Import the binary from your Python code
- Call the library functions

### Examples

```python
from origen.ai.ecl import read_transmissibility

trans = read_transmissibility("path-to-data.DATA")
print(trans)
```

### Develop

You can use the main.cpp file to debug. Just call your function from there and compile the code. You will find the binary in `build/bin/main`
