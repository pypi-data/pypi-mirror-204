from typing import Union, Tuple

import numpy as np
import pandas as pd
import planetary_computer
import pystac
import stackstac
import xarray as xr
import rioxarray  # Not in use, but needed for xarray to use rasterio

from config import x_array_dims, data_train_config


def transforms_xr_to_pandas(array: xr.DataArray,) -> pd.DataFrame:
    __validate_xarray(array)
    __validate_dimensions(array)
    """Transforms a xr.DataArray to a pandas DataFrame."""
    columns = array.coords[x_array_dims.band].values
    shape = array.shape
    array = np.moveaxis(array.data, 0, -1)
    array = array.reshape(shape[1] * shape[2], shape[0])
    array = pd.DataFrame(array, columns=columns.tolist())
    array = __reduce_mem_usage(array)
    return array


def __reduce_mem_usage(dataframe):
    """
    Reduces the memory of a dataframe by changing the data type of the columns.
    Credits to: Kaggle user Guillaume Martin.
    url: https://www.kaggle.com/code/gemartin/load-data-reduce-memory-usage/notebook
    Args:
        dataframe (pd.DataFrame): The dataframe to reduce the memory.
    Returns:
        pd.DataFrame: The dataframe with the reduced memory.
    Raises:
        TypeError: If the df is not a pd.DataFrame.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("The dataframe must be a pd.DataFrame")

    for col in dataframe.columns:
        col_type = dataframe[col].dtype

        if col_type != object:
            c_min = dataframe[col].min()
            c_max = dataframe[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    dataframe[col] = dataframe[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    dataframe[col] = dataframe[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    dataframe[col] = dataframe[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    dataframe[col] = dataframe[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    dataframe[col] = dataframe[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    dataframe[col] = dataframe[col].astype(np.float32)
                else:
                    dataframe[col] = dataframe[col].astype(np.float64)
        else:
            dataframe[col] = dataframe[col].astype('category')
    return dataframe


def convert_numpy_to_xarray(
        array: Union[pd.Series, np.array],
        metadata_array: xr.DataArray,
) -> xr.DataArray:
    """
    Función que convierte un numpy array en un DataArray.

    Args:
        array (Union[pd.Series, np.array]): A pandas series or a numpy array.
        metadata_array (xr.DataArray): An xarray DataArray. This is the DataArray that contains the training_data
            to be used in the prediction.
    Returns:
        xr.DataArray: The DataArray version of parameter `array` with the dimensions and coordinates of
            `metadata_array`.
    Raises:
        TypeError: If `array` is not a `pd.Series`or a `np.array`.
        TypeError: If `metadata_array`is not a `xr.DataArray`
    """
    if not isinstance(array, pd.Series) and not isinstance(array, np.ndarray):
        raise TypeError('`array` parameter must be a `pd.Series` or a `np.array`')
    elif isinstance(array, np.ndarray) and array.ndim != 1:
        raise TypeError('`array` numpy array has no dimension == 1, try using ravel()')
    elif not isinstance(metadata_array, xr.DataArray):
        raise TypeError('`metadata_array` parameter must be an `xr.DataArray`')

    y_shape = metadata_array.shape[1]
    x_shape = metadata_array.shape[2]

    y_dim = metadata_array.dims[1]
    x_dim = metadata_array.dims[2]

    if isinstance(array, pd.Series):
        data = array.to_numpy().reshape(y_shape, x_shape)
    else:
        data = array.reshape(y_shape, x_shape)

    da = xr.DataArray(
        data=data,
        dims=(y_dim, x_dim),
        coords={
            y_dim: metadata_array[y_dim].data,
            x_dim: metadata_array[x_dim].data
        },
        attrs=metadata_array.attrs
    )
    da.rio.write_crs(metadata_array.rio.crs, inplace=True)
    return da


def obtain_stac(
        scene_id: str,
        x_min: int,
        y_max: int,
        pixels: int = 800,
) -> xr.DataArray:
    """Make a prediction using a saved model pipeline."""
    url = f"https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2/items/{scene_id}"
    item = pystac.Item.from_file(url)
    signed_item = planetary_computer.sign(item)
    signed_item = stackstac.stack(signed_item)
    __validate_time_values(signed_item, scene_id)
    date_string = np.datetime_as_string(signed_item.time.values[0])
    x_range, y_range = __ranges_by_xmin_ymax(
        x_min=x_min,
        y_max=y_max,
        pixels=pixels
    )
    return signed_item.sel(band=data_train_config.input_columns).sel(
        time=date_string,
        x=x_range,
        y=y_range,
        method='nearest'
    )


def __validate_time_values(item: xr.DataArray, scene_id: str) -> None:
    if len(item.time.values) > 1:
        raise ValueError(f"Input data has more than one time value which is not possible. Are you sure that's the "
                         f"correct {scene_id}?")


def __ranges_by_xmin_ymax(
        x_min: int,
        y_max: int,
        pixels: int = 800,
        step: int = 30
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates the ranges of coordinates to search given x_min and y_max. The ranges are created taking into
    account that the size of the image in this x axis is 1600 pixels by default (this value is for easy processing and
    futher training).

    Args:
        x_min (int): The minimum value of the x axis.
        y_max (int): The maximum value of the y axis.
        pixels (int): The number of pixels to create the array. By default is 1600.
        step (int): The step to create the array. By default is 30. which is the size of the pixel
        of a Landsat image.
    Return:
        Tuple[float, float]: range of coordinates.
    Raises:
        TypeError: If x_min is not an integer.
        TypeError: If y_max is not an integer.
        TypeError: If step is not an integer.
    """
    __validate_integer(x_min, y_max, step, pixels)
    x_axes_array = np.arange(x_min, x_min + pixels * step, step)
    y_axes_array = np.arange(y_max, y_max - (pixels * step), - step)

    # Create the `y_axes_array` in ascending order
    y_axes_array = y_axes_array[::-1]
    return x_axes_array, y_axes_array


def __validate_integer(*numbers: int) -> None:
    """
    Validates that all input numbers are integers.

    Args:
        numbers (int): One or multiple integers to validate.
    Returns:
        None
    Raises:
        TypeError: If any of the input numbers is not an integer.
    """
    for i, number in enumerate(numbers):
        if not isinstance(number, int):
            raise TypeError(f"The number {i} must be an integer, but got {type(number).__name__} instead")


def __validate_xarray(array: xr.DataArray) -> None:
    """
    Validates that the input `array` is a xr.DataArray.
    Args:
        array (xr.DataArray): The array to validate

    Returns:
        None

    Raises:
        TypeError: If array is not a xr.DataArray.
    """
    if not isinstance(array, xr.DataArray):
        raise TypeError("The array must be a xr.DataArray")


def __validate_dimensions(array: xr.DataArray) -> None:
    """
    Validates that the used dimensions are according to pystac conventions.
    Args:
        array (xr.DataArray): The array to validate
    Returns:
        None
    Raises:
        ValueError: If some of the dimensions is not present in the `array`.
    """
    for dimension in ['x', 'y', 'band']:
        if dimension not in array.dims:
            raise ValueError(f"The dimension {dimension} is not present in the array")


def verify_columns(df: pd.DataFrame) -> None:
    """
    Verifies that the input dataframe has the required columns to make a prediction.
    Args:
        df (pd.DataFrame): The dataframe to validate.
    Returns:
        None
    Raises:
        ValueError: If the dataframe doesn't have the required columns.
    """
    for column in data_train_config.input_columns:
        if column not in df.columns:
            raise ValueError(f"The dataframe must have the column {column} to make a prediction")
