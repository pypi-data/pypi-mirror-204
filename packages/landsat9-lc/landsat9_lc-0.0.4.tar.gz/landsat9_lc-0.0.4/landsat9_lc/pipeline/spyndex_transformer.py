import numpy as np
import spyndex
from sklearn.base import BaseEstimator, TransformerMixin


class IndexTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, indices):
        self.indices = indices

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.astype(np.float64)
        self.params = {
            "A": X.coastal,
            "B": X.blue,
            "G": X.green,
            "R": X.red,
            "N": X.nir08,
            "S1": X.swir16,
            "S2": X.swir22,
            "T1": X.lwir11,
            "T": X.lwir11,
            "gamma": spyndex.constants.gamma.value,
            "sla": spyndex.constants.sla.value,
            "slb": spyndex.constants.slb.value,
            "alpha": spyndex.constants.alpha.value,
            "g": spyndex.constants.g.value,
            "C1": spyndex.constants.C1.value,
            "C2": spyndex.constants.C2.value,
            "omega": spyndex.constants.omega.value,
            "L": spyndex.constants.L.value,
            "nexp": spyndex.constants.nexp.value,
            "cexp": spyndex.constants.cexp.value,
            "fdelta": spyndex.constants.fdelta.value,
            "beta": spyndex.constants.beta.value,
        }

        X[self.indices] = spyndex.computeIndex(self.indices, self.params)
        X = self._drop_nans(X)

        X['tass_veg'] = (-0.2848 * X['blue']) - (0.2435 * X['green']) - (0.5436 * X['red']) + (0.7243 * X['nir08']) + (
                    0.0840 * X['swir16']) - (0.18 * X['swir22'])
        X['tass_wet'] = (0.1509 * X['blue']) + (0.1973 * X['green']) + (0.3279 * X['red']) + (0.3406 * X['nir08']) - (
                    0.7112 * X['swir16']) - (0.4572 * X['swir22'])
        X['fe2'] = (X['swir22'] / X['nir08']) + (X['green'] / X['red'])
        X['fe3'] = X['red'] / X['green']
        X['ferric_oxides'] = X['swir16'] / X['nir08']
        X['ferric_iron'] = (X['swir22'] / X['nir08']) + (X['green'] / X['red'])
        X['ferric_silicates'] = (X['swir22'] / X['swir16'])
        X = X.replace([np.inf, -np.inf], 0)

        return X

    def _drop_nans(self, X, percentage: float = 0.5):
        null_percentage = X.isna().mean()
        columns_to_drop = null_percentage[null_percentage >= percentage].index
        return X.drop(columns_to_drop, axis=1)