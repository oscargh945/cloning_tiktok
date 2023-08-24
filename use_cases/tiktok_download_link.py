import asyncio
import os
from typing import Dict

import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TikTokItemVideo:
    def __init__(self, chromedriver_path, download_folder) -> None:
        self.chromedriver_path = chromedriver_path
        self.service = None
        self.driver = None
        self.video_url = None
        self.download_link = None
        self.filename = None
        self.download_folder = download_folder

    async def start_driver(self) -> None:
        self.service = Service(self.chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service)

    async def stop_driver(self) -> None:
        if self.driver:
            self.driver.quit()

    async def get_video(self, video_url: str, video_id: str) -> dict[str, str] | dict[str, None]:
        self.video_url = video_url
        await self.start_driver()
        try:
            self.driver.get('https://tiktokdownloader.com/')
            search_box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "tiktokUrl"))
            )
            search_box.send_keys(self.video_url)
            download_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "loadVideos"))
            )
            download_btn.click()
            await asyncio.sleep(2)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            download_div = soup.find('div', {'id': 'downloadNoWatermark'})
            self.download_link = download_div.find('button')['data-media-url']
            self.filename = download_div.find('button')['data-filename']
            video_content = await self.fetch_video_content(self.download_link)

            if video_content:
                video_path = os.path.join(self.download_folder, f"{video_id}{self.filename}")
                with open(video_path, 'wb') as video_file:
                    video_file.write(video_content)
                return {
                    'url': video_path,  # Guardamos la ruta local del video descargado
                    'filename': f"{video_id}{self.filename}"
                }
            else:
                print(f"No se pudo obtener el video {video_id}")
                return {
                    'url': None,
                    'filename': None
                }
        finally:
            await self.stop_driver()

    async def fetch_video_content(self, video_url: str):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get(video_url) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        print(f"Error al obtener el video en {video_url}.  {response.status}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Error al hacer la solicitud HTTP: {e}")
                return None
