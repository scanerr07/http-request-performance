import time
import asyncio
import requests
import aiohttp
import threading

# --- SENKRON (tek tek, en yavaş yöntem) ---
def get_data_sync(urls):
    st = time.time()                                  # Başlangıç zamanı
    json_array = []
    for url in urls:                                  # URL'leri sırayla çalıştırır
        json_array.append(requests.get(url).json())   # Her seferinde 3 sn bekler
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds') # Toplam geçen süre
    return json_array


# --- ASENKRON ama SIRAYLA (yine yavaş, wrapper gibi) ---
async def get_data_async_but_as_wrapper(urls):
    st = time.time()
    json_array = []
    async with aiohttp.ClientSession() as session:
        for url in urls:                              # Tek tek istek atar (senkrona benzer)
            async with session.get(url) as resp:
                json_array.append(await resp.json())
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    return json_array


# --- ASENKRON yardımcı fonksiyon (tek bir URL için) ---
async def get_data(session, url, json_array):
    async with session.get(url) as resp:
        json_array.append(await resp.json())


# --- ASENKRON GERÇEK PARALEL (hepsini aynı anda, en hızlı yöntem) ---
async def get_data_async_concurrently(urls):
    st = time.time()
    json_array = []
    async with aiohttp.ClientSession() as session:
        tasks = []                                    # Görevler listesi oluştur
        for url in urls:
            tasks.append(asyncio.ensure_future(get_data(session, url, json_array)))
        await asyncio.gather(*tasks)                  # Tüm istekleri aynı anda çalıştır
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    return json_array


# --- THREADING ile (çoklu iş parçacığı) ---
class ThreadingDownloader(threading.Thread):
    json_array = []
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):                                    # Thread çalıştığında yapılacak iş
        response = requests.get(self.url)             # URL'den veri çek
        self.json_array.append(response.json())
        return self.json_array


def get_data_threading(urls):
    st = time.time()
    threads = []
    for url in urls:                                  # Her URL için yeni bir thread başlat
        t = ThreadingDownloader(url)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()                                      # Tüm thread'ler bitene kadar bekle
        print(t)
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


# --- TEST URL'LERİ (her biri 3 sn gecikmeli cevap verir) ---
urls = ['https://postman-echo.com/delay/3'] * 10

#get_data_sync(urls)                  # ≈42 sn sürer (en yavaş)
#asyncio.run(get_data_async_but_as_wrapper(urls)) # ≈34 sn sürer
#asyncio.run(get_data_async_concurrently(urls))   # ≈4 sn sürer (en hızlı)
#get_data_threading(urls)             # ≈4 sn sürer (çoklu iş parçacığı)
