from werkzeug.exceptions import HTTPException
from flask import make_response


class BusinessError(HTTPException):
    def __init__(self, error_code, error_message, error_field=None, status_code=400):
        self.response = make_response({
            'error_code': error_code,
            'error_message': error_message,
            'error_field': error_field
        }, status_code)


class ListNotFoundError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-1001', 'List does not exist.', 404)


class ListNotSpecifiedError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-1002', 'List ID is not specified.', 400)


class ListAlreadyExistsError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-1003', 'A list with this name already exists.', 'name', 400)


class ListNameError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-1004', 'List name should not exceed 25 characters.', 'name', 400)


class CardNotFoundError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-2001', 'Card does not exist.', 404)


class CardNotSpecifiedError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-2002', 'Card ID is not specified.', 400)


class CardPastDeadlineError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-2003', 'Card deadline should not be in the past if it is due.', 'deadline', 400)


class CardTitleError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-2004', 'Card title should not exceed 25 characters.', 'title', 400)


class CardContentError(BusinessError):
    def __init__(self):
        super().__init__('ERROR-2005', 'Card content should not exceed 250 characters.', 'content', 400)
