import requests
import re
import configparser
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
# print('path::',dir_path)
config = configparser.ConfigParser() 
config.read(str(dir_path)+'//configure.ini')
##### Field Names from INI #####
Field_Name='lawncare'

mainURL = config.get(Field_Name,'url')
title_re = config.get(Field_Name,'title_re')
block_re = config.get(Field_Name,'block_re')
domainName = config.get(Field_Name,'domainName')
sublink_re = config.get(Field_Name,'sublink_re')
addressBlock_re = config.get(Field_Name,'addressBlock_re')
website_re = config.get(Field_Name,'website_re')
phone_re = config.get(Field_Name,'phone_re')
email_re = config.get(Field_Name,'email_re')
mobile_re = config.get(Field_Name,'mobile_re')
link_re = config.get(Field_Name,'link_re')
tel_re = config.get(Field_Name,'tel_re')
name_re = config.get(Field_Name,'name_re')
company_re = config.get(Field_Name,'company_re')
nextpagelink_re = config.get(Field_Name,'nextpagelink_re')
nxtCondtion_lst = nextpagelink_re.split('|')
print('nxtCondtion',nxtCondtion_lst)
if nxtCondtion_lst[0] == 'True':
    nxtCondtions = nxtCondtion_lst[1]
    print('nxt:',nxtCondtions)
    
# sys.exit()


print('nxtlink:',nextpagelink_re)

  
  
while True:
	print('mainURL::',mainURL)
	input('------------	 ')
	req = requests.get(mainURL)
	mainContent = req.content.decode('UTF-8',errors ='ignore')
	blocks = re.findall(block_re,mainContent)
		
	for count,block in enumerate(blocks):
		print(count,'/',len(blocks))
		title = re.findall(title_re,block)
		print('title:',title)
		if name_re:
				name = re.findall(name_re,block)
				print('name:',name)
		if company_re:
				company = re.findall(company_re,block)
				print('company:',company)
		if sublink_re:
				sublink = re.findall(sublink_re,block)
				subURL =	domainName + sublink[0]
				print('subURL:',subURL)
				subreq = requests.get(subURL)
				subContent = subreq.content.decode('UTF-8',errors='ignore')
				# print('subContent:',subContent)
				with open('subContent.html','w',encoding = 'UTF-8') as n:
					n.write(subContent)
				addressBlock = re.findall(addressBlock_re,subContent)
				print('address::::',addressBlock)
				if addressBlock:
					address	= re.sub('(<[^>]*?>)','|',addressBlock[0])
					address	= re.sub('\s+',' ',address)
					print('addressBlock:',address)
				if website_re:
						website = re.findall(website_re,subContent)
						print('website:',website)
				else:
						website = ''
				if email_re:
						email = re.findall(email_re,subContent)
						print('email:',email)
				else:
						email_re = ''
				
	if nxtCondtion_lst[0] == 'True':
		nextpagelink = re.findall(nxtCondtions,mainContent)
		if nextpagelink:
				nextpagelink = 'domainName' + nextpagelink[0]
				print('nextpagelink::',nextpagelink)		
				mainURL = nextpagelink
		else:
			print('No Next Page')
			break
	else:
		print('No Next Page')
		break