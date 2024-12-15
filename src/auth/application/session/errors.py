from auth.application.base.errors import ApplicationError


class AuthenticationError(ApplicationError): ...


class AlreadyAuthenticatedError(ApplicationError): ...
