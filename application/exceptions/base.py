class ApplicationException(Exception):
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"
