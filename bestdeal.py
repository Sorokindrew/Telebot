import requests
import json

url = 'https://hotels4.p.rapidapi.com/properties/v2/list'
sort_string = 'PRICE_RELEVANT'


def bestdeal():
	"""
	Функция для нахождения топ самых выгодных предложений.
	:return: list список отелей оптимальных по сооьношению цена / качество
	"""
	return 'Узнать топ отелей, наиболее подходящих по цене и расположению ' \
	       'от центра'