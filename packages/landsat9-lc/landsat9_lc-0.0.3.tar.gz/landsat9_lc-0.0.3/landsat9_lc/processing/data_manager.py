import joblib
import json
import pandas as pd

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from config import data_train_config, model_config


def save_labels(le: LabelEncoder, values) -> None:
    save_path = model_config.path_label_encoder
    encoding_dict = {}
    for value in values:
        encoding_dict[value] = int(le.transform([value])[0])

    encoding_dict = json.dumps(
        encoding_dict,
        ensure_ascii=False,
        indent=4
    )
    with open(save_path, 'w', encoding=model_config.json_encoding) as f:
        f.write(encoding_dict)


def load_labels() -> dict:
    save_path = model_config.path_label_encoder
    with open(save_path, 'r', encoding='ISO-8859-1') as f:
        encoding_dict = json.load(f)
    return encoding_dict


def load_dataset(file_name: str) -> pd.DataFrame:
    # TODO esto debería estar en un s3 por que github lo rechaza.
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
    for column in columns:
        if input_data[column].dtype.kind not in 'iuf':
            raise ValueError(f"The column {column} is not numeric")


def load_pipeline() -> Pipeline:
    """Loads the latest saved pipeline."""
    save_path = Path(f"{model_config.full_path}")
    return joblib.load(save_path)
