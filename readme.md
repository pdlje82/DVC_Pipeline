## Preparation

### 1. Clone this repository
```bash
git clone https://github.com/pdlje82/DVC_Pipeline.git
cd DVC_Pipeline/
```

### 2. Create and activate virtual environment
Create virtual environment named `dvc_pipeline`
```bash
python3 -m venv dvc_pipeline
echo "export PYTHONPATH=$PWD" >> dvc_pipeline-venv/bin/activate
source dvc_pipeline-venv/bin/activate
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