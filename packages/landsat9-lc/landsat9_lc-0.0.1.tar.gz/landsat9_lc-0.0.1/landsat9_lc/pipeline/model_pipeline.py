import xgboost as xgb

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, RobustScaler, QuantileTransformer
from feature_engine.wrappers import SklearnTransformerWrapper
from feature_engine.imputation import MeanMedianImputer
from sklearnex import patch_sklearn

from .spyndex_transformer import IndexTransformer
from config import model_config, data_train_config

patch_sklearn()

pipeline = Pipeline([
    ('mmi_1', MeanMedianImputer(imputation_method='mean', variables=data_train_config.input_columns)),
    ('it', IndexTransformer(indices=model_config.indexes_columns)),
    ('mmi_2', MeanMedianImputer(
        imputation_method='mean',
        variables=model_config.indexes_columns + data_train_config.input_columns)),
    ('rs', SklearnTransformerWrapper(
        RobustScaler(),
        variables=data_train_config.input_columns + model_config.indexes_columns)),
    ('mms', SklearnTransformerWrapper(
        MinMaxScaler(clip=True),
        variables=model_config.indexes_columns + data_train_config.input_columns)),
    ('qt', SklearnTransformerWrapper(
        QuantileTransformer(output_distribution='normal', random_state=42),
        variables=model_config.indexes_columns + data_train_config.input_columns)),
    ('pca', PCA(n_components=model_config.pca_components, random_state=42)),
    ('xgb', xgb.XGBClassifier(
        n_estimators=model_config.xgb_n_estimators,
        max_depth=model_config.xgb_max_depth,
        subsample=model_config.xgb_sub_sample,
        gamma=model_config.xgb_gamma,
        min_child_weight=model_config.xgb_min_child_weight,
        objective=model_config.xgb_objective,
        n_jobs=-1,
    ))]
)

