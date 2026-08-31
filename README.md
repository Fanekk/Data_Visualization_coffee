# Data Visualization & Coffee Survey Analysis ☕📊

Repository containing my Data Visualization project.

---

## 📂 Project Structure

```text
├── Datasets/
│   ├── coffe_project.csv   # Raw coffee survey dataset
│   └── coffee_renamed.csv  # Cleaned coffee survey dataset
├── Notebooks/
│   └── Coffee_project.ipynb # Exploratory data analysis & preprocessing
├── Scripts/
│   └── app.py              # Interactive Dash web dashboard
├── requirements.txt        # Python package dependencies
└── .gitignore              # Ignored files & virtual environments
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.9+** installed.

### 2. Setup Virtual Environment
```bash
# Clone repository
git clone https://github.com/Fanekk/Data_Visualization_coffee.git
cd Data_Visualization_coffee

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📈 Running the Dash Web Application

To start the interactive coffee dashboard:

```bash
cd Scripts
python3 app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:8050/
```

### Dashboard Features:
* **Demographics & Spend**: Distribution of age groups, monthly spending, and daily cups.
* **Brewing Methods**: Home brewing preferences vs. on-the-go purchasing habits.
* **Taste Test Results**: Breakdown of blind coffee taste tests and willingness to pay.
* **Interactive Filters**: Dynamic filtering and responsive Plotly charts.

---

## 🛠️ Built With
* **Python 3**
* **Dash** & **Plotly** (Interactive Web Visualizations)
* **Pandas** & **NumPy** (Data Manipulation & Cleaning)
* **Jupyter Notebooks** (Exploratory Data Analysis)
* **Seaborn** & **Matplotlib** (Statistical Plots)

---

## 👤 Author
* **Franek Apanowicz** - [@Fanekk](https://github.com/Fanekk)
