import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver



class TikTokScraper:
    def __init__(self, username, num_pages):
        self.driver = webdriver.Chrome()
        self.num_pages = num_pages
        self.username = username
        self.url_template = 'https://www.tiktok.com/@{username}'

    async def fetch(self, url):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                return await response.text()

    async def get_videos_links(self, page, is_category: bool = False):
        pattern = 'https://www.tiktok.com/@{0}/video/'.format(self.username)
        if is_category:
            self.url_template = 'https://www.tiktok.com/tag/{username}'
            pattern = r"https://www\.tiktok\.com/(@\w+)/video/(\d+)"
        url = self.url_template.format(username=self.username, page=page)
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(8)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # html = await self.fetch(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        links = [{'url': a['href']} for a in soup.find_all('a', href=re.compile(pattern))]
        self.driver.quit()

        if page > self.num_pages:
            return []
        return links

    async def scrape(self, is_category: bool = False):
        tasks = [self.get_videos_links(page, is_category) for page in range(1, self.num_pages + 1)]
        results = await asyncio.gather(*tasks)
        list_links = [link for page_links in results for link in page_links]
        return [{'id': url['url'].split('/')[-1], 'url': url['url']} for url in list_links]
