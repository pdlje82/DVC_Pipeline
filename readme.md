## Preparation

### 1. Clone this repository
```bash
git clone https://github.com/pdlje82/DVC_Pipeline.git
cd DVC_Pipeline/
```

### 2a. Install conda and mamba (==fast conda) (optional)
- Download and install Miniforge
- Linux
```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b - p /workspace # set you install dir here
echo 'export PATH="/workspace/miniforge3/bin:$PATH"' >> ~/.bashrc # adjust path according to your install
```
- Win 
  - assumes you have git bash installed
```bash
curl -LO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
start Miniforge3-Windows-x86_64.exe
echo 'export PATH="/path/to/miniforge3/Scripts:$PATH"' >> ~/.bash_profile # adjust path according to your install
conda init bash
source ~/.bash_profile

```
#### 2a.1 Create and activate virtual environment with conda
Create virtual environment named `venv_DVCpipeline` using conda (slow but less prone to crash)
- see bottom of this file how to install the via mamba (==fast conda)
```bash
conda env create -f conda_env.yml --name venv_DVCpipeline -y 
# OR, if you installed miniforge
mamba env create -f conda_env.yml --name venv_DVCpipeline
# then
conda activate venv_DVCpipeline
````
### 2b. (Alternative) Create and activate virtual environment with venv
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

### 3. Add Virtual Environment to Jupyter Notebook
```bash
python -m ipykernel install --user --name=dvc_pipeline
```
### 4. (Optional) Configure ToC for jupyter notebook

```bash
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main
```

### 5. Clone the yolov5 model
```bash
cd model/
git clone https://github.com/ultralytics/yolov5
cd yolov5/
pip install -r requirements.txt
```

### 6. Run Jupyter Notebook
```bash
jupyter notebook
```