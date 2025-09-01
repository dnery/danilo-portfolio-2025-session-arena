from app.config import settings
from rich import print


def main():
    print(settings)
    print(settings.redis_url)
    print(settings.database_url)


if __name__ == "__main__":
    main()
