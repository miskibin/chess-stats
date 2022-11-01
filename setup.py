from setuptools import setup

if __name__ == "__main__":
    setup(
        name="games_parser",
        version="0.1.0",
        description="This is a chess game analyzer",
        author="Michał Skibiński",
        package_dir={"": "src"},
        license="MIT",
        packages=["games_parser"],
    )
