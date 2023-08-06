class PsDeliveryException(Exception):
    pass


class RequestFailed(PsDeliveryException):
    pass


class RequestTimeout(PsDeliveryException):
    pass


class ElementNotFoundError(PsDeliveryException):
    pass


class WebdriverIsNotLoaded(PsDeliveryException):
    pass
