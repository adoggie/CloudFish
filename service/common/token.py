#coding:utf-8

__author__ = 'root'

import json,traceback

import lemon.utils.cipher

def encryptUserToken(user):
	"""
	加密生成用户令牌
		user : {
			user_id,
			user_name,
			app_id,
			app_sid,
			app_name,
			node_type(client/server),
			create_time,expire_time
		}

	"""
	data = json.dumps( user)
	token = lemon.utils.cipher.encryptToken( data )
	return token

def decryptUserToken(token):
	"""
	解开用户令牌
	"""

	user = json.loads( lemon.utils.cipher.decryptToken(token) )
	return user
