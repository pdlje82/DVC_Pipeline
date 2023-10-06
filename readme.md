
## Preparation
This script assumes that the installation is done on a host with a volume `\workspace`. 
- Everything will be installed into this directory.
- if you use a containerized environment like runpod.io, your permanent volume should have at least 40GB available space

The next steps show how to install the environment. 
- All pipeline components will be executed in the same environment

### 1. Clone this repository
```bash
git clone https://github.com/pdlje82/DVC_Pipeline.git
cd DVC_Pipeline/
```

### 2a. Install conda and mamba (==fast conda) (optional)
- Download and install Miniforge
- Linux
```bash
cd /workspace
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b -p /workspace/miniforge3 # set you install dir here
echo 'export PATH="/workspace/miniforge3/bin:$PATH"' >> ~/.bashrc # adjust path according to your install
```
- Win 
  - assumes you have git bash installed
```bash
curl -LO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
start Miniforge3-Windows-x86_64.exe
echo 'export PATH="/____/____/miniforge3/Scripts:$PATH"' >> ~/.bash_profile # adjust path according to your install
conda init bash
source ~/.bash_profile

```
### 3 Create and activate virtual environment 
- ~ `4GB` download space
- ~ `18GB` install space min.
 
#### 3a Install with conda
Create virtual environment named `venv_DVCpipeline` using conda (slow but less prone to crash)
- see bottom of this file how to install the via mamba (==fast conda)
```bash
conda env create -f conda_env.yml --name venv_DVCpipeline -y 
# OR, if you installed miniforge
mamba env create -f conda_env.yml --name venv_DVCpipeline
# then
conda activate venv_DVCpipeline
````
#### 3.b (Alternative) Install  with venv
python venv (fast but more prone to crash)
- installs into project directory
```bash
python3 -m venv venv_DVCpipeline
# Linux
echo "export PYTHONPATH=$PWD" >> venv_DVCpipeline/bin/activate
source venv_DVCpipeline/bin/activate

# Windows
echo "set PYTHONPATH=%cd%" >> venv_DVCpipeline\Scripts\activate.bat
source venv_DVCpipeline/Scripts/activate
```
Install python libraries
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Add Virtual Environment to Jupyter Notebook
This step also enables the use of the pipeline environment in a preinstalled Jupiter Lab
```bash
python -m ipykernel install --user --name=dvc_pipeline
```

### 5. Clone the yolov5 model
```bash
cd model/
git clone https://github.com/ultralytics/yolov5
git checkout tags/v7.0
```
- requirements are already installed with the environment, if there are problems you could try `cd yolov5/` and `pip install -r requirements.txt`

### 6. Run Jupyter Notebook
If a host like runpod.io is used:
- do NOT execute jupyter from bash
- make use of its integrated Jupyter notebook or Jupyter Lab environment. 
- Connect to it, load the notebook and set the kernel to `dvc_pipeline`

```bash
jupyter notebook 

```