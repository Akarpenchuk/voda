##-*- coding: utf-8 -*-
import pickle
import csv
import requests
from bs4 import BeautifulSoup
from tkinter import *
import time, random

BASE_URL = 'http://kv-po-duty01.mts.com.ua:8080/report2/PowerEvents.xhtml'
LOGIN_REP = 'nmc'
PASSWORD_REP ='nmc'
vars = []	#Глобалка из чекбатонна для прочека видео
rb = 0		#Глобалка для радио батона

def get_report():	# логинимся как КА блеа... хедерами имитируем лису, из тела хтмл вырываем супом 'javax.faces.ViewState' (для даты) без нее не фурычит, и еще нужно отвравлять форму со вежими куками каждый раз
	global_headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
		'Accept-Encoding': 'gzip, deflate'
	}

	ses_init = requests.get(BASE_URL, headers = global_headers)
	soup = BeautifulSoup(ses_init.content, 'html.parser')
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
		'j_id_4:username' : LOGIN_REP,
		'j_id_4:password' : PASSWORD_REP,
		'j_id_4:j_id_u' : 'Войти',
		'j_id_4_SUBMIT' : '1',
		'javax.faces.ViewState' : javax_faces_ViewState
	}
	r = requests.post(BASE_URL, headers = local_headers, data = data_r)  #борода которая логинится и получает все записи в репорте, ваще все во влкадке олл
	return str(r.content.decode('utf-8'))

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
			'down' : str(cols[11].find('span').string),
			'down_color' : (str(cols[11].span.get('style'))).split(':')[-1],
			'up' : str(cols[13].find('span').string),
			'up_color' : (str(cols[13].span.get('style'))).split(':')[-1],
			'resposible' : str(cols[-6].text),
			'add_info' : str(cols[-2].string).replace('\r\n', ' '),
			'updated' : str(cols[-1].string)
		})
	return report_table

def save_csv(report_table, path): # Вносим в CSV для наглядности хотя, можно и без этого
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Дата', 'BSC', 'BCF', 'Сайт','приоритет_BS', 'MC', 'Акб', 'АКБ_колор', 'Падение', 'Падение_колор', 'Поднятие', \
			'Поднятие_колор', 'Ответственные', 'add_info', 'Дежурный'))

		for rows in report_table:
			writer.writerow((rows['date'], rows['bsc'], rows['bcf'], rows['site'], rows['pr_bs'], rows['mc'], rows['akb'], rows['akb_color'], \
				rows['down'], rows['down_color'], rows['up'], rows['up_color'], rows['resposible'], rows['add_info'], rows['updated']))

def list_vnosa(list_dict):
	list_vnos = []
	for dic in list_dict:
		if (dic["down_color"] == "yellow") or (dic["up_color"] == "yellow"):
			if (dic['mc'] == "DNE") or (dic['mc'] == "ZAP") or (dic['mc'] == "KIR") or (dic['mc'] == "KRR"):
				dic['teritor'] = 1
			elif (dic['mc'] == "DON") or (dic['mc'] == "LUG") or (dic['mc'] == "MAR") or (dic['mc'] == "KRM") or (dic['mc'] == "SVD"):
				dic['teritor'] = 2
			elif (dic['mc'] == "KHA") or (dic['mc'] == "SHO") or (dic['mc'] == "KRE") or (dic['mc'] == "SUM") or (dic['mc'] == "POL"):
				dic['teritor'] = 3
			elif (dic['mc'] == "CHN") or (dic['mc'] == "ZHI") or (dic['mc'] == "CHK") or (dic['mc'] == "VIN"):
				dic['teritor'] = 4
			elif (dic['mc'] == "KIE"):
				dic['teritor'] = 5
			elif (dic['mc'] == "TER") or (dic['mc'] == "IVF") or (dic['mc'] == "CHR") or (dic['mc'] == "LUT") or (dic['mc'] == "UZH") or (dic['mc'] == "RIV"):
				dic['teritor'] = 6
			elif (dic['mc'] == "ODE") or (dic['mc'] == "NIK") or (dic['mc'] == "GEN") or (dic['mc'] == "IZM") or (dic['mc'] == "HER") or (dic['mc'] == "KOT"):
				dic['teritor'] = 7
			else:
				dic['teritor'] = 0
			list_vnos.append(dic)
	return list_vnos #выбираем из словаря то что можно вносить и и дописываем в виборку поле територии для радиобатона

def teritori():	# передаем аргумент глобал из радио баттона int
	teritor_res = []
	# print(rb)
	for row in list_vnosa(lst):
		if row['teritor'] == rb.get():
			teritor_res.append(row)
	return teritor_res

