from utils.mongo import connect_to_db


def pytest_configure():
    connect_to_db()
