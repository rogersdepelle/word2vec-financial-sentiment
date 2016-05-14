"""metrics.py: defines the metrics used to evaluate our system."""

__author__      = "Edimar Manica"


def accuracy(tp, tn, fp, fn):
    """
    Computes accuracy

    Args:
        tp (int): true positive
        tn (int): true negative
        fp (int): false positive
        fn (int): false negative

    Returns:
        float: accuracy
    """
    return float(tp + tn) / (tp + tn + fp + fn)


def precision(tp, fp):
    """
    Computes precision

    Args:
        tp (int): true positive
        fp (int): false positive

    Returns:
        float: precision
        """
    return float(tp) / (tp + fp)


def recall(tp, fn):
    """
    Computes precision

    Args:
        tp (int): true positive
        fn (int): false negative

    Returns:
        float: precision
    """
    return float(tp) / (tp + fn)

def specificity(tn, fp):
    """
    Computes specificity

    Args:
        tn (int): true negative
        fp (int): false positive

    Returns:
        float: precision
        """
    return float(tn) / (tn + fp)

def f1 (p, r):
    """
    Computes F1

    Args:
        p (float): precision
        r (float): recall

    Returns:
        float: F1
        """
    return 2 * (p*r) / (p+r)

