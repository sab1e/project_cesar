from core.application import Application


def index_view(request):
    return '200 OK', 'Index Page'


urls = {'/': index_view}
middlewares = []

application = Application(urls, middlewares)
