from pathlib import Path
from typing import List

from pydantic import BaseSettings


class DataTrain(BaseSettings):
    train_folder = Path(__file__).parent.parent / 'data'
    train_file = 'full_cluster_1_percent.parquet'
    target = 'cobertura'
    input_columns: List[str] = ['coastal', 'blue', 'red', 'green', 'nir08', 'swir16', 'swir22', 'lwir11']


data_train_config = DataTrain()
