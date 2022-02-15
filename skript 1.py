# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:19:47 2022

@author: sklad_2
"""
    # Чтения токена и ID пользователя из файла псстрочно
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
