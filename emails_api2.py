from flask import Flask,jsonify,request
import pandas as pd
from csv import reader
import requests
import json
import urllib3
import os

global domain

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
@app.route('/emails', methods = ['GET'])
#ReturnJSON
def ReturnJSON():
	if(request.method == 'GET'):
		dictionary = {}
		emails = []
		domains = []
		jsondictionary = []
		csv_file = open('/var/www/html/emails/emails.csv', "r")
		csv_reader = reader(csv_file)
#		file_domains = open('domainlist.txt', "r")
#		lines = file_domains.readlines()
		for row1 in csv_reader:
			domain_csvw = str(row1[0])
			domain_csv = domain_csvw
			domains.append(domain_csv)
			
		for domain in domains:
			emails.clear()			
			domain2 = domain
			csv_file = open('/var/www/html/emails/emails.csv', "r")
			csv_reader = reader(csv_file)
			jsondata = {'url' : ' ', 'city': ' ', 'founded' : ' ', 'size' : ' ', 'industry' : ' ', 'social' : ' ', 'emails' : []}			
			for row in csv_reader:
#				print(row)
				if domain2 in row and row[1] not in emails:
					emails.append(row[1])
					jsondata['city'] =  str(row[2])
					jsondata['founded'] = str(row[3])
					jsondata['industry'] = str(row[4])
					jsondata['size'] = str(row[5])
					jsondata['social'] = str(row[6])
				else:
					pass
#					print(emails)
			jsondata['emails'] += emails
			jsondata['url'] = domain2
			if jsondata not in jsondictionary:
				jsondictionary.append(jsondata)
				
		#jsondictionary.pop(0)
		jsonData1 = str(jsondictionary)
		
		f = open("emails.json", "w")
		f.write(json.dumps(jsondictionary))
		f.close()
		files = {'userfile': open('emails.json','rb')}
		r = requests.post('http://samurai3.keenetic.link/csv/queue_endpoint.php', files=files)
		print(f"Status Code: {r.status_code}")
		os.remove("/var/www/html/emails/emails.csv")
		
		return jsonify(jsondictionary)
		
		

if __name__=='__main__':
	app.run(debug=True)
