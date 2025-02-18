from presenter.app import app

__all__ = ("app",)

if __name__ == "__main__":
    from argparse import ArgumentParser
    from fastapi.openapi.utils import get_openapi
    from json import dump
    from sys import stdout

    parser = ArgumentParser()
    parser.add_argument(
        "--docs",
        "-D",
        action="store_true",
        default=False,
        help="Generate docs into stdout",
    )
    namespace = parser.parse_args()

    if namespace.docs:
        docs = get_openapi(title=app.title, version=app.version, routes=app.routes)
        dump(docs, stdout, indent=4)
