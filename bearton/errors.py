"""File defining Bearto-specific exceptions.
"""

class BeartonError(Exception):
    """Base class for all Bearton-specific exceptions.
    """
    pass


class BeartonEnvironmentError(BeartonError):
    """Raised when something related to Bearton-specific environment goes wrong.
    """
    pass

class RepositoryNotFoundError(BeartonEnvironmentError):
    pass

class SchemesDirectoryNotFoundError(BeartonEnvironmentError):
    pass

class SchemePathNotFoundError(BeartonEnvironmentError):
    pass

class UIDescriptionsNotFoundError(BeartonEnvironmentError):
    pass
