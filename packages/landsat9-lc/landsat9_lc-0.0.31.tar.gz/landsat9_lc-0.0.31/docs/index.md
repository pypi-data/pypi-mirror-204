# Welcome to landsat9_lc's documentation!

`landsat9_lc` is a Python package created for aiming geospatial scientist 
classifying Landsat 9 imagery. It is currently under development. 
The package is designed to be used with the actual data analysis ecosystem of python, 
and geospatial ecosystem of `pangeo` with the use of `xarray`. All you need to know is a 
Landsat 9 identifier and the coordinates of the top left of your image.

`landsat9_lc` uses `planetary_computer` and `pystac` to access the data. You can also 
use your own data of pixel values, but they must come in `pd.DataFrame` format, the classifier
expects the following columns: `coastal`, `blue`, `green`, `red`, `nir08`, `swir16`, `swir22`
which are the name of the bands in `stac`.


The supported classes are:

| Class                           | Description                    | Value |
|---------------------------------|--------------------------------|-------|
| Water                           | Water                          | 0     |
| Forest                          | Cloud                          | 1     |
| Ice/Snow                        | Ice/Snow                       | 2     |
| Clouds                          | Clouds                         | 3     |
| Noise                           | Noise                          | 4     |
| Cloud Shadow                    | Cloud Shadow                   | 5     |
| Agriculture                     | Agriculture                    | 6     |
| Open space with low vegetation  | Open Space with low vegetation | 7     |
| Open space with vegetation      | Open Space with vegetation     | 8     |
| Artificial Zones                | Artificial Zones               | 9     |
| Wetlands                        | Wetlands                       | 10    |
