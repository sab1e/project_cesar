import sqlite3
from http import HTTPStatus

from core.application import Application
from core.models import Project
from core.test_mappers import ProjectMapper
from core.templates import render
from settings import DB_NAME, INDEX_HEAD, INDEX_FOOT

connection = sqlite3.connect(DB_NAME)
mapper = ProjectMapper(connection, Project)


def index_view(request):
    projects = mapper.get_all()
    return f'{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}', \
           render('index.html', projects=projects)


urls = {'/': index_view}
middlewares = []

application = Application(urls, middlewares)

# uwsgi --http :8000 --wsgi-file view.py
