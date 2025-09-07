# file: app/core/exceptions.py

from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    """
    Exception kustom untuk resource yang tidak ditemukan (HTTP 404).
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    """
    Exception kustom untuk request yang tidak valid atau gagal validasi bisnis (HTTP 400).
    """
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ForbiddenException(HTTPException):
    """
    Exception kustom untuk aksi yang tidak diizinkan (HTTP 403).
    """
    def __init__(self, detail: str = "Operation not permitted"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class UnprocessableEntityException(HTTPException):
    """
    Exception kustom untuk data yang valid secara sintaksis tetapi tidak dapat diproses (HTTP 422).
    Berguna untuk validasi logika bisnis yang lebih dalam.
    """
    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)