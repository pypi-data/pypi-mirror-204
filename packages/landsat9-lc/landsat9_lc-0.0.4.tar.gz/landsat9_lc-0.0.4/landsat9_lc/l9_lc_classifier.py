import numpy as np
import pandas as pd
import xarray as xr

from landsat9_lc.processing.data_manager import load_pipeline, validate_inputs
from landsat9_lc.processing.utils import (
    transforms_xr_to_pandas, convert_numpy_to_xarray, obtain_stac, verify_columns)


class Landsat9LCClassifier:
    """This class provides methods to make predictions of land cover types from Landsat 9 data.
    It can work with custom pandas dataframes or directly from STAC items.
    """

    def make_prediction(self, input_data: pd.DataFrame) -> np.ndarray:
        """
        Use this method if you have a custom pandas DataFrame that matches the coordinates of the `band` dimension
        of an xarray object obtained by `pystac` and `stacstack`. If these terms are unfamiliar, we recommend
        reviewing the `Microsoft Planetary Computer` documentation. Note that this method loads the entire
        input data into memory, so it is recommended to use smaller portions of the data for larger datasets.

        Parameters
        ----------
        input_data :
            A pandas dataframe with the columns specified in `data_train_config.input_columns`.

        Returns
        -------
        np.ndarray:
            A numpy array with the predictions.

        Raises
        ------
        ValueError
            If the dataframe doesn't have the correct columns.
        """
        verify_columns(input_data)
        pipeline = load_pipeline()
        if isinstance(input_data, pd.DataFrame):
            validate_inputs(input_data)
        # TODO batch predict for memory efficiency
        prediction = pipeline.predict(input_data)
        return prediction

    def predict_from_stac(
            self,
            scene_id: str,
            x_min: int,
            y_max: int,
            pixels: int = 800,
    ) -> xr.DataArray:
        """Use this method if you want to make predictions from a STAC item that is a Landsat9 image.
        by default the amount of pixels in x and y are 800 and are always square (this behaviour shouldnt
        be permanent and it should be one of the first things in coming versions). The suggestion is
        to try to avoid the edges of the image as it can produce not implemented errors and create bad
        predictions.

        If you are note sure about the identifier of the image you cand read Microsoft Planetary Computer
        documentation, of check its datasets, if you are a QGIS user you can also use `STAC API Browser Plugin`.

        Parameters
        ----------
        scene_id :
            The identifier of the STAC item.
        x_min :
            The x coordinate of the top left corner of the subscene.
        y_max :
            The y coordinate of the top left corner of the subscene.
        pixels :
            The amount of pixels in x and y, by default 800

        Returns
        -------
        xr.DataArray:
            A xarray DataArray with the predictions.

        """
        stac = obtain_stac(
            scene_id=scene_id,
            x_min=x_min,
            y_max=y_max,
            pixels=pixels
        )
        stac_df = transforms_xr_to_pandas(stac)
        predictions = self.make_prediction(stac_df)
        return convert_numpy_to_xarray(predictions, stac)
