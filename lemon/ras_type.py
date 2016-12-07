# coding: utf-8

__author__ = 'chengchaojie'


class ArchivePrintStatus:
	NOT_UPLOAD_PDF = 1
	DRAFT_PDF = 2
	SENDER_PDF = 3
	RECEIVER_PDF = 4
	READER_PDF = 5

	def __init__(self):
		pass


class ArchiveSentRecordStatus:
	DRAFT = 0
	SUCCESS = 1
	RELAY = 2

	def __init__(self):
		pass


class ArchiveRasStatus:
	def __init__(self):
		pass

	class RasStatus:
		CREATE = 1
		ARRIVE = 5

		def __init__(self):
			pass

	class RasStatusMask:
		def __init__(self):
			pass

		REVOCATION = 1

		UNREAD = 2
		READ_AND_UNPRINTED = 4
		ALLOW_PRINT = 8
		NOT_ALLOW_PRINT = 16

		__ras_status_mask = {
			1: u"撤回",
			2: u"未阅",
			4: u"已阅",
			8: u"已打印",
			16: u"打印完毕",
		}

		@classmethod
		def get_name(cls, status):
			if isinstance(status, int):
				if status & cls.REVOCATION > 0:
					return cls.__ras_status_mask.get(status)

				keys = cls.__ras_status_mask.keys()
				keys.reverse()
				for k in keys:
					if k & status > 0:
						return cls.__ras_status_mask.get(status)

			return None

		@classmethod
		def is_read(cls, status):
			if isinstance(status, int):
				if status & cls.READ_AND_UNPRINTED > 0:
					return "已阅"
				else:
					return "未阅"

			return None


class AuthorizedReaderStatus:
	UNREAD = 1
	READ = 2
	CANCELED = 4
	DELETED = 5

	def __init__(self):
		pass


class AttendUserMapping:
	def __init__(self):
		pass

	__attend_user_mapping = {

	}


class ArchiveAttributeMapping:
	def __init__(self):
		pass

	__attribute_mapping = {
		"recv_unit": u"收文单位",
		"print_count": u"收文份数",
		"printed_count": u"已打印份数",
		"relay_count": u"转发份数",
		"relayed_count": u"已转发份数",
		"ras_status_mask": u"接收情况",
		"recv_user_id": u"收文人员",
		"recv_time": u"收文时间",
		"is_hasten": u"催办情况",
		"feedback_status": u"回执情况",
		"description": u"回执内容",
		"attend_count": u"会议人数",
		"meeting_attender": u"与会人员名单",
		"reprint_need_approve": u"打印控制",
	}

	__attribute_feedback_attr = {
		"feedback_status": u"回执情况",
		"description": u"回执内容",
		"attend_count": u"会议人数",
		"meeting_attender": u"与会人员名单",
	}

	@classmethod
	def get_query_fields(cls, k):
		if k in cls.__attribute_mapping:
			if k in cls.__attribute_feedback_attr:
				print k
				if k == "feedback_status":
					return "feedback_id"

				if k == "meeting_attender":
					return "id"

				if k != "meeting_attender":
					return "%s__%s" % ("feedback", k)
			else:
				if k == "recv_unit":
					return "recv_unit__name"

				return k

		return None

	@classmethod
	def get_attr_name(cls, attr):
		return cls.__attribute_mapping.get(attr)

	@classmethod
	def get_attr_name_list(cls, attr_list):

		name_list = []
		if isinstance(attr_list, list):
			for attr in attr_list:
				name_list.append(cls.__attribute_mapping.get(attr))

			if len(attr_list) == len(name_list):
				return name_list

		return None


class ArchiveStatus:
	def __init__(self):
		pass

	class ArchiveType:
		def __init__(self):
			pass

		FILE = 1
		MEETING_NOTICE = 2
		PERIODICAL = 3
		MATERIAL = 4
		BRIEF = 5
		OTHER = 6

		__archive_type = {
			1: "文件",
			2: "会议通知",
			3: "刊物杂志",
			4: "材料",
			5: "简报",
			6: "其他"
		}

		@classmethod
		def get_name(cls, status):
			if isinstance(status, int):
				return cls.__archive_type.get(status)
			return None

	class SecurityClassification:
		def __init__(self):
			pass

		UNCLASSIFIED = 1
		SECRET = 2
		CONFIDENTIAL = 3

		__security_classification = {
			1: "无密级",
			2: "秘密",
			3: "机密"
		}

		@classmethod
		def get_name(cls, status):
			if isinstance(status, int):
				return cls.__security_classification.get(status)
			return None

	class EmergencyType:
		def __init__(self):
			pass

		URGENT = 1
		MORE_URGENT = 2
		TOP_URGENT = 3
		UNDEFINED = 4

		emergency_type = {
			1: "平急",
			2: "加急",
			3: "特急",
			4: "无紧急程度",
		}

		@classmethod
		def get_name(cls, status):
			if isinstance(status, int):
				return cls.emergency_type.get(status)
			return None

	class ArchiveFeedbackMeetingType:
		def __init__(self):
			pass

		__feedback_meeting_type = {
			u"name": "need_attender_name",
			u"dept_name": "need_attender_depatname",
			u"duty": "need_attender_duty",
			u"sex": "need_attender_sex",
			u"car_no": "need_attender_car_integer",
			u"photo": "need_attender_photo",
		}

		@classmethod
		def get_name(cls, field):
			if isinstance(field, str) or isinstance(field, unicode):
				return cls.__feedback_meeting_type.get(field)
			return None


	class FeedbackType:
		def __init__(self):
			pass

		NOT_REQUIRE_FEEDBACK = 1
		REQUIRE_FEEDBACK = 2
		REQUIRE_MEETING_FEEDBACK = 3
		REQUIRE_ATTENDANCE_FEEDBACK = 4

		__feedback_type = {
			1: "不需要回执",
			2: "普通回执",
			3: "会议回执",
			4: "会议回执且需要人员名单",
		}

		@classmethod
		def get_name(cls, status):
			if isinstance(status, int):
				return cls.__feedback_type.get(status)
			return None