def checkbar(teritori):
	global fre1
	if fre1.winfo_viewable():
			fre1.destroy()
	fre1 = Frame(root, bd=5, relief=FLAT)
	lb_date = Label(fre1, text = "Date").grid(row = 0, column = 0)
	lb_bsc = Label(fre1, text = "BSC").grid(row = 0, column = 1)
	lb_bts = Label(fre1, text = "BTS").grid(row = 0, column = 2)
	lb_prio = Label(fre1, text = "Prio").grid(row = 0, column = 3)
	lb_check = Label(fre1, text = "Check").grid(row = 0, column = 4)
	lb_mc = Label(fre1, text = "M_cent").grid(row = 0, column = 5)
	lb_akb_time = Label(fre1, text = "akb_time").grid(row = 0, column = 6)
	lb_down_time = Label(fre1, text = "down_time").grid(row = 0, column = 7)
	lb_up_time = Label(fre1, text = "up_time").grid(row = 0, column = 8)
	# lb_resposible = Label(fre1, text = "resposible").grid(row = 0, column = 9)
	iter_t = 1
	for pick in teritori:
		lbi_date = Label(fre1, text = pick["date"], bd=2).grid(row = iter_t, column = 0)
		lbi_bsc = Label(fre1, text = pick["bsc"], bd=2).grid(row = iter_t, column = 1)
		lbi_bts = Label(fre1, text = pick["site"], bd=2).grid(row = iter_t, column = 2)
		lbi_prio = Label(fre1, text = pick["pr_bs"], bd=2).grid(row = iter_t, column = 3)
		var = IntVar()
		lbi_check = Checkbutton(fre1, variable=var, relief=GROOVE, bd=2).grid(row = iter_t, column = 4)
		lbi_mc = Label(fre1, text = pick["mc"], bd=2).grid(row = iter_t, column = 5)
		lbi_akb_time = Label(fre1, text = pick["akb"], bd=2, bg = colors(pick["akb_color"])).grid(row = iter_t, column = 6)
		lbi_down_time = Label(fre1, text = pick["down"], bd=2, bg = colors(pick["down_color"])).grid(row = iter_t, column = 7)
		lbi_up_time = Label(fre1, text = pick["up"], bd=2, bg = colors(pick["up_color"])).grid(row = iter_t, column = 8)
		# lbi_resposible = Label(fre1, text = pick["resposible"]).grid(row = iter_t, column = 9)
		vars.append({
			'var': var,
			'site': pick["site"]
			})

		iter_t +=1		
	fre1.grid(row = 1, column = 0)

def variki(): 
	# print(list(map(lambda var: var['var'].get(), vars)))
	vars_on = []
	for i in vars:
		if (i['var'].get() == 1) and (i['site'] not in vars_on):
			# print(i['site'], sep = ' ')
			vars_on.append(i['site'])
	print(vars_on)

def colors(color):
	if color == "yellow":
		res = "yellow"
	elif color == "ForestGreen":
		res = "light green"
	else:
		res = None
	return res

def sel():
	checkbar(teritori())

def form():
	
	global rb
	rb = IntVar()
	Radiobutton(fre2, text="ДТУ", variable=rb, value=1, command = sel).pack(side=LEFT, anchor = W)
	Radiobutton(fre2, text="ВТУ", variable=rb, value=2, command = sel).pack(side=LEFT, anchor = W)
	Radiobutton(fre2, text="СТУ", variable=rb, value=3, command = sel).pack(side=LEFT, anchor = W)
	Radiobutton(fre2, text="ЦТУ", variable=rb, value=4, command = sel).pack(side=LEFT, anchor = W)
	Radiobutton(fre2, text="КиТУ", variable=rb, value=5, command = sel).pack(side=LEFT, anchor = W)
	Radiobutton(fre2, text="ЗТУ", variable=rb, value=6, command = sel).pack(side=LEFT, anchor = W)
	Radiobutton(fre2, text="ЮТУ", variable=rb, value=7, command = sel).pack(side=LEFT, anchor = W)
	Button(fre2, text ='Обновить репорт', command = checkbar).pack(side=LEFT, anchor = W)
	Button(fre2, text = "Внести", command = variki).pack(side=LEFT, anchor = W)

if __name__ == '__main__':	
	project = []

	# report_f = get_report()
	# project.extend(parse(report_f))
	
	fi = open("datafile.pkl", 'rb')
	# f = open("datafile.pkl", "wb")
	# pickle.dump(x,f)
	lst = pickle.load(fi)
	rep_list = list_vnosa(lst)
	# save_csv(x, 'report.csv')
	root = Tk()
	root.geometry("540x700")
	fre2 = Frame(root, relief=GROOVE)
	fre2.grid(row = 0, column = 0)
	fre1 = Frame(root, bd=5, relief=FLAT)

	form()
	root.mainloop()
	# f.close()