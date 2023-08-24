import asyncio
import sys

from dotenv import load_dotenv

from tiktok_to_blumer import TiktokToBlumer

load_dotenv()
username = 'jasantaolalla'
num_pages = 1
chromedriver_path = '/usr/local/bin/chromedriver'
download_folder = '/home/jgabriel2g/Downloads/cloning-main/categories_videos/home_and_garden/organization'


def get_array(arreglo):
    print("Cuantas o categoria a minar : ", arreglo)


if __name__ == "__main__":
    if len(sys.argv[2:]) == 0:
        raise ValueError("Tienes que pasar parametros")
    for item in sys.argv[2:]:
        blumer_start = TiktokToBlumer(item, num_pages, chromedriver_path, download_folder)

        if "--category" in sys.argv:
            results = asyncio.run(blumer_start.start_cloning(True))
        elif "--user" in sys.argv:
            results = asyncio.run(blumer_start.start_cloning())

            get_array(sys.argv[2:])
