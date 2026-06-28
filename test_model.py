import numpy as np
from model import train_and_predict, get_accuracy


def test_predictions_not_none():
    """
    Test 1: Sprawdza, czy otrzymujemy jakakolwiek predykcje.
    """
    preds, _ = train_and_predict()
    assert preds is not None, "Predictions should not be None."


def test_predictions_length():
    """
    Test 2: Sprawdza, czy dlugosc listy predykcji jest wieksza od 0
    i czy odpowiada liczbie probek testowych.
    """
    preds, y_test = train_and_predict()
    assert len(preds) > 0, "Predictions list should not be empty."
    assert len(preds) == len(y_test), "Predictions length should match test set length."


def test_predictions_value_range():
    """
    Test 3: Sprawdza, czy wartosci w predykcjach mieszcza sie w zakresie klas (0, 1, 2).
    """
    preds, _ = train_and_predict()
    assert all(p in [0, 1, 2] for p in preds), "All predictions should be in range [0, 1, 2]."


def test_model_accuracy():
    """
    Test 4: Sprawdza, czy model osiaga co najmniej 70% dokladnosci.
    """
    accuracy = get_accuracy()
    assert accuracy >= 0.7, f"Model accuracy {accuracy} is below 70%."