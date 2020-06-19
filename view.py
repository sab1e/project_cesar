import sqlite3

from core.application import Application
from core.models import Project
from core.test_mappers import ProjectMapper
from settings import DB_NAME, INDEX_HEAD, INDEX_FOOT


connection = sqlite3.connect(DB_NAME)
mapper = ProjectMapper(connection, Project)


def index_view(request):
    projects = mapper.get_all()
    body = ''
    for project in projects:
        body += f'<div class ="col-sm">{project.id_project}</div>' \
                f'<div class ="col-sm">{project.name}</div>' \
                f'<div class ="col-sm">' \
                f'{"" if project.from_date is None else project.from_date}' \
                f'</div><div class ="col-sm">' \
                f'{"" if project.to_date is None else project.to_date}' \
                f'</div><div class ="col-sm">' \
                f'{"" if project.manager is None else project.manager}' \
                f'</div><div class ="col-sm">' \
                f'{"" if project.employees is None else project.employees}' \
                f'</div><div class ="col-sm">' \
                f'{"" if project.tasks is None else project.tasks}</div>' \
                f'<div class ="w-100"></div>'
    context = INDEX_HEAD + body + INDEX_FOOT
    return '200 OK', context


urls = {'/': index_view}
middlewares = []

application = Application(urls, middlewares)

# uwsgi --http :8000 --wsgi-file view.py
