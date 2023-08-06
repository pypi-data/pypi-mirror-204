from typing import Union

import pandas as pd
import xarray as xr
from src.landsat9_lc.processing.data_manager import load_pipeline, validate_inputs


def make_prediction(input_data: Union[xr.DataArray, pd.DataFrame]) -> xr.DataArray:
    """Make a prediction using a saved model pipeline."""
    pipeline = load_pipeline()
    if isinstance(input_data, pd.DataFrame):
        validate_inputs(input_data)
    # batch predict for memory efficiency
    prediction = pipeline.predict(input_data)
    return prediction