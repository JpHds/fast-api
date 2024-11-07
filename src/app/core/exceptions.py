from fastapi import HTTPException, status


class ClientNotFoundException(HTTPException):
    def __init__(self, detail: str = "Cliente não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
