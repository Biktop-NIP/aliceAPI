from typing import Iterable

import aiofiles
import asyncio
import aiohttp
import requests
import conf


def get_images() -> list[str]:
    '''
    Возвращает список всех загруженных изображений
    '''
    response = requests.get(conf.URL_IMAGE, headers={'Authorization': 'OAuth '+ conf.TOCEN})
    images_ids = []
    for image in response.json()['images']:
        images_ids.append(image['id'])
    return images_ids


def upload_image(path: str) -> str:
    ''' 
    Загружает изоброжание в навык
    Принимает: 
        path - путь до файла
    Возвращает: 
        индификатор изображнеия
    '''
    headers = { 'Authorization': 'OAuth '+ conf.TOCEN }
    
    with open(path, 'rb') as file:
        files = {'file': (path, file)}
        response = requests.post(conf.URL_IMAGE, files=files, headers=headers)
        data = response.json()
        image_id = data['image']['id']

        return image_id
    

def upload_images(paths: Iterable[str]) -> list[str]:
    ''' 
    асинхроно загружает список изображений
    Принимает:
        paths - список путей до изображений
    Возвращает:
        список индификаторов изображений
    '''
    
    async def upload(path, session, ids, i):
        headers = { 'Authorization': 'OAuth '+ conf.TOCEN }
        async with aiofiles.open(path, 'rb') as file:
                    data = aiohttp.FormData()
                    data.add_field('file',
                            open(path, 'rb'),
                            filename=path,
                            content_type='application/vnd.ms-excel')
                
                    async with session.post(conf.URL_IMAGE, data=data, 
                                            headers=headers) as response:
                        
                        json = await response.json()
                        ids.append((json['image']['id'], i))
    
    
    async def main(paths, ids):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i, path in enumerate(paths):
                tasks.append(upload(path, session, ids, i))
        
            return await asyncio.gather(*tasks)
    
    images_ids = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(paths, images_ids))
    return [i[0] for i in sorted(images_ids, key=lambda x: x[1])]


def upload_image_url(url: str) -> str:
    ''' 
    Загружает изоброжание в навык
    Принимает: 
        url - адрес изображения
    Возвращает: 
        индификатор изображнеия
    '''
    headers = {'Authorization': 'OAuth '+ conf.TOCEN, 'Content-Type': 'application/json'}
    data = {'url': url}
    response = requests.post(conf.URL_IMAGE, headers=headers, json=data)
    data = response.json()
    image_id = data['image']['id']
    return image_id


def upload_images_url(urls: Iterable[str]) -> list[str]:
    '''
    асинхроно загружает список изображений
    Принимает:
        urls - список адресов изображений
    Возвращает:
        список индификаторов изображений
    '''
    async def upload(url, session, ids, i):
        headers = {'Authorization': 'OAuth '+ conf.TOCEN, 'Content-Type': 'application/json'}
        async with session.post(conf.URL_IMAGE, headers=headers, json={'url': url}) as response:
            json = await response.json()
            ids.append((json['image']['id'], i))
            
        
    async def main(urls, ids):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i, url in enumerate(urls):
                tasks.append(upload(url, session, ids, i))
                
            return await asyncio.gather(*tasks)
    
    images_ids = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls, images_ids))
    return [i[0] for i in sorted(images_ids, key=lambda x: x[1])]
 

def delety_image(image_id: str) -> None:
    '''
    Удаляет изображение по айди
    '''
    response = requests.delete(conf.URL_IMAGE+image_id, 
                               headers={'Authorization': 'OAuth '+ conf.TOCEN})
    

def delety_images(images_ids: Iterable[str]) -> None:
    '''
    асахронно удаляет список изображений принимает список индификаторов изображений 
    '''
    async def delete(image_id, session):
        async with session.delete(conf.URL_IMAGE+image_id, 
                       headers={'Authorization': 'OAuth '+ conf.TOCEN}): pass
    
    
    async def main(imades_ids):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for image_id in imades_ids:
                tasks.append(delete(image_id, session))
            
            return await asyncio.gather(*tasks)
        
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(images_ids))
    