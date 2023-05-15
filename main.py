import json
import requests

def enrich_message(message, enrichment):
  message['nome'] = enrichment
  return message
  
def json_merge(message, enrichment):
  message.update(enrichment)
  return message

def getName():
  try:
    response = requests.get(url="http://localhost:8882/api/rest")
    response_json = response.json()
    return response_json
  except Exception as e:
    print('Failed to get request')
    return {'status': 'error', 'message': str(e)}
  
def main():
  texto = '{"nascimento": "16-12-1996","cpf": "10777197014"}'
  response = getName()
  json_entrada = json.loads(texto)
  json_entrada2 = response
  
  mensaagem = json_merge(json_entrada, json_entrada2)
  print('menssagem = {}'.format(mensaagem))
  
if __name__ == '__main__':
  main()