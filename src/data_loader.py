from pathlib import Path
import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"


def load_hospital_data():
    """
    Load all structured hospital data from CSV files.

    Returns:
        dict: DataFrames containing hospital information,
              departments, doctors, schedules and contacts.
    """

    data = {
        "hospital_info": pd.read_csv(DATA_DIR / "hospital_info.csv"),
        "departments": pd.read_csv(DATA_DIR / "departments.csv"),
        "doctors": pd.read_csv(DATA_DIR / "doctors.csv"),
        "doctor_schedule": pd.read_csv(DATA_DIR / "doctor_schedule.csv"),
        "contacts": pd.read_csv(DATA_DIR / "contacts.csv"),
    }

    return data