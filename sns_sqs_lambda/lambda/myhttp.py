import requests
import json


class Feign:

  url = "http://localhost:8882/api/rest"

  def getName(self):
    try:
      response = requests.get(url=self.url)
      response_json = response.json()
      return response_json
    except Exception as e:
      print('Failed to get request')
      return {'status': 'error', 'message': str(e)}