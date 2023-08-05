from msb_exceptions import ApiException


class MsbAuthExceptions:
	class AuthenticationFailed(ApiException):
		"""
			general exception that user needs to see
		"""
		_message = "Authentication failed."
		_code = 640

	class InvalidRequestParameters(ApiException):
		"""
		If failed to build the auth data
		"""
		_message = "Invalid request parameters."
		_code = 641
