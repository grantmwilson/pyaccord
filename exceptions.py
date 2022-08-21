class NoPyaccordClientProvidedError(Exception):
    """Raised when there is no pyaccord client but one is required for the command."""
    pass
