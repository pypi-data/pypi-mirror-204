from setuptools import setup, find_packages


def main() -> None:
    import ledes_parser as app

    setup(
        name='ledes-parser',
        version=app.__version__,
        packages=find_packages(),
        install_requires=[
            # List your package dependencies here
        ],
        author='Travis Bashor',
        author_email='travis.bashor@gmail.com',
        description='A package for parsing LEDES format files',
        url='https://github.com/travisbashor/ledes-parser',
    )


if __name__ == "__main__":
    main()
