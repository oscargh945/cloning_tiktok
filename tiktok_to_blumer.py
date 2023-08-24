from use_cases.tik_tok_scraper import TikTokScraper
from use_cases.tiktok_download_link import TikTokItemVideo



class TiktokToBlumer(TikTokScraper, TikTokItemVideo):
    def __init__(self, username, num_pages, chromedriver_path, download_folder):
        super().__init__(username, num_pages)
        TikTokItemVideo.__init__(self, chromedriver_path=chromedriver_path, download_folder=download_folder)

    async def start_cloning(self, is_category: bool = False):
        video_links = await self.scrape(is_category)
        print(video_links)
        print(f"total de videos: {len(video_links)}")
        download = [await self.get_video(video_url=video['url'], video_id=video['id']) for video in video_links]
        videos_with_category = [{**video, "username": self.username} for video in download]
