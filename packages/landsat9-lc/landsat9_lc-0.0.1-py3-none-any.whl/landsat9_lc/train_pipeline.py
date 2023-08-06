from sklearn.preprocessing import LabelEncoder
from config import data_train_config
from src.landsat9_lc.pipeline import pipeline
from src.landsat9_lc.processing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    data = load_dataset(data_train_config.train_folder.joinpath(data_train_config.train_file))
    x_train = data[data_train_config.input_columns]
    y_train = data[data_train_config.target]
    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    pipeline.fit(x_train, y_train)
    save_pipeline(pipeline)


if __name__ == '__main__':
    run_training()