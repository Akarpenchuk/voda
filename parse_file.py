import csv
import requests
from bs4 import BeautifulSoup

FAIL = 'bs_binar.txt'

def files(path):
	f = open(path, 'r')
	x = f.read()
	f.close()
	return x

def parse(html):
	soup = BeautifulSoup(html)
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
			'resposible' : str(cols[-6].text),
			'add_info' : str(cols[-2].string),
			'updated' : str(cols[-1].string)
		})
	return report_table

tabl = parse(files(FAIL))
for i in tabl:
	print(i, '\n')

# find('span')