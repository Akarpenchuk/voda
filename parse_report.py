# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://kv-po-duty01.mts.com.ua:8080/report2/PowerEvents.xhtml'
LOGIN = 'nmc'
PASSWORD ='nmc'

def get_report():	# логинимся как КА блеа... хедерами имитируем лису, из тела хтмл вырываем супом 'javax.faces.ViewState' (для даты) без нее не фурычит, и еще нужно отвравлять форму со вежими куками каждый раз
	global_headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
		'Accept-Encoding': 'gzip, deflate'
	}

	ses_init = requests.get(BASE_URL, headers = global_headers)
	soup = BeautifulSoup(ses_init.content)
	javax_faces_ViewState = str(soup.find_all(id ='javax.faces.ViewState')[-1].get('value'))
	cokie = ses_init.headers.get('Set-Cookie')

	local_headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
		'Accept-Encoding': 'gzip, deflate',
		'Set-Cookie' : cokie
	}
	data_r = {
		'j_id_4:username' : LOGIN,
		'j_id_4:password' : PASSWORD,
		'j_id_4:j_id_u' : 'Войти',
		'j_id_4_SUBMIT' : '1',
		'javax.faces.ViewState' : javax_faces_ViewState
	}
	r = requests.post(BASE_URL, headers = local_headers, data = data_r)  #борода которая логинится и получает все записи в репорте, ваще все во влкадке олл
	return str(r.content.decode('utf-8'))

def parse(html):	# парсим обьект(текст бинанар хтмл), пихаем этот хлам в словарь
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
			'add_info' : str(cols[-2].string).replace('\r\n', ' '),
			'updated' : str(cols[-1].string)
		})
	return report_table

def save_csv(report_table, path):
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Дата', 'BSC', 'BCF', 'Сайт','приоритет_BS', 'MC', 'Акб', 'АКБ_колор', 'Падение', 'Падение_колор',\
			'Поднятие', 'Поднятие_колор', 'Ответственные', 'add_info', 'Дежурный'))

		for rows in report_table:
			writer.writerow((rows['date'], rows['bsc'], rows['bcf'], rows['site'], rows['pr_bs'], rows['mc'], rows['akb'], \
				rows['akb_color'], rows['down'], rows['down_color'], rows['up'], rows['up_color'], rows['resposible'], rows['updated']))

project = []
report_f = get_report()
project.extend(parse(report_f))
save_csv(project, 'report.csv')

# f = open('bs_dict.txt', 'w')		#в файл запихую допилю дома
# f.write(report_f)
# f.close()
