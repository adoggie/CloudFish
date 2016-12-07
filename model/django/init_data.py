# -- coding:utf-8 --
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lemon.settings")
import core.models as cm

def clearup():
	cm.TeamRelation.objects.all().delete()
	cm.UserRelation.objects.all().delete()
	cm.UserSettings.objects.all().delete()
	cm.UserGroup.objects.all().delete()
	cm.UserTeam.objects.all().delete()
	cm.User.objects.all().delete()


	cm.GlobalSettings.objects.all().delete()

global_settings={
	'ver':'0.0.0.1',
    'date':'2013-11-21',
    'server':'localhost:14001'
}



def_users=[{
	'id':1,
	'user':'test',
    'passwd':'111111',
    'name':'test',
    'age':10,
    'email':'24509826@qq.com',
    'teams':[{'id':1,'name':'team1_in_test1'},{'id':2,'name':'team2_in_test1'}],
    'in_teams':[],
	},
	{
	'id':2,
	'user':'test2',
    'passwd':'111111',
    'name':'test2',
    'age':10,
    'email':'245098262@qq.com',
	'teams':[],
	'in_teams':[1,]
	},
    {
	'id':3,
	'user':'test3',
    'passwd':'111111',
    'name':'test3',
    'age':10,
    'email':'245098263@qq.com',
    'teams':[],
	'in_teams':[1,]
	},
	]

def init_database():
	clearup()

	for k,v in global_settings.items():
		en = cm.GlobalSettings()
		en.name = k
		en.value= v
		en.save()

	users={}
	for i in def_users:
		r = cm.User()
		r.user = i['user']
		r.name = i['name']
		r.passwd = i['passwd']
		r.age = i['age']
		r.email = i['email']
		r.save()

		users[i['id']] = i # users= {id,user}
		i['delta'] = r #关联信息到 dbobj

	teams={}
	for id,user in users.items():
		#user['delta']  指向 dbobj
		for teaminfo in user['teams']: #依次创建群
			team = cm.UserTeam()
			team.user = user['delta']
			team.name = teaminfo['name']
			team.save()
			teaminfo['owner_id'] = id
			teaminfo['delta'] = team
			teams[teaminfo['id']] = teaminfo

			#rel = cm.TeamRelation()
			#rel.user = team.user
			#rel.team = team
			#rel.save()
			#rel = cm.UserRelation()
			#rel.user = user['delta']
			#rel.friend = user['delta']
			#rel.team = team
			#rel.save()  #将本人加入自己的群内

	for id,user in users.items():
		for teamid in user['in_teams']:
			team = teams[teamid]
			userid = team['owner_id']
			owner_of_team = users[userid]
			rel = cm.UserRelation()
			rel.user = owner_of_team['delta']
			rel.friend = user['delta']
			#rel.team = team['delta']
			rel.save()

			rel = cm.UserRelation()
			rel.user = user['delta']
			rel.friend = owner_of_team['delta']
			rel.save()

			rel = cm.TeamRelation()
			rel.user = user['delta']
			rel.team = team['delta']
			rel.save()




if __name__ == "__main__":
	init_database()
