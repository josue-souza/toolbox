import requests
from datetime import datetime
import json
from firebase_admin import db

class Toolbox():
    def __init__(self):
        self.url_firebase = '###'
        self.url_firebase_json = '###'
        self.url_weatherbit = 'https://api.weatherbit.io/v2.0/current'

    def request_api(self, url, method, str_json, str_data, str_params):
        if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
            response = getattr(requests, method.lower())(url, json=str_json, data=str_data, params=str_params)
            return response


    def post_to_do(self, date, name, task):
        json_data = {date: {'nome': name, 'tarefa': task}}
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
        for value in date_now.values():
            for item_key, item_value in value.items():
                if item_key == date:
                    name = item_value.get('nome')
                    task = item_value.get('tarefa') 
                    status = item_value.get('status')
                    api_return.append((date, name, task, status))
                    
        if not api_return:
            print('Não há tarefas para esta data!')
        return api_return
    

    def processing_data_to_do(self, task):
        response = self.request_api(self.url_firebase_json, 'get', None, None, None)
        data= response.json()
        desc_task = task
        key_node = None
        for key, valor_name in data.items():
            for data_key, valor_task in valor_name.items():
                if 'tarefa' in valor_task and valor_task['tarefa'] == desc_task:
                    key_node = key
                    break
        return key_node
 

    def update_to_do(self, node, date, name, task, status):
        if date != None:
            params = {node: {'data': date}}
            data = json.dumps(params)
            response = self.request_api(self.url_firebase_json, 'patch', None, data, None)
            if response.status_code == 200:
                updated_data = response.json()
                print('\n \tData alterada com sucesso!')
            else:
                print(f"Ocorreu um erro durante o processo. {response.status_code}")
        if name != None:
            params = {node: {'nome': name}}
            data = json.dumps(params)
            response = self.request_api(self.url_firebase_json, 'patch', None, data, None)            
            if response.status_code == 200:
                print('\n \tNome alterado com sucesso!')
            else:
                print(f"Ocorreu um erro durante o processo. {response.status_code}")

        if task != None:
            params = {node: {'tarefa': task}}
            data = json.dumps(params)
            response = self.request_api(self.url_firebase_json, 'patch', None, data, None)
            if response.status_code == 200:
                print('\n \tTarefa alterada com sucesso!')
            else:
                print(f"Ocorreu um erro durante o processo. {response.status_code}")
        if status != None:
            params = {node: {'status': status}}
            data = json.dumps(params)
            response = self.request_api(self.url_firebase_json, 'patch', None, data, None)
            if response.status_code == 200:
                print('\n \Status alterado com sucesso!')
            else:
                print(f"Ocorreu um erro durante o processo. {response.status_code}")
        self.toolbox()


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
                        
                        if edit_option == '1' or edit_option.lower() == 'data':
                            edit_date = input('Digite a nova data (dd-mm-aaaa): ')
                            date_start = selected_task[0]
                            name_start = selected_task[1]
                            status_start = selected_task[3]
                            task_processing = selected_task[2]
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, edit_date, None, None, None)

                        elif edit_option == '2' or edit_option.lower() == 'nome':
                            edit_name = input('Digite o novo nome: ')
                            task_processing = selected_task[2]
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, None, edit_name, None, None)
                            print(f"\nNome atualizado para {edit_name}")

                        elif edit_option == '3' or edit_option.lower() == 'tarefa':
                            edit_task = input('Digite a nova tarefa: ')
                            task_processing = selected_task[2]
                            processing_node = self.processing_data_to_do(task_processing)
                            update = self.update_to_do(processing_node, None, None, edit_task, None)
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
                            update = self.update_to_do(processing_node, None, None, None, edit_status)
                            print(f"\nStatus alterado para {edit_status}")
                    
                    elif task_option == '2' or task_option.lower() == 'excluir':
                        list_date.remove(selected_task)
                        print(f"Tarefa '{selected_task[1]}' excluída com sucesso.")
                    
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
        API_KEY = '###'
        params = {
            'key': API_KEY,
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
                if date == 'q':
                    self.toolbox()
                name = input('Digite o nome: ')
                if name == 'q':
                    self.toolbox()
                task = input('Digite a tarefa: ')
                self.post_to_do(date, name, task)

            elif option_main == '2' or option_main == 'listar':
                print('\nEscolha uma opção: \n 1 - Hoje \n 2 - Outra data')
                option_date = input('Digite o número da opção desejada: ')

                if option_date == '1':
                    date_now = datetime.now().strftime('%d-%m-%Y')
                    list_date = self.list_to_do(date_now)
                    if not list_date:
                        print('Sem tarefas para esta data.')
                    else:
                        self.menu_update_to_do(list_date)

                elif option_date == '2':
                    date_input = input('Digite a data (dd-mm-aaaa): ')
                    date_validate = self.validate_date(date_input)
                    if date_validate:
                        list_date = self.list_to_do(date_validate)
                        if not list_date:
                            print('Sem tarefas para esta data.')
                        else:
                            self.menu_update_to_do(list_date)

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

toolbox = Toolbox()
main = toolbox.toolbox()
