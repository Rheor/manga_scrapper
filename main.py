import asyncio
from kissmanga.aggregators.website import kissmanga
from kissmanga.config import NUM_CONCURRENT_TASKS

# point is to have the possibility to switch downloader at the entrypoint of the project
# in the  future when needs ask for it
# ex: send the files to an upstream bucket / filesystem
# for now, we use a downloader that handles downloading locally
from kissmanga.downloader import LocalMangaDownloader


def main():
    semaphore = asyncio.Semaphore(NUM_CONCURRENT_TASKS)
    asyncio.run(kissmanga(semaphore, LocalMangaDownloader))


if __name__ == "__main__":
    main()