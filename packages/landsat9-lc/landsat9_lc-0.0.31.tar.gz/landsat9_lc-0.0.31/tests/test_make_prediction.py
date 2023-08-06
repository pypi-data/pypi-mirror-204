import numpy as np
import pytest
import pandas as pd
import xarray as xr

from config import data_train_config, x_array_dims
from landsat9_lc import Landsat9LCClassifier
from landsat9_lc.processing import transforms_xr_to_pandas, obtain_stac


def test_incorrect_input(sample_input_data):
    for column in data_train_config.input_columns:
        sample_input_data = sample_input_data.drop(columns=column, axis='columns')
        with pytest.raises(ValueError):
            # When
            clf = Landsat9LCClassifier()
            clf.make_prediction(sample_input_data)


def test_make_train_prediction(sample_input_data):
    # Given
    clf = Landsat9LCClassifier()
    predictions = clf.make_prediction(sample_input_data)
    # Then
    assert predictions is not None
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(sample_input_data)


def test_incorrect_data_type(wrong_data_type):
    # Given
    clf = Landsat9LCClassifier()
    # Then
    with pytest.raises(ValueError):
        clf.make_prediction(wrong_data_type)


def test_correct_stac_array(get_subscene):
    # Given
    subject = get_subscene
    # Then
    assert subject is not None
    assert isinstance(subject, xr.DataArray)


def test_correct_transformation(get_subscene):
    # Given
    subject = get_subscene
    # When
    subject = transforms_xr_to_pandas(subject)
    # Then
    assert subject is not None
    assert isinstance(subject, pd.DataFrame)
    assert set(subject.columns) == set(data_train_config.input_columns)


def test_make_prediction_from_stac(base_id, base_coords, base_pixels):
    # Given
    clf = Landsat9LCClassifier()
    # When
    predictions = clf.predict_from_stac(base_id, base_coords[0], base_coords[1], base_pixels)
    # Then
    assert predictions is not None
    assert isinstance(predictions, xr.DataArray)


def test_correct_output_obtain_stack(base_id, base_coords, base_pixels):
    # Given
    array = obtain_stac(base_id, base_coords[0], base_coords[1], base_pixels)
    # Then
    assert array is not None
    assert isinstance(array, xr.DataArray)
    assert array.dims == (x_array_dims.band, x_array_dims.y, x_array_dims.x)
    assert set(array.coords[x_array_dims.band].values) == set(data_train_config.input_columns)


def test_correct_output_obtain_pandas(base_id, base_coords, base_pixels):
    dataframe = transforms_xr_to_pandas(obtain_stac(base_id, base_coords[0], base_coords[1], base_pixels))
    # Then
    assert dataframe is not None
    assert isinstance(dataframe, pd.DataFrame)
    assert set(dataframe.columns) == set(data_train_config.input_columns)






