import re

from tabulate import tabulate

from ldap3 import Server, Connection, ALL, Tls
import ssl
import getpass

# uname = getpass.getpass(prompt='Password: ', stream=None)
passwd = input("Password... ")



# define the server and the connection
server = Server("somesever", get_info=ALL)
with Connection(server, user="someuser", password=passwd, auto_bind=True) as conn:
	# print(conn)
	conn.start_tls()
	# print(conn.extend.standard.who_am_i())
	while True:
		app_name = input("\nApplicant name: ")
		# print(app_name)
		search_addertion = ""
		app_name = re.sub("[, ]", " ", app_name)
		app_name = app_name.strip().split()
		if len(app_name) == 1:
			search_addertion = "(displayName={})".format(app_name[0])
		else:
			for _p in app_name:
				search_addertion += "(displayName=*{}*)".format(_p)

			search_addertion = "(&" + search_addertion + ")"
		# print(search_addertion)

		conn.search("some_search_area", search_addertion, attributes=["cn","displayName", "title", "mail", "neuDepatrment", "neuDivisionDescription"])

		if conn.entries:
			for _entry in conn.entries:
				print_lst = []
				if "title" in _entry:
					print_lst.append(['title', _entry["title"]])
				if "displayName" in _entry:
					print_lst.append(['displayName', _entry["displayName"]])
				if "cn" in _entry:
					print_lst.append(['cn', _entry["cn"]])
				if "mail" in _entry:
					print_lst.append(['mail', _entry["mail"]])
				if "neuDepatrment" in _entry:
					print_lst.append(['Department', _entry["neuDepatrment"]])
				if "neuDivisionDescription" in _entry:
					print_lst.append(['Division', _entry["neuDivisionDescription"]])

				print(tabulate(print_lst))

			# print(conn.entries)

		else:
			print("Cannot find {}".format(app_name))
