from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('book_list', '/book/list')
    config.add_route('book_detail', '/book/detail/{id}')
    config.add_route('book_add', '/book/add')
    config.add_route('book_edit', '/book/edit/{id}')
    config.add_route('book_delete', '/book/delete/{id}')

    config.scan()
    return config.make_wsgi_app()

