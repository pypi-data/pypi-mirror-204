import xgboost as xgb

from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, RobustScaler, QuantileTransformer
from feature_engine.wrappers import SklearnTransformerWrapper
from feature_engine.imputation import MeanMedianImputer
from .spyndex_transformer import IndexTransformer
from config.model import model_config

pipeline = make_pipeline(
    MeanMedianImputer(imputation_method='mean'),
    SklearnTransformerWrapper(RobustScaler()),
    IndexTransformer(indices=model_config.indexes_columns),
    SklearnTransformerWrapper(RobustScaler()),
    SklearnTransformerWrapper(MinMaxScaler(clip=True)),
    SklearnTransformerWrapper(
        QuantileTransformer(output_distribution='normal', random_state=42)),
    PCA(n_components=0.95, random_state=42),
    xgb.XGBClassifier(
        n_estimators=model_config.xgb_n_estimators,
        max_depth=model_config.xgb_max_depth,
        subsample=model_config.xgb_sub_sample,
        gamma=model_config.xgb_gamma,
        min_child_weight=model_config.xgb_min_child_weight,
        objective=model_config.xgb_objective,
        n_jobs=-1,
    )
)

