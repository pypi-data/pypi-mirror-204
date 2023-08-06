from pydantic import BaseSettings
from typing import List, Dict, Union
from pathlib import Path
from .package import package_config


class Model(BaseSettings):
    model_folder: str = str(Path(__file__).parent.parent / 'landsat9_lc' / 'models')
    model_name: str = f'pipeline_{package_config.version}'
    model_extension: str = '.pkl'
    model_version: str = package_config.version

    indexes_columns: List[str] = [
        'AFRI1600', 'MNDVI', 'MNLI', 'MRBVI', 'NDVI', 'NDTI', 'NDVIMNDWI', 'NDWI', 'NDWIns', 'NWI',
        'BAI', 'BAIM', 'CSI', 'CSIT', 'NDVIT', 'SAVIT', 'VI6T', 'NBSIMS', 'NDSI', 'NDSII', 'NDSInw', 'S3', 'SWI',
        'BLFEI', 'BRBA', 'DBI', 'NBUI', 'VgNIRBI', 'VrNIRBI', 'BI', 'BaI', 'DBSI', 'EMBI', 'NSDSI1', 'NSDSI2',
        'NSDSI3',
    ]
    pca_components: int = 7
    xgb_n_estimators: int = 59
    xgb_max_depth: int = 12
    xgb_min_child_weight: int = 4
    xgb_sub_sample: float = 0.973756
    xgb_gamma: float = 0.146554
    xgb_objective: str = 'multi:softmax'
    # TODO current_test with outpreprocessing on cv = 0.71
    # TODO current_train on cv = 0.91
    json_encoding = 'utf8'

    @property
    def full_path(self) -> str:
        return f"{self.model_folder}/{self.model_name}{self.model_extension}"

    @property
    def path_label_encoder(self) -> str:
        return f"{self.model_folder}/label_encoder.json"


model_config = Model()
