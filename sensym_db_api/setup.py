import setuptools

setuptools.setup(
    name="sensym_db_api",
    version="1.0.0",
    author="Omar Elsayd",
    email="omar_2546@hotmail.com",
    discription="Database models and apis for sensym app",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3.10"],
    install_requires=[
        "sqlalchemy",
        "fastapi",
        "uvicorn",
        "alembic",
        "psycopg2",
        "pyaudio",
        "python-dotenv",
        "librosa",
        "matplotlib",
        "nltk",
        "textblob",
        "transformers"
        ]
    )