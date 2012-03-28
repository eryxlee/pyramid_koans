from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession, 
    root_factory,
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)


    config.add_view('traverseonrdb.views.view_root', 
                    context='traverseonrdb.models.MyRoot', 
                    renderer="templates/root.pt")
    config.add_view('traverseonrdb.views.view_cat', 
                    context='traverseonrdb.models.MyCat', 
                    renderer="templates/cat.pt")

    config.add_view('traverseonrdb.views.view_photo',
                    name="photoview",
                    context='traverseonrdb.models.MyFile',
                    renderer="templates/photo.pt")    
    
    config.add_view('traverseonrdb.views.view_file',
                    context='traverseonrdb.models.MyFile',
                    renderer="templates/file.pt")

    return config.make_wsgi_app()

