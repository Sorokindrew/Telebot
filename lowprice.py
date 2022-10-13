import json
import requests

url = 'https://hotels4.p.rapidapi.com/properties/v2/list'
sort_string = 'PRICE_LOW_TO_HIGH'


def lowprice(headers, querystring):
	"""
	Функция для нахождения топ самых дешевых отелей.
	:return: list список самых дешевых отелей

	"""
	response = requests.request('POST',
	                            url=url,
	                            headers=headers,
	                            params=querystring)

	data = json.loads(response.text)
	return 'Узнать топ самых дешевых отелей в городе'

