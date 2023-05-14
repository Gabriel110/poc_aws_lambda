import json

def enrich_message(message, enrichment):
  message['nome'] = enrichment
  return message
  
def json_merge(message, enrichment):
  message.update(enrichment)
  return message
  
def main():
  texto = '{"nascimento": "16-12-1996","cpf": "10777197014"}'
  json_entrada = json.loads(texto)
  json_entrada2 = json.loads('{"nome":"gabriel", "sexo":"masculino"}')
  
  mensaagem = json_merge(json_entrada, json_entrada2)
  print('menssagem = {}'.format(mensaagem))
  
if __name__ == '__main__':
  main()