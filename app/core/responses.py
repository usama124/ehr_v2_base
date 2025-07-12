from http import HTTPStatus

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic.json import pydantic_encoder


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class SuccessResponse(CustomException):
    code = HTTPStatus.OK
    error_code = HTTPStatus.OK
    message = HTTPStatus.OK.description


class TokenExpired(CustomException):
    def __init__(self, message="The authentication token has expired."):
        self.code = 498
        self.error_code = 498
        self.message = message
        super().__init__(self.message)


class ApiCustomResponse:
    @staticmethod
    def get_response(data=None, message="Success", status_code=HTTPStatus.OK):
        response_data = {
            "status_code": status_code,
            "message": message,
            "data": jsonable_encoder(data) if data is not None else []
        }
        return JSONResponse(content=response_data, status_code=status_code)
