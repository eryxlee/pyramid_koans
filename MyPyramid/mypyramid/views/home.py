# -*- coding: UTF-8 -*-

from pyramid.response import Response
from pyramid.view import view_config


from sqlalchemy.exc import DBAPIError

from mypyramid.models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='home', renderer='mypyramid:templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'MyPyramid'}


@view_config(route_name='pyramid_locale', renderer='mypyramid:templates/pyramid_locale.pt')
def locale(request):
    from pyramid.i18n import TranslationString as _

    ts = _('add-number', default='Add ${number}', mapping={'number':1}, domain='MyPyramid')
    ts2 = _('add-number2', default='Add2 ${number}', mapping={'number':1}, domain='MyPyramid')
    print ts
    return {'locale_str': ts}

##    from pyramid.i18n import TranslationString as _
##    locale_str = _(u'a new string')

@view_config(route_name='pyramid_locale_mako', renderer='mypyramid:templates/pyramid_locale_mako.mako')
def mako_locale(request):

    _ = request.translate

    ts = _('add-number', mapping={'number':1}, domain='MyPyramid')
    ts2 = _('add-number2')
    print ts
    return {'locale_str': ts}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MyPyramid_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

