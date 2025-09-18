# 🚗 V2X Modelisation


[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Mesa](https://img.shields.io/badge/Mesa-Agent--Based%20Modeling-orange)](https://mesa.readthedocs.io/)

Simulation and modeling of **V2V** (Vehicle-to-Vehicle) and **V2I** (Vehicle-to-Infrastructure) communications with defense mechanisms against fake news.  
This project is built with **Python, Flask, and Mesa**.

---

## 🛠️ Requirements

- [Python 3.12](https://www.python.org/downloads/)  
- [Git](https://git-scm.com/)  
- A terminal (PowerShell, Bash, etc.)

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/egerbeaud/V2X_Modelisation.git
```
```bash 
# 2. Move in the repository
cd V2X_Modelisation
```

```bash
# 3. Create a virtual environment
python -m venv venv
```

```bash
# 4. Activate the environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source venv/bin/activate

#Install Graphical backend
sudo apt install python3-tk #(On Linux, if you haven't installed or configured a graphical backend)
```

```bash
# 5. Install dependencies
pip install -r requirements.txt
```
---

## ▶️ Run the project

```bash
# 1. Run the Flask launcher
python flask_launcher.py
```

2. Open your web browser and go to http://localhost:8080
