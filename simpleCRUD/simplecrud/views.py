import logging
import transaction

from pyramid.view import view_config
from pyramid.url import route_path
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from formencode import Schema, validators
from sqlalchemy.exc import IntegrityError

from .models import DBSession, Book

log = logging.getLogger(__name__)


class BookSchema(Schema):

    filter_extra_fields = True
    allow_extra_fields = True

    name = validators.String(min=2, max=64, not_empty=True)
    author = validators.String(max=32)
    desc = validators.String()
    ISBN = validators.String(max=20)
    price = validators.Number(max=1000)


@view_config(route_name='home', renderer='simplecrud:templates/book/book_list.pt')
@view_config(route_name='book_list', renderer='simplecrud:templates/book/book_list.pt')
def book_list(request):
    books = DBSession.query(Book).all()
    return dict(books = books)


@view_config(route_name='book_detail', renderer='simplecrud:templates/book/book_detail.pt')
def book_detail(request):
    book = None
    try:
        book_id = int(request.matchdict['id'])
        if book_id:
            book = DBSession.query(Book).filter(Book.id==book_id).first()
    except ValueError:
        log.warning("invalidate id %s input." % request.matchdict['id'])
    except Exception:
        log.error("database error!")

    if not book:
        return HTTPForbidden()

    return dict(book=book)


@view_config(route_name='book_add', renderer='simplecrud:templates/book/book_add.pt')
def book_add(request):
    form = Form(request, schema=BookSchema)
    if form.validate():

        book = Book(form.data.get("name"),
                    form.data.get("author"),
                    form.data.get("desc"),
                    form.data.get("ISBN"),
                    form.data.get("price"))

        try:
            DBSession.add(book)
            DBSession.flush()
            transaction.commit()

            return HTTPFound(location=route_path("book_list", request))
        except IntegrityError:
            transaction.abort()
            form.errors["global_error"] = 'database insert error, maybe book name conflict.'
        except Exception, e:
            transaction.abort()
            form.errors["global_error"] = 'database error.' + str(e)
            log.error("database error!")

    return dict(renderer=FormRenderer(form))


@view_config(route_name='book_edit', renderer='simplecrud:templates/book/book_edit.pt')
def book_edit(request):
    book_id = 0
    try:
        book_id = int(request.matchdict['id'])
    except Exception:
        pass

    if not book_id:
        return HTTPForbidden()

    form = Form(request, schema=BookSchema)
    if form.validate():
        try:
            DBSession.query(Book).filter(Book.id==book_id).update({Book.name:form.data.get("name"),
                                                                   Book.author:form.data.get("author"),
                                                                   Book.desc:form.data.get("desc"),
                                                                   Book.ISBN:form.data.get("ISBN"),
                                                                   Book.price:form.data.get("price")})
            return HTTPFound(location=route_path("book_list", request))
        except IntegrityError:
            transaction.abort()
            form.errors["global_error"] = 'database update error, maybe book name conflict.'
        except Exception:
            transaction.abort()
            form.errors["global_error"] = 'database error.'
            log.error("database error!")
    else:
        book = None
        try:
            book = DBSession.query(Book).filter(Book.id==book_id).first()
        except Exception:
            pass

        if not book:
            return HTTPForbidden()

        form = Form(request, schema=BookSchema, obj = book)

    return dict(renderer=FormRenderer(form))

@view_config(route_name='book_delete')
def book_delete(request):
    try:
        book_id = int(request.matchdict['id'])
        if book_id:
            DBSession.query(Book).filter(Book.id==book_id).delete()
        return HTTPFound(location=route_path("book_list", request))
    except Exception:
        return HTTPForbidden()
