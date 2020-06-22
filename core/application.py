class Application:
    def __init__(self, urls, middlewares):
        self.urls = urls
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        request = []

        for middleware in self.middlewares:
            middleware(request)

        if path in self.urls:
            view = self.urls[path]
            code, text = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode(encoding='utf-8')]
        else:
            start_response('404 Not found', [('Content-Type', 'text/plain')])
            return [b'Not Found']
