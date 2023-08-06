from sklearn.preprocessing import LabelEncoder
from config import data_train_config
from landsat9_lc.pipeline import pipeline
from landsat9_lc.processing.data_manager import load_dataset, save_pipeline, save_labels


def get_labels(y):
    le = LabelEncoder()
    y_trans = le.fit_transform(y)
    save_labels(le, y.unique().tolist())
    return y_trans


def run_training() -> None:
    data = load_dataset(data_train_config.train_folder.joinpath(data_train_config.train_file))
    x_train = data[data_train_config.input_columns]
    y_train = data[data_train_config.target]
    y_train = get_labels(y_train)
    for column in x_train.columns:
        if column not in data_train_config.input_columns:
            raise ValueError(f"Input data does not have the correct columns expected columns are "
                             f"{data_train_config.input_columns}")
    pipeline.fit(x_train, y_train)
    save_pipeline(pipeline)


if __name__ == '__main__':
    run_training()
