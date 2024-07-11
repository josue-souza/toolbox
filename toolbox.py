import requests
from datetime import datetime
import json

class Toolbox():
    def __init__(self, url_firebase, key_weatherbit):
        self.url_firebase_json = url_firebase
        self.url_weatherbit = 'https://api.weatherbit.io/v2.0/current'
        self.key_weatherbit = key_weatherbit

    def request_api(self, url, method, str_json, str_data, str_params):
        if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
            response = getattr(requests, method.lower())(url, json=str_json, data=str_data, params=str_params)
            return response


    def post_to_do(self, date, name, task):
        json_data = {'data': date, 'nome': name, 'tarefa': task, 'status': 'não definido'}
        print(name)
        response = self.request_api(self.url_firebase_json, 'post', json_data, None, None)
        if response.status_code == 200:
            print('Tarefa criada com sucesso! \n')
            return response.json()
        else:
            print('Erro ao criar tarefa.')
            return None


    def list_to_do(self, date):
        response = self.request_api(self.url_firebase_json, 'get', None, None, None)
        date_now = response.json()
        api_return = []
        try:
            for value in date_now.values():
                value_date = value.get('data')
                if value_date == date:
                    name = value.get('nome')
                    task = value.get('tarefa') 
                    status = value.get('status')
                    api_return.append((date, name, task, status))
                        
            if not api_return:
                print('Não há tarefas para esta data!')
            return api_return
        except AttributeError:
            print('Banco de dados vazio!')
    
    def list_all_to_do(self):
        response = self.request_api(self.url_firebase_json, 'get', None, None, None)
        data = response.json()
        try:
            for value in data.values():
                date = value.get('data')
                name = value.get('nome')
                task = value.get('tarefa') 
                status = value.get('status')
                if status != 'realizado' and date != None and name != None:
                    print(f"\tData: {date} - Nome: {name}")
        except AttributeError:
            print('Banco de dados vazio!')
    

    def processing_data_to_do(self, task):
        response = self.request_api(self.url_firebase_json, 'get', None, None, None)
        data= response.json()
        desc_task = task
        key_node = None
        for key, valor_name in data.items():
            for data_key, valor_task in valor_name.items():
                if valor_task == desc_task:
                    key_node = key
                    break
        return key_node
 

    def update_to_do(self, node, date, name, task, status):
        params = {'data': date, 'nome': name, 'tarefa': task, 'status': status}
        data = json.dumps(params)
        url = self.url_firebase_json.strip('.json')
        response = self.request_api(f"{url}{node}.json", 'patch', None, data, None)
        if response.status_code == 200:
            updated_data = response.json()
        else:
            print(f"Ocorreu um erro durante o processo. {response.status_code}")
        return response.status_code


    def delete_to_do(self, node):
        url = self.url_firebase_json.strip('.json')
        node_delete = node
        response = self.request_api(f"{url}{node_delete}.json", 'delete', None, None, None)
        if response.status_code != 200:
            print('Não foi possível deletar a tarefa.')
        return response


    def menu_update_to_do(self, list_date):
        while True:
            for index_task, item in enumerate(list_date, start=1):
                date = item[0]
                name = item[1]
                task = item[2]
                status = item[3]
                if status is None:
                    status = 'Não definido'
                print(f"\n\t{index_task} - Data: {date} - Nome: {name}\n\tTarefa: {task}\n\tStatus: {status}")
            
            task_index = input('Escolha o número da tarefa para alterar: ')
            
            if task_index.lower() == 'q':
                break
            
            try:
                task_index = int(task_index) 
                if 1 <= task_index <= len(list_date):
                    selected_task = list(list_date[task_index - 1])
                    print(f"\nVocê selecionou a tarefa {task_index} - Nome: {selected_task[1]}")
                    print('\nEscolha uma opção:\n1 - Editar uma tarefa\n2 - Excluir uma tarefa')
                    task_option = input('Digite o número da opção desejada: ')
                    
                    if task_option == '1' or task_option.lower() == 'editar':
                        print('\n\t1 - Editar data\n\t2 - Editar nome\n\t3 - Editar tarefa\n\t4 - Editar status')
                        edit_option = input('Digite o número da opção desejada: ')
                        date_start = selected_task[0]
                        name_start = selected_task[1]
                        status_start = selected_task[3]
                        task_processing = selected_task[2]
                        if edit_option == '1' or edit_option.lower() == 'data':
                            edit_date = input('Digite a nova data (dd-mm-aaaa): ')
                            if edit_date == 'now':
                                edit_date = datetime.now().strftime('%d-%m-%Y')
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, edit_date, name_start, task_processing, status_start)
                            if update == 200:
                                print(f"\nData atualizada para {edit_date}")
                        elif edit_option == '2' or edit_option.lower() == 'nome':
                            edit_name = input('Digite o novo nome: ')
                            task_processing = selected_task[2]
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, date_start, edit_name, task_processing, status_start)
                            if update == 200:
                                print(f"\nNome atualizado para {edit_name}")

                        elif edit_option == '3' or edit_option.lower() == 'tarefa':
                            edit_task = input('Digite a nova tarefa: ')
                            task_processing = selected_task[2]
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, date_start, name_start, edit_task, status_start)
                            if update == 200:
                                print(f"\nTarefa atualizada para {edit_task}")

                        elif edit_option == '4' or edit_option.lower() == 'status':
                            edit_status = input('Digite o novo status (N, A, R): ')
                            if edit_status == 'N':
                                edit_status = 'não realizada'
                            elif edit_status == 'A':
                                edit_status = 'em andamento'
                            elif edit_status == 'R':
                                edit_status = 'realizado'
                            else:
                                print("Opção de status inválida.")
                                continue
                            task_processing = selected_task[2]
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, date_start, name_start, task_processing, edit_status)
                            if update == 200:
                                print(f"\nStatus alterado para {edit_status}")
                    
                    elif task_option == '2' or task_option.lower() == 'excluir':
                        task_processing = selected_task[2]
                        processing_node = self.processing_data_to_do(task_processing)
                        response = self.delete_to_do(processing_node)
                        if response.status_code == 200:
                            print('Tarefa excluída com sucesso')

                    else:
                        print("Opção inválida. Escolha 1 para editar ou 2 para excluir.")
                else:
                    print("Número de tarefa inválido.")
            except ValueError:
                print("Digite um número válido para a tarefa.")
        print("Saindo do menu de atualização de tarefas.")


    def validate_date(self, date_str):
        try:
            date = datetime.strptime(date_str, '%d-%m-%Y').strftime('%d-%m-%Y')
            return date
        except ValueError:
            return None


    def weather( self, city):
        api_key = self.key_weatherbit
        params = {
            'key': api_key,
            'city': city,
            'lang': 'pt'
        }
        response = self.request_api(self.url_weatherbit, 'get', None, None, params)
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


    def toolbox(self):
        while True:
            print('\nEscolha uma opção: \n 1 - Criar nova tarefa \n 2 - Listar tarefas \n 3 - Previsão do tempo')
            option_main = input('Digite o número da opção desejada: ')

            if option_main == '1' or option_main == 'criar':
                date = input('Digite a data (dd-mm-aaaa): ')
                if date == 'now':
                    date = datetime.now().strftime('%d-%m-%Y')
                if date == 'q':
                    self.toolbox()
                name = input('Digite o nome: ')
                if name == 'q':
                    self.toolbox()
                task = input('Digite a tarefa: ')
                self.post_to_do(date, name, task)

            elif option_main == '2' or option_main == 'listar':
                print('\nEscolha uma opção: \n 1 - Hoje \n 2 - Outra data \n 3 - Listar tarefas não realizadas')
                option_date = input('Digite o número da opção desejada: ')

                if option_date == '1':
                    date_now = datetime.now().strftime('%d-%m-%Y')
                    list_date = self.list_to_do(date_now)
                    if not list_date:
                        continue
                    else:
                        self.menu_update_to_do(list_date)

                elif option_date == '2':
                    date_input = input('Digite a data (dd-mm-aaaa): ')
                    date_validate = self.validate_date(date_input)
                    if date_validate:
                        list_date = self.list_to_do(date_validate)
                        if not list_date:
                            continue
                        else:
                            self.menu_update_to_do(list_date)
                elif option_date == '3':
                    self.list_all_to_do()

                elif option_date == 'q':
                    self.toolbox()

                else:
                    print('Opção inválida!')
            elif option_main == '3' or option_main == 'previsao':
                city = input('Digite o nome da cidade: ')
                self.weather(city)
                if option_main == 'q':
                    self.toolbox()

            else:
                print('Opção inválida!')

url_firebase = '##########'
waetherbit_key = '##########'

toolbox = Toolbox(url_firebase, waetherbit_key)
main = toolbox.toolbox()
