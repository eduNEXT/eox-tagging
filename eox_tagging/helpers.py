"""Helper functions."""


def get_model_name(instance):
    """
    Function to get the name of a class.

    Arguments:
        - instance: instance of the model
    """
    return instance.__class__.__name__
