#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
import cgi
import create_db
import funct

mysql_enable = funct.get_config_var('mysql', 'enable')

if mysql_enable == '1':
	from mysql.connector import errorcode
	import mysql.connector as sqltool
else:	
	import sqlite3 as sqltool
		
def add_user(user, email, password, role, group):
	con, cur = create_db.get_cur()
	sql = """INSERT INTO user (username, email, password, role, groups) VALUES ('%s', '%s', '%s', '%s', '%s')""" % (user, email, password, role, group)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close()   
	
def update_user(user, email, password, role, group, id):
	con, cur = create_db.get_cur()
	sql = """update user set username = '%s', 
			email = '%s',
			password = '%s', 
			role = '%s', 
			groups = '%s' 
			where id = '%s'""" % (user, email, password, role, group, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close()

def delete_user(id):
	con, cur = create_db.get_cur()
	sql = """delete from user where id = '%s'""" % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
		con.rollback()
	else: 
		return True
	cur.close()
	
def add_group(name, description):
	con, cur = create_db.get_cur()
	sql = """INSERT INTO groups (name, description) VALUES ('%s', '%s')""" % (name, description)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		print(cur.lastrowid)
		return True
	cur.close()    
	con.close() 

def delete_group(id):
	con, cur = create_db.get_cur()
	sql = """delete from groups where id = '%s'""" % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 
	
def update_group(name, descript, id):
	con, cur = create_db.get_cur()
	sql = """
		update groups set 
		name = '%s',
		description = '%s' 
		where id = '%s';
		""" % (name, descript, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
	else:
		return True
	cur.close()    
	con.close()

def add_server(hostname, ip, group, typeip, enable, master, cred, alert):
	con, cur = create_db.get_cur()
	sql = """
			INSERT INTO servers 
			(hostname, ip, groups, type_ip, enable, master, cred, alert) 
			VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
		""" % (hostname, ip, group, typeip, enable, master, cred, alert)
	try:    
		cur.execute(sql)
		con.commit()
		return True
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
		return False
		
	cur.close()    
	con.close() 	

def delete_server(id):
	con, cur = create_db.get_cur()
	sql = """delete from servers where id = '%s'""" % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 		

def update_server(hostname, ip, group, typeip, enable, master, id, cred, alert):
	con, cur = create_db.get_cur()
	sql = """update servers set 
			hostname = '%s',
			ip = '%s',
			groups = '%s',
			type_ip = '%s',
			enable = '%s',
			master = '%s',
			cred = '%s',
			alert = '%s'
			where id = '%s'""" % (hostname, ip, group, typeip, enable, master, cred, alert, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()

def update_server_master(master, slave):
	con, cur = create_db.get_cur()
	sql = """ select id from servers where ip = '%s' """ % master
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	for id in cur.fetchall():
		sql = """ update servers set master = '%s' where ip = '%s' """ % (id[0], slave)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()
	
def select_users(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from user ORDER BY id"""
	if kwargs.get("user") is not None:
		sql = """select * from user where username='%s' """ % kwargs.get("user")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()    
	
def select_groups(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from groups ORDER BY id"""
	if kwargs.get("group") is not None:
		sql = """select * from groups where name='%s' """ % kwargs.get("group")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def select_user_name_group(id):
	con, cur = create_db.get_cur()
	sql = """select name from groups where id='%s' """ % id
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	else:
		for group in cur.fetchone():
			return group
	cur.close()    
	con.close()  
	
def select_servers(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from servers where enable = '1' ORDER BY groups """
	if kwargs.get("server") is not None:
		sql = """select * from servers where ip='%s' """ % kwargs.get("server")
	if kwargs.get("full") is not None:
		sql = """select * from servers ORDER BY groups """ 
	if kwargs.get("get_master_servers") is not None:
		sql = """select id,hostname from servers where master = 0 and type_ip = 0 and enable = 1 ORDER BY groups """ 
	if kwargs.get("get_master_servers") is not None and kwargs.get('uuid') is not None:
		sql = """
			select servers.id, servers.hostname from servers 
			left join user as user on servers.groups = user.groups 
			left join uuid as uuid on user.id = uuid.user_id 
			where uuid.uuid = '%s' and servers.master = 0 and servers.type_ip = 0 and servers.enable = 1 ORDER BY servers.groups 
			""" % kwargs.get('uuid')
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def get_type_ip_checkbox(id, **kwargs):
	con, cur = create_db.get_cur()
	sql = """select id, type_ip from servers where id='%s' """ % id
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		for server in cur.fetchall():
			if server[1] == 1:
				checked = 'checked'
			else:
				checked = ""
			print('<label for="typeip-%s"></label><input type="checkbox" id="typeip-%s" %s>' % (server[0],server[0], checked))
	cur.close()    
	con.close() 
	
def get_enable_checkbox(id, **kwargs):
	con, cur = create_db.get_cur()
	sql = """select id, enable from servers where id='%s' """ % id
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		for server in cur.fetchall():
			if server[1] == 1:
				checked = 'checked'
			else:
				checked = ""
			print('<label for="enable-%s"></label><input type="checkbox" id="enable-%s" %s>' % (server[0],server[0], checked))
	cur.close()    
	con.close() 
	
def write_user_uuid(login, user_uuid):
	con, cur = create_db.get_cur()
	session_ttl = funct.get_config_var('main', 'session_ttl')
	session_ttl = int(session_ttl)
	sql = """ select id from user where username = '%s' """ % login
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	for id in cur.fetchall():
		if mysql_enable == '1':
			sql = """ insert into uuid (user_id, uuid, exp) values('%s', '%s',  now()+ INTERVAL %s day) """ % (id[0], user_uuid, session_ttl)
		else:
			sql = """ insert into uuid (user_id, uuid, exp) values('%s', '%s',  datetime('now', '+%s days')) """ % (id[0], user_uuid, session_ttl)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()
	
def write_user_token(login, user_token):
	con, cur = create_db.get_cur()
	token_ttl = funct.get_config_var('main', 'token_ttl')	
	sql = """ select id from user where username = '%s' """ % login
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	for id in cur.fetchall():
		if mysql_enable == '1':
			sql = """ insert into token (user_id, token, exp) values('%s', '%s',  now()+ INTERVAL %s day) """ % (id[0], user_token, token_ttl)
		else:
			sql = """ insert into token (user_id, token, exp) values('%s', '%s',  datetime('now', '+%s days')) """ % (id[0], user_token, token_ttl)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()
	
def get_token(uuid):
	con, cur = create_db.get_cur()

	sql = """ select token.token from token left join uuid as uuid on uuid.user_id = token.user_id where uuid.uuid = '%s' """ % uuid
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	else:
		for token in cur.fetchall():
			return token[0]
				
	cur.close()    
	con.close()
	
def delete_uuid(uuid):
	con, cur = create_db.get_cur()
	sql = """ delete from uuid where uuid = '%s' """ % uuid
	try:
		cur.execute(sql)		
		con.commit()
	except sqltool.Error as e:
		pass
	cur.close()    
	con.close() 
	
def delete_old_uuid():
	con, cur = create_db.get_cur()
	if mysql_enable == '1':
		sql = """ delete from uuid where exp < now() or exp is NULL """
		sql1 = """ delete from token where exp < now() or exp is NULL """
	else:
		sql = """ delete from uuid where exp < datetime('now') or exp is NULL""" 
		sql1 = """ delete from token where exp < datetime('now') or exp is NULL""" 
	try:    
		cur.execute(sql)
		cur.execute(sql1)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()		

def update_last_act_user(uuid):
	con, cur = create_db.get_cur()
	session_ttl = funct.get_config_var('main', 'session_ttl')
	
	if mysql_enable == '1':
		sql = """ update uuid set exp = now()+ INTERVAL %s day where uuid = '%s' """ % (session_ttl, uuid)
	else:
		sql = """ update uuid set exp = datetime('now', '+%s days') where uuid = '%s' """ % (session_ttl, uuid)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<div class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></div>')
		con.rollback()
	cur.close()    
	con.close()
	
def get_user_name_by_uuid(uuid):
	con, cur = create_db.get_cur()
	sql = """ select user.username from user left join uuid as uuid on user.id = uuid.user_id where uuid.uuid = '%s' """ % uuid
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for user_id in cur.fetchall():
			return user_id[0]
	cur.close()    
	con.close() 
	
def get_user_role_by_uuid(uuid):
	con, cur = create_db.get_cur()
	sql = """ select role.id from user left join uuid as uuid on user.id = uuid.user_id left join role on role.name = user.role where uuid.uuid = '%s' """ % uuid
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for user_id in cur.fetchall():
			return user_id[0]
	cur.close()    
	con.close() 
	
def get_user_group_by_uuid(uuid):
	con, cur = create_db.get_cur()
	sql = """ select user.groups from user left join uuid as uuid on user.id = uuid.user_id  where uuid.uuid = '%s' """ % uuid
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for user_id in cur.fetchall():
			return user_id[0]
	cur.close()    
	con.close() 

def get_user_telegram_by_uuid(uuid):
	con, cur = create_db.get_cur()
	sql = """ select telegram.* from telegram left join user as user on telegram.groups = user.groups left join uuid as uuid on user.id = uuid.user_id where uuid.uuid = '%s' """ % uuid
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		return cur.fetchall()
	cur.close()    
	con.close() 	
	
def get_telegram_by_ip(ip):
	con, cur = create_db.get_cur()
	sql = """ select telegram.* from telegram left join servers as serv on serv.groups = telegram.groups where serv.ip = '%s' """ % ip
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		return cur.fetchall()
	cur.close()    
	con.close()

def get_dick_permit(**kwargs):
	import http.cookies
	import os
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_id = cookie.get('uuid')
	
	con, cur = create_db.get_cur()
	sql = """ select * from user where username = '%s' """ % get_user_name_by_uuid(user_id.value)
	if kwargs.get('virt'):
		type_ip = "" 
	else:
		type_ip = "and type_ip = 0" 
	if kwargs.get('disable') == 0:
		disable = 'or enable = 0'
	else:
		disable = ''
		
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		for group in cur:
			if group[5] == '1':
				sql = """ select * from servers where enable = 1 %s %s """ % (disable, type_ip)
			else:
				sql = """ select * from servers where groups like '%{group}%' and (enable = 1 {disable}) {type_ip} """.format(group=group[5], disable=disable, type_ip=type_ip)		
		try:   
			cur.execute(sql)
		except sqltool.Error as e:
			print("An error occurred:", e.args[0])
		else:
			return cur.fetchall()
	cur.close()    
	con.close() 
	
def is_master(ip, **kwargs):
	con, cur = create_db.get_cur()
	sql = """ select slave.ip from servers as master left join servers as slave on master.id = slave.master where master.ip = '%s' """ % ip
	if kwargs.get('master_slave'):
		sql = """ select master.hostname, master.ip, slave.hostname, slave.ip from servers as master left join servers as slave on master.id = slave.master where slave.master > 0 """
	try:
		cur.execute(sql)		
	except sqltool.Error as e:
		print("An error occurred:", e)
	else:
		return cur.fetchall()
	cur.close()    
	con.close() 
	
def select_ssh(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from cred """
	if kwargs.get("name") is not None:
		sql = """select * from cred where name = '%s' """ % kwargs.get("name")
	if kwargs.get("id") is not None:
		sql = """select * from cred where id = '%s' """ % kwargs.get("id")
	if kwargs.get("serv") is not None:
		sql = """select serv.cred, cred.* from servers as serv left join cred on cred.id = serv.cred where serv.ip = '%s' """ % kwargs.get("serv")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
	else:
		return cur.fetchall()
	cur.close()    
	con.close() 
	
def insert_new_ssh(name, enable, group, username, password):
	con, cur = create_db.get_cur()
	sql = """insert into cred(name, enable, groups, username, password) values ('%s', '%s', '%s', '%s', '%s') """ % (name, enable, group, username, password)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 
	
def delete_ssh(id):
	con, cur = create_db.get_cur()
	sql = """ delete from cred where id = %s """ % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 

def update_ssh(id, name, enable, group, username, password):
	con, cur = create_db.get_cur()
	sql = """ 
			update cred set 
			name = '%s',
			enable = '%s',
			groups = %s,
			username = '%s',
			password = '%s' where id = '%s' """ % (name, enable, group, username, password, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()
	
def show_update_ssh(name, page):
	from jinja2 import Environment, FileSystemLoader
	env = Environment(loader=FileSystemLoader('templates/ajax'))
	template = env.get_template('/new_ssh.html')

	print('Content-type: text/html\n')

	output_from_parsed_template = template.render(groups = select_groups(), sshs = select_ssh(name=name),page=page)
	print(output_from_parsed_template)

def insert_new_telegram(token, chanel, group):
	con, cur = create_db.get_cur()
	sql = """insert into telegram(`token`, `chanel_name`, `groups`) values ('%s', '%s', '%s') """ % (token, chanel, group)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 

def delete_telegram(id):
	con, cur = create_db.get_cur()
	sql = """ delete from telegram where id = %s """ % (id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	else: 
		return True
	cur.close()    
	con.close() 	
	
def select_telegram(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from telegram  """
	if kwargs.get('group'):
		sql = """select * from telegram where groups = '%s' """ % kwargs.get('group')
	if kwargs.get('token'):
		sql = """select * from telegram where token = '%s' """ % kwargs.get('token')
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close() 
	
def update_telegram(token, chanel, group, id):
	con, cur = create_db.get_cur()
	sql = """ 
			update telegram set 
			`token` = '%s',
			`chanel_name` = '%s',
			`groups` = '%s'
			where id = '%s' """ % (token, chanel, group, id)
	try:    
		cur.execute(sql)
		con.commit()
	except sqltool.Error as e:
		print('<span class="alert alert-danger" id="error">An error occurred: ' + e.args[0] + ' <a title="Close" id="errorMess"><b>X</b></a></span>')
		con.rollback()
	cur.close()    
	con.close()
	
def show_update_telegram(token, page):
	from jinja2 import Environment, FileSystemLoader
	env = Environment(loader=FileSystemLoader('templates/ajax'))
	template = env.get_template('/new_telegram.html')

	print('Content-type: text/html\n')

	output_from_parsed_template = template.render(groups = select_groups(), telegrams = select_telegram(token=token),page=page)
	print(output_from_parsed_template)	

def show_update_user(user):
	from jinja2 import Environment, FileSystemLoader
	env = Environment(loader=FileSystemLoader('templates/ajax'))
	template = env.get_template('/new_user.html')

	print('Content-type: text/html\n')

	output_from_parsed_template = template.render(users = select_users(user=user),
													groups = select_groups(),
													roles = select_roles())
	print(output_from_parsed_template)
		
def show_update_server(server, page):
	from jinja2 import Environment, FileSystemLoader
	env = Environment(loader=FileSystemLoader('templates/ajax/'))
	template = env.get_template('/new_server.html')

	print('Content-type: text/html\n')

	output_from_parsed_template = template.render(groups = select_groups(),
													servers = select_servers(server=server),
													roles = select_roles(),
													masters = select_servers(get_master_servers=1),
													sshs = select_ssh(),
													page = page)
	print(output_from_parsed_template)

def show_update_group(group):
	from jinja2 import Environment, FileSystemLoader
	env = Environment(loader=FileSystemLoader('templates/ajax/'))
	template = env.get_template('/new_group.html')

	print('Content-type: text/html\n')

	output_from_parsed_template = template.render(groups = select_groups(group=group))
	print(output_from_parsed_template)

def select_roles(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from role ORDER BY id"""
	if kwargs.get("role") is not None:
		sql = """select * from role where name='%s' """ % kwargs.get("group")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def select_roles(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select * from role ORDER BY id"""
	if kwargs.get("roles") is not None:
		sql = """select * from role where name='%s' """ % kwargs.get("roles")
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close()  
	
def select_alert(**kwargs):
	con, cur = create_db.get_cur()
	sql = """select ip from servers where alert = 1 """
	try:    
		cur.execute(sql)
	except sqltool.Error as e:
		print("An error occurred:", e.args[0])
	else:
		return cur.fetchall()
	cur.close()    
	con.close() 
				
form = cgi.FieldStorage()
error_mess = '<span class="alert alert-danger" id="error">All fields must be completed <a title="Close" id="errorMess"><b>X</b></a></span>'

if form.getvalue('newusername') is not None:
	email = form.getvalue('newemail')
	password = form.getvalue('newpassword')
	role = form.getvalue('newrole')
	group = form.getvalue('newgroupuser')
	new_user = form.getvalue('newusername')	
	if password is None or role is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		if add_user(new_user, email, password, role, group):
			show_update_user(new_user)
		
if form.getvalue('updateuser') is not None:
	email = form.getvalue('email')
	password = form.getvalue('password')
	role = form.getvalue('role')
	group = form.getvalue('usergroup')
	new_user = form.getvalue('updateuser')	
	id = form.getvalue('id')	
	if password is None or role is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		update_user(new_user, email, password, role, group, id)
		
if form.getvalue('userdel') is not None:
	print('Content-type: text/html\n')
	if delete_user(form.getvalue('userdel')):
		print("Ok")
		
if form.getvalue('newserver') is not None:
	import funct
	hostname = form.getvalue('newserver')	
	ip = form.getvalue('newip')
	group = form.getvalue('newservergroup')
	typeip = form.getvalue('typeip')
	enable = form.getvalue('enable')
	master = form.getvalue('slave')
	cred = form.getvalue('cred')
	alert = form.getvalue('alert_en')
	page = form.getvalue('page')
	page = page.split("#")[0]
	if ip is None or group is None or cred is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:	
		print('Content-type: text/html\n')
		if add_server(hostname, ip, group, typeip, enable, master, cred, alert):
			show_update_server(ip, page)
		
if form.getvalue('serverdel') is not None:
	print('Content-type: text/html\n')
	if delete_server(form.getvalue('serverdel')):
		print("Ok")
	
if form.getvalue('newgroup') is not None:
	newgroup = form.getvalue('newgroup')	
	desc = form.getvalue('newdesc')
	print('Content-type: text/html\n')
	if add_group(newgroup, desc):
		show_update_group(newgroup)

if form.getvalue('groupdel') is not None:
	print('Content-type: text/html\n')
	if delete_group(form.getvalue('groupdel')):
		print("Ok")
		
if form.getvalue('updategroup') is not None:
	name = form.getvalue('updategroup')
	descript = form.getvalue('descript')	
	id = form.getvalue('id')	
	if name is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		update_group(name, descript, id)
		
if form.getvalue('updateserver') is not None:
	import funct
	name = form.getvalue('updateserver')
	ip = form.getvalue('ip')	
	group = form.getvalue('servergroup')	
	typeip = form.getvalue('typeip')		
	enable = form.getvalue('enable')		
	master = form.getvalue('slave')		
	id = form.getvalue('id')	
	cred = form.getvalue('cred')	
	alert = form.getvalue('alert_en')	
	if name is None or ip is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		#if funct.ssh_connect(ip, check=1):
		update_server(name, ip, group, typeip, enable, master, id, cred, alert)
		#else:
		#	print('<span class="alert alert-danger" id="error"><a title="Close" id="errorMess"><b>X</b></a></span>')
			
if form.getvalue('updatessh'):
	id = form.getvalue('id')
	name = form.getvalue('name')
	enable = form.getvalue('ssh_enable')	
	group = form.getvalue('group')	
	username = form.getvalue('ssh_user')		
	password = form.getvalue('ssh_pass')
	if username is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:
		import funct
		print('Content-type: text/html\n')
		fullpath = funct.get_config_var('main', 'fullpath')
		
		for sshs in select_ssh(id=id):
			ssh_enable = sshs[2]
			ssh_key_name = fullpath+'/keys/%s.pem' % sshs[1]
			new_ssh_key_name = fullpath+'/keys/%s.pem' % name
					
		if ssh_enable == 1:
			cmd = 'mv %s %s' % (ssh_key_name, new_ssh_key_name)
			try:
				funct.subprocess_execute(cmd)
			except:
				pass
		update_ssh(id, name, enable, group, username, password)
		
if form.getvalue('new_ssh'):
	name = form.getvalue('new_ssh')
	enable = form.getvalue('ssh_enable')	
	group = form.getvalue('new_group')	
	username = form.getvalue('ssh_user')		
	password = form.getvalue('ssh_pass')
	page = form.getvalue('page')
	page = page.split("#")[0]
	if username is None or name is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:
		if insert_new_ssh(name, enable, group, username, password):
			show_update_ssh(name, page)
			
if form.getvalue('sshdel') is not None:
	import funct
	print('Content-type: text/html\n')
	fullpath = funct.get_config_var('main', 'fullpath')
	
	for sshs in select_ssh(id=form.getvalue('sshdel')):
		ssh_enable = sshs[2]
		ssh_key_name = fullpath+'/keys/%s.pem' % sshs[1]
				
	if ssh_enable == 1:
		cmd = 'rm -f %s' % ssh_key_name
		try:
			funct.subprocess_execute(cmd)
		except:
			pass
	if delete_ssh(form.getvalue('sshdel')):
		print("Ok")

if form.getvalue('newtelegram'):
	token = form.getvalue('newtelegram')
	chanel = form.getvalue('chanel')	
	group = form.getvalue('telegramgroup')	
	page = form.getvalue('page')
	page = page.split("#")[0]
	if token is None or chanel is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:
		if insert_new_telegram(token, chanel, group):
			show_update_telegram(token, page)
			
if form.getvalue('telegramdel') is not None:
	print('Content-type: text/html\n')
	if delete_telegram(form.getvalue('telegramdel')):
		print("Ok")
		
if form.getvalue('updatetoken') is not None:
	token = form.getvalue('updatetoken')
	chanel = form.getvalue('updategchanel')	
	group = form.getvalue('updategroup')	
	id = form.getvalue('id')		
	if token is None or chanel is None or group is None:
		print('Content-type: text/html\n')
		print(error_mess)
	else:		
		print('Content-type: text/html\n')
		update_telegram(token, chanel, group, id)