import asyncio
from kissmanga.kissmanga import kissmanga


def main():
    loop = asyncio.get_event_loop()
    kissmanga_gathering = kissmanga()
    loop.run_until_complete(kissmanga_gathering)


if __name__ == "__main__":
    main()