import requests
import json

url = 'https://hotels4.p.rapidapi.com/properties/v2/list'
sort_string = 'PRICE_LOW_TO_HIGH'


def highprice():
	"""
	Функция для нахождения топ самых дорогих отелей.
	:return: list список самых дорогих отелей

	"""
	return 'Узнать топ самых дорогих отелей в городе'