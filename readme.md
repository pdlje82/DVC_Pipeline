## Preparation

### 1. Clone this repository
```bash
git clone https://github.com/pdlje82/DVC_Pipeline.git
cd DVC_Pipeline/
```

### 2. Create and activate virtual environment
Create virtual environment named `venv_DVCpipeline` using conda (slow but less prone to crash)
- installs into conda directory
```bash
conda env create -f conda_env.yml --name venv_DVCpipeline -y
conda activate venv_DVCpipeline
````
Or use python venv (fast but more prone to crash)
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

Add Virtual Environment to Jupyter Notebook
```bash
python -m ipykernel install --user --name=dvc_pipeline
```
Configure ToC for jupyter notebook (optional)

```bash
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main
```

### 3. Clone the yolov5 model
```bash
cd model/
git clone https://github.com/ultralytics/yolov5
cd yolov5/
pip install -r requirements.txt
```
### 4. Run Jupyter Notebook
```bash
jupyter notebook
```