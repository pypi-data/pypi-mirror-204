import pandas as pd
import pytest

from landsat9_lc.processing.utils import obtain_stac, __ranges_by_xmin_ymax


@pytest.fixture(scope="module")
def sample_input_data() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "coastal": [1.0, 2.0, 3.0],
            "blue": [5.0, 4.0, 3.0],
            "red": [5.0, 0, 2.0],
            "green": [5.0, 3.0, 3.0],
            "nir08": [5.0, 5.0, 3.0],
            "swir16": [5.0, 5.0, 3.0],
            "swir22": [5.0, 6.0, 3.0],
            "lwir11": [5.0, 2.0, 3.0],
        }
    )
    return df


@pytest.fixture(scope="module")
def wrong_data_type() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "coastal": ['a', 'b', 'c'],
            "blue": ['d', 'e', 'f'],
            "red": [1, 2, 3],
            "green": [1, 2, 3],
            "nir08": [1, 2, 3],
            "swir16": [1, 2, 3],
            "swir22": [1, 2, 3],
            "lwir11": [1, 2, 3],
        }
    )
    return df

@pytest.fixture(scope='module')
def base_pixels():
    return 10


@pytest.fixture(scope='module')
def base_coords():
    return 688635, 476085


@pytest.fixture(scope='module')
def base_id():
    return 'LC09_L2SP_007057_20220108_02_T1'


@pytest.fixture(scope='module')
def ranges_coords(base_coords, base_pixels):
    return __ranges_by_xmin_ymax(
        base_coords[0],
        base_coords[1],
        pixels=base_pixels,
    )


@pytest.fixture(scope='module')
def get_subscene(base_id, base_coords, base_pixels):
    return obtain_stac(
        base_id,
        base_coords[0],
        base_coords[1],
        pixels=base_pixels,
    )
