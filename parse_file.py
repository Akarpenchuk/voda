##-*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup

FAIL = 'bs_binar.txt'

def files(path):
	f = open(path, 'r')
	x = f.read()
	f.close()
	return x

def parse(html):	# парсим обьект(текст бинанар хтмл), пихаем этот хлам в словарь
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find('table', class_= 'powerSupplyTable')
	table_powerSupplyTableOddRow = table.find_all('tr', class_ = 'powerSupplyTableOddRow')
	table_powerSupplyTableEvenRow = table.find_all('tr', class_ = 'powerSupplyTableEvenRow')
	table = table_powerSupplyTableEvenRow + table_powerSupplyTableOddRow

	report_table = []
	for rows in table:
		cols = rows.find_all('td')
		
		report_table.append({
			'date' : str(cols[1].string),
			'bsc' : str(cols[2].string),
			'bcf' : str(cols[3].string),
			'site' : str(cols[4].string),
			'pr_bs' : str(cols[5].string),
			'pr_ts' : str(cols[6].string),
			'mc' : str(cols[7].string),
			'akb' : str(cols[9].find('span').string),
			'akb_color' : (str(cols[9].span.get('style'))).split(':')[-1],
			'down' : str(cols[10].find('span').string),
			'down_color' : (str(cols[10].span.get('style'))).split(':')[-1],
			'up' : str(cols[11].string),
			'up_color' : (str(cols[10].span.get('style'))).split(':')[-1],
			'resposible' : (cols[-6].text),
			'add_info' : (cols[-2]).decode('utf-8'),
			'updated' : str(cols[-1].string)
		})
	return report_table

def save_csv(report_table, path):
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Date', 'BSC', 'BCF', 'Site','priority_BS', 'MC', 'AKB', 'AKB_color', 'DOWN', 'DOWN_color', 'UP', \
			'UP_color', 'Resposible', 'add_info', 'CKU_duty'))

		for rows in report_table:
			writer.writerow((rows['date'], rows['bsc'], rows['bcf'], rows['site'], rows['pr_bs'], rows['mc'], rows['akb'], rows['akb_color'], \
				rows['down'], rows['down_color'], rows['up'], rows['up_color'], rows['resposible'], rows['add_info'], rows['updated']))

tabl = parse(files(FAIL))
for i in tabl:
	print(i, '\n')

# project = []
# # report_f = 
# project.extend(parse(files(FAIL)))
# save_csv(project, 'report.csv')