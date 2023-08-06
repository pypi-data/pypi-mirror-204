import joblib
import pandas as pd

from pathlib import Path
from config import data_train_config, model_config
from sklearn.pipeline import Pipeline


def load_dataset(file_name: str) -> pd.DataFrame:
    file_path = Path(__file__).parent.parent / file_name
    # TODO eliminar el sampling ya que esto es solo en el prototipo.
    return pd.read_parquet(file_path)[data_train_config.input_columns + [data_train_config.target]].sample(frac=0.01)


def save_pipeline(pipeline) -> None:
    """Overwrites any previous pipeline."""
    save_path = Path(f"{model_config.full_path}")
    joblib.dump(pipeline, save_path)


def validate_inputs(input_data: pd.DataFrame) -> None:
    """Validate the input data."""
    columns = input_data.columns
    if set(columns) != set(data_train_config.input_columns):
        raise ValueError(f"Input data does not have the correct columns expected columns are "
                         f"{data_train_config.input_columns}")
    # all columns must be numeric
    if not all(input_data[columns].apply(pd.to_numeric, errors='coerce').notnull().all()):
        raise ValueError("Input data contains non-numeric values")


def load_pipeline() -> Pipeline:
    """Loads the latest saved pipeline."""
    save_path = Path(f"{model_config.full_path}")
    return joblib.load(save_path)
