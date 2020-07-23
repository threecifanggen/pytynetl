class NotIllegalRetryingNumber(Exception):
    """Retrying Time must greater than 0.
    """

class IllegalTypeToCastAsABaseTasker(Exception):
    """Only Callable object can be cast as a BaseTasker
    """
