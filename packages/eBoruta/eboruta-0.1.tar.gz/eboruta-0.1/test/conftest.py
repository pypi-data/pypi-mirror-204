import pytest
from sklearn.datasets import make_classification, make_regression


@pytest.fixture
def sample_cls_data():
    return make_classification()


@pytest.fixture
def regression_data():
    pass
