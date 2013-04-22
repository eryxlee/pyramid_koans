import os
import datetime
import transaction

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import engine_from_config

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Unicode,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode(255), default=u'')
    post_date = Column(DateTime, default=datetime.datetime.now)
    finished = Column(Integer, default=0)

    def __init__(self, title, post_date, finished):
        self.title = title
        self.post_date = post_date
        self.finished = finished


@view_config(route_name='index',  renderer='/index.mako')
def index_view(request):
    todos = DBSession.query(Todo).order_by(Todo.post_date.desc()).all()
    return {'todos': todos}


@view_config(route_name='add', request_method='POST')
def add_post_view(request):
    title = request.params.get('title', '')
    with transaction.manager:
        todo = Todo(title=title, post_date=datetime.datetime.now(), finished=0)
        DBSession.add(todo)

    raise HTTPFound(location = request.route_url('index'))


@view_config(route_name='edit', request_method='GET', renderer='/edit.mako')
def edit_view(request):
    id = int(request.matchdict.get('id'))
    todo = DBSession.query(Todo).filter(Todo.id==id).first()

    return {'todo': todo}


@view_config(route_name='edit', request_method='POST')
def edit_post_view(request):
    id = int(request.matchdict.get('id'))
    title = request.params.get('title')
    with transaction.manager:
        DBSession.query(Todo).filter(Todo.id==id).update({Todo.title:title})

    raise HTTPFound(location = request.route_url('index'))


@view_config(route_name='finish')
def finish_view(request):
    id = int(request.matchdict.get('id'))
    status = request.params.get('status', 'yes')
    finished = {'yes':1, 'no':0}.get(status)
    if finished != None:
        with transaction.manager:
            DBSession.query(Todo).filter(Todo.id==id).update({Todo.finished:finished})

    raise HTTPFound(location = request.route_url('index'))


@view_config(route_name='delete')
def delete_view(request):
    id = int(request.matchdict.get('id'))
    with transaction.manager:
        DBSession.query(Todo).filter(Todo.id==id).delete()

    raise HTTPFound(location = request.route_url('index'))


def my_static_path(self, path, **kw):
    if not os.path.isabs(path):
        if not ':' in path:
            path = '%s:%s/%s' % ("simpletodo", 'static', path)
    kw['_app_url'] = self.script_name

    return self.static_url(path, **kw)


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_request_method(my_static_path, 'static_path')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('add', '/todo/new')
    config.add_route('edit', '/todo/{id:\d+}/edit')
    config.add_route('finish', '/todo/{id:\d+}/finish')
    config.add_route('delete', '/todo/{id:\d+}/delete')
    config.scan()

    return config.make_wsgi_app()
