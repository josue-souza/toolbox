import requests
from datetime import datetime


def get_api():
    url = 'COLOQUE AQUI O CAMINHO DO SEU GOOGLE FIREBASE'
    response = requests.get(url)
    data = response.json()
    return data

def post_api(data, nome, tarefa):
    url = 'https://to-do-a207f-default-rtdb.firebaseio.com/.json'
    json_data = {data: {'nome': nome, 'tarefa': tarefa}}
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        print('Tarefa criada com sucesso! \n')
        return response.json()
    else:
        print('Erro ao criar tarefa.')
        return None

def list_api(data):
    date_now = get_api()
    api_retorno = []
    for value in date_now.values():
        for item_key, item_value in value.items():
            if item_key == data:
                nome = item_value['nome']
                tarefa = item_value['tarefa']
                api_retorno.append((nome, tarefa))

    if not api_retorno:
        print('Não há tarefas para esta data!')

    return api_retorno

def validar_data(data_str):
    try:
        data = datetime.strptime(data_str, '%d-%m-%Y').strftime('%d-%m-%Y')
        return data
    except ValueError:
        return None


def weather(cidade):
  API_KEY = 'COLOQUE AQUI SUA API KEY OBTIDA NO SITE ABAIXO:'
  base_url = 'https://api.weatherbit.io/v2.0/current'
  params = {
      'key': API_KEY,
      'city': cidade,
      'lang': 'pt'
  }
  response = requests.get(base_url, params=params)
  if response.status_code == 200:
      data = response.json()
      location_name = data['data'][0]['city_name']
      temperature = data['data'][0]['temp']
      weather_description = data['data'][0]['weather']['description']
      previsao = f'\n \tCondições climáticas em {location_name}: \n \tTemperatura atual: {temperature}°C \n \tDescrição do tempo: {weather_description}'
      print(previsao)
  else:
      print(f'Erro ao acessar a API da Weatherbit. Código de status: {response.status_code}')
  return previsao


def to_do():
    while True:
        print('\nEscolha uma opção: \n 1 - Criar nova tarefa \n 2 - Listar tarefas \n 3 - Previsão do tempo')
        criar_listar = input('Digite o número da opção desejada: ')

        if criar_listar == '1' or criar_listar == 'criar':
            data = input('Digite a data (dd-mm-aaaa): ')
            if data == 'q':
                to_do()
            nome = input('Digite o nome: ')
            if nome == 'q':
                to_do()
            tarefa = input('Digite a tarefa: ')
            post_api(data, nome, tarefa)

        elif criar_listar == '2' or criar_listar == 'listar':
            print('\nEscolha uma opção: \n 1 - Hoje \n 2 - Outra data')
            data_opcao = input('Digite o número da opção desejada: ')

            if data_opcao == '1':
                data_atual = datetime.now().strftime('%d-%m-%Y')
                list_data = list_api(data_atual)
                if not list_data:
                    print('Sem tarefas para esta data.')
                else:
                    for indice, item in enumerate(list_data, start=1):
                        print(f"\n \t{indice} - Nome: {item[0]} \n    \tTarefa: {item[1]}\n")

            elif data_opcao == '2':
                data_input = input('Digite a data (dd-mm-aaaa): ')
                data_validada = validar_data(data_input)
                if data_validada:
                    list_data = list_api(data_validada)
                    if not list_data:
                        print('Sem tarefas para esta data.')
                    else:
                        for indice, item in enumerate(list_data, start=1):
                            print(f"\n \t{indice} - Nome: {item[0]} \n    \tTarefa: {item[1]}\n")

            elif data_opcao == 'q':
                to_do()

            else:
                print('Opção inválida!')
        elif criar_listar == '3' or criar_listar == 'previsao':
          cidade = input('Digite o nome da cidade: ')
          if cidade == 'q':
            to_do()
          weather(cidade)
        elif criar_listar == 'q':
            to_do()

        else:
            print('Opção inválida!')

to_do()
