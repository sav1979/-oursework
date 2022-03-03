# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:19:47 2022

@author: sklad_2
"""

import os
import requests
import datetime
import json
from tqdm import tqdm

    # Чтения токена и ID пользователя из файла
def get_my_token_id(file_name):
    with open(os.path.join(os.getcwd(), file_name), 'r') as reading_file:
        token = reading_file.readline().strip()
        my_id = reading_file.readline().strip()
    return [token, my_id]


    # Cсылка на фото макс. размера и размер фото
def search_max_dpi(dict_in_search):
    max_dpi = 0
    size_elem = 0
    for j in range(len(dict_in_search)):
        file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            size_elem = j
    return dict_in_search[size_elem].get('url'), dict_in_search[size_elem].get('type')


    # Преобразование даты фото в др. формат
def time_convert(time_unix):
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time


# Запрос VK
class VkRequest:
    def __init__(self, token_list, version='5.131'):
        self.token = token_list[0]
        self.id = token_list[1]
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self._sort_info()


# Получение фото (кол-во)
    def _get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1,
                  'rev': 0
                  }
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']
        return photo_info['count'], photo_info['items']
    

# Словарь с фото
def _get_logs_only(self):
    photo_count, photo_items = self._get_photo_info()
    result = {}
    for i in range(photo_count):
        likes_count = photo_items[i]['likes']['count']
        url_download, picture_size = find_max_dpi(photo_items[i]['sizes'])
        time_warp = time_convert(photo_items[i]['date'])
        new_val = result.get(likes_count, [])
        new_val.append({'add_name': time_warp,
                          'url_picture': url_download,
                          'size': picture_size})
        result[likes_count] = new_val
    return result


# Словарь с парам-ми фото и JSON под выгрузку
def _sort_info(self):
    json_list = []
    sort_dict = {}
    picture_dict = self._get_logs_only()
    counter = 0
    for elem in picture_dict.keys():
        for value in picture_dict[elem]:
            if len(picture_dict[elem]) == 1:
                file_name = f'{elem}.jpeg'
            else:
                file_name = f'{elem} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                sort_dict[file_name] = picture_dict[elem][counter]['url_picture']
                counter += 1
    return json_list, sort_dict


# Загрузка фото на ЯндексДиск
class Yandex:
    def __init__(self, folder_name, token_list):
        self.token = token_list[0]
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self._create_folder(folder_name)
        
        
# Создания папки на Я-диске
    def _create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\n Папка {folder_name} успешно создана \n')
        else:
            print(f'\n Папка {folder_name} уже существует.\n')
        return folder_name
    
    
# Ссылка для загрузки фотографий
    def _in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for element in resource:
            in_folder_list.append(element['name'])
        return in_folder_list


# Загрузка фото
    def create_copy(self, dict_files):
        files_in_folder = self._in_folder(self.folder)
        added_files_num = 0
        for key, i in zip(dict_files.keys(), tqdm(list(dict_files.keys()))):
            if added_files_num < 5:
                if key not in files_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key],
                              'overwrite': 'false'}
                    requests.post(self.url, headers=self.headers, params=params)
                    added_files_num += 1
                else:
                    print(f'Файл {key} уже существует')
            else:
                break
        print(f'\nЗапрос завершен, файлы скопированны: {added_files_num}')
        
# if __name__ == '__main__':