# python-matching-project

This project matches training data to ideal mathematical functions using least squares, maps test pounts based on deviation thresholds, saves results to a database, and visualizes the outcomes.

---

## Features
- Object-oriented design with inheritance
- Data loading and transformation using **pandas**
- Data storage via **SQLAlchemy** to SQLite databases
- **Matplotlib** and **Bokeh** visualizations
- Exception handling with custom error classes
- Unit testing for all core components
- Results are saved, visualized, and available for inspection

---

## Project Structure
.
├── data/                 # Input Excel files: train.xlsx, ideal.xlsx, test.xlsx
├── database/             # SQLite databases: functions.db, results.db
├── plots/                # Saved plots (matplotlib + Bokeh)
│   └── bokeh/            # Bokeh-generated HTML visualizations
├── src/
│   ├── models/           # SQLAlchemy ORM models
│   ├── init.py
│   ├── create_tables.py
│   ├── db.py
│   ├── data_handler.py
│   ├── exceptions.py
│   ├── load_data.py
│   ├── save_utils.py
│   └── visualize.py
├── tests/                # Unit tests
├── main.py               # Main program pipeline
├── cleanup_db.py         # Utility to clean/reset databases
└── README.md

---
## Technologies Used
- Python 3.11
- Pandas
- SQLAlchemy
- Matplotlib
- Bokeh
- Pytest
---

---
## How to Run
1. ** Install dependencied **
   ```bash
   pip install -r requirements.txt
---

---
## Run main program
python main.py
---

---
## Run unit tests
pytest -v
---

---
## Contributions

# Clone the repository
git clone https://github.com/irisasteve1/python-matching-project.git
cd python-matching-project

# Create a feature branch
git checkout -b feature/your-feature

# After making changes
git add .
git commit -m "Add new feature"
git push origin feature/your-feature
---
