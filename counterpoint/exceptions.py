class CounterpointGenerationError(Exception):
    """Custom exception raised for errors during counterpoint generation."""
    pass

class NoCounterpointFoundError(Exception):
    """Custom exception raised when no valid counterpoint can be found."""
    pass