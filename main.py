import asyncio
from kissmanga.kissmanga import kissmanga
from kissmanga.config import NUM_CONCURRENT_TASKS


def main():
    semaphore = asyncio.Semaphore(NUM_CONCURRENT_TASKS)
    loop = asyncio.get_event_loop()
    kissmanga_gathering = kissmanga(semaphore)
    loop.run_until_complete(kissmanga_gathering)


if __name__ == "__main__":
    main()