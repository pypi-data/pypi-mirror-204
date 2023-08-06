from .app.start import start_app
from .args import get_args


def main() -> None:
    start_app(get_args())


if __name__ == "__main__":
    main()
