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
    try:
        return float(tp + tn) / (tp + tn + fp + fn)
    except ZeroDivisionError:
        return 0



def precision(tp, fp):
    """
    Computes precision

    Args:
        tp (int): true positive
        fp (int): false positive

    Returns:
        float: precision
        """
    try:
        return float(tp) / (tp + fp)
    except ZeroDivisionError:
        return 0


def recall(tp, fn):
    """
    Computes precision

    Args:
        tp (int): true positive
        fn (int): false negative

    Returns:
        float: precision
    """
    try:
        return float(tp) / (tp + fn)
    except ZeroDivisionError:
        return 0


def specificity(tn, fp):
    """
    Computes specificity

    Args:
        tn (int): true negative
        fp (int): false positive

    Returns:
        float: precision
        """
    try:
        return float(tn) / (tn + fp)
    except ZeroDivisionError:
        return 0

def f1 (p, r):
    """
    Computes F1

    Args:
        p (float): precision
        r (float): recall

    Returns:
        float: F1
        """
    try:
        return 2 * (p*r) / (p+r)
    except ZeroDivisionError:
        return 0


