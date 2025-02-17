import numpy as np
import pandas as pd
from colorama import Fore, Style


def preprocess_features(X: pd.DataFrame) -> np.ndarray:
    def transform_categorical_preprocessor():
        """
        Scikit-learn pipeline that transforms a cleaned dataset of shape (_, 7)
        into a preprocessed one of fixed shape (_, 65).

        Stateless operation: "fit_transform()" equals "transform()".
        """
        categorical_features = ['brand', 'currency', 'collection', 'life_span']

        encoder =  pd.get_dummies(X, columns=categorical_features, drop_first=True)
        result = encoder.fit_transform(X)

        return result

    print(Fore.BLUE + "\nPreprocessing features..." + Style.RESET_ALL)

    preprocessor = transform_categorical_preprocessor()
    X_processed = preprocessor.fit_transform(X)

    print("✅ X_processed, with shape", X_processed.shape)

    return X_processed
