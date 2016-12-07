# coding: utf-8

__author__ = 'chengchaojie'

from lemon.errors import ErrorDefs


class IntermediateResult:
	def __init__(self, status=True, code=ErrorDefs.ParameterIllegal[0], msg=ErrorDefs.ParameterIllegal[1]):
		self.__success = status
		self.__error_code = code
		self.__error_message = msg

		self.__response = None
		self.content_for_log = None

	def set_status(self, status):
		self.__success = status

		if self.__success:
			self.__error_code = None
			self.__error_message = None
		else:
			self.__error_code = ErrorDefs.ParameterIllegal[0]
			self.__error_message = ErrorDefs.ParameterIllegal[1]


	def set_error(self, error_code, error_message):
		self.__success = False
		self.__error_code = error_code
		self.__error_message = error_message

	def is_success(self):
		return self.__success

	def get_error(self):
		return self.__error_code, self.__error_message

	def get_error_code(self):
		return self.__error_code

	def get_error_message(self):
		return self.__error_message

	@staticmethod
	def get_instance(status=False, error_code=None, error_message=None):

		ecm = IntermediateResult()

		if isinstance(status, bool) and status:
			ecm.__success = True
			return ecm

		if isinstance(status, bool) and isinstance(error_code, int) and isinstance(error_message, str):
			ecm.__error_message = status
			ecm.__error_code = error_code
			ecm.__error_message = error_message
		else:
			ecm.__success = False
			ecm.__error_code = ErrorDefs.ParameterIllegal[0]
			ecm.__error_message = ErrorDefs.ParameterIllegal[1]

		return ecm