import requests
import json
from celery import shared_task
from SyncModule.libs import ping_external_server, generate_changes_file
from Core.config import REMOTE_ADDRES_SERVER
from django.apps import apps

@shared_task
def InitSyncProcedure():
    # Проверить доступность
    serverAvailable = ping_external_server()

    # Сгенерировать файл
    changeFileUrl = generate_changes_file('init')

    # Отправить файл
    if serverAvailable:
        remote_server_url = REMOTE_ADDRES_SERVER + '/dbw/file_acceptance/'

        # Открываем файл в бинарном режиме
        with open(changeFileUrl, 'rb') as file:
            # Отправляем файл на удаленный сервер
            response = requests.post(remote_server_url, files={'file': file})

            if response.status_code == 200:
                print('[DBS] Файл синхронизации отправлен')
            else:
                print(response.json())
                print('[DBS] Что-то сломалось...')
    else:
        print('[DBS] Файл синхронизации не был отправлен')

@shared_task
def AcceptanceOfChanges(filepath):
    # Проверить доступность
    # serverAvailable = ping_external_server()

    with open(filepath, 'r') as file:
        data = json.load(file)

    applied_changes = []
    changes = data.get("changes", [])

    for change in changes:
        id = change["id"]
        model_name = change["model_name"]
        record_id = change["record_id"]
        change_type = change["change_type"]
        new_state = change["new_state"]
        new_state.pop('id', None)
        # Получаем модель по имени
        model = apps.get_model(app_label='WareHouse', model_name=model_name)

        # В зависимости от типа изменения, выполняем соответствующие действия
        if change_type == 'insert':
            # Создаем новую запись
            instance = model(id=record_id, **new_state)
            instance._is_local_sync = True
            instance.save()
        elif change_type == 'update':
            # Обновляем существующую запись
            instance = model.objects.get(id=record_id)
            instance._is_local_sync = True
            for field, value in new_state.items():
                setattr(instance, field, value)
            instance.save()
        elif change_type == 'delete':
            # Удаляем запись
            instance = model.objects.get(id=record_id)
            instance._is_local_sync = True
            instance.delete()

        # Добавляем ID примененного изменения в список
        applied_changes.append(id)
    applied_changes_response = data.get("applied_changes", [])
    if applied_changes_response != []:
        for id_r in applied_changes_response:
            print(f'Change {id_r} aplied')
    
    
    changeFileUrl = generate_changes_file('response', applied_changes)
    
    serverAvailable = ping_external_server() 
    
    if serverAvailable:
        remote_server_url = REMOTE_ADDRES_SERVER + '/dbw/file_acceptance/'

        # Открываем файл в бинарном режиме
        with open(changeFileUrl, 'rb') as file:
            # Отправляем файл на удаленный сервер
            response = requests.post(remote_server_url, files={'file': file})

            if response.status_code == 200:
                print('[DBS] Файл синхронизации отправлен')
            else:
                print(response.json())
                print('[DBS] Что-то сломалось...')
    else:
        print('[DBS] Файл синхронизации не был отправлен')