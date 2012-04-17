import logging
import unittest
import transaction

from pyramid import testing

from .models import DBSession

log = logging.getLogger(__name__)

def _registerRoutes(config):
    config.add_route('book_list', '/book/list')
    config.add_route('book_detail', '/book/detail/{id}')
    config.add_route('book_add', '/book/add')
    config.add_route('book_edit', '/book/edit/{id}')
    config.add_route('book_delete', '/book/delete/{id}')


class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Book,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            book = Book(name='Python', author='chen', desc='desc', ISBN='978-7-121-06874-4', price=69.80)
            DBSession.add(book)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_book_list(self):
        from .views import book_list
        request = testing.DummyRequest()
        info = book_list(request)
        self.assertEqual(len(info['books']), 1)
        self.assertEqual(info['books'][0].name, 'Python')

    def test_book_detail(self):
        from .views import book_detail
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = book_detail(request)
        self.assertEqual(info['book'].name, 'Python')

    def test_book_detail_unauthorized(self):
        from pyramid.httpexceptions import HTTPForbidden
        from .views import book_detail
        request = testing.DummyRequest()
        request.matchdict['id'] = 555
        info = book_detail(request)
        self.assertIsInstance(info, HTTPForbidden)

    def test_book_add_form(self):
        from pyramid_simpleform.renderers import FormRenderer
        from .views import book_add
        request = testing.DummyRequest()
        info = book_add(request)
        self.assertIsInstance(info['renderer'], FormRenderer)

    def test_book_add_save(self):
        from pyramid.httpexceptions import HTTPFound
        from .views import book_add
        from .models import Book

        _registerRoutes(self.config)

        request = testing.DummyRequest({'name':'a new book',
                                        'author':'a new author',
                                        'ISBN':'a new ISBN',
                                        'desc':'a new desc',
                                        'price':'6.0',
                                        'submit':'save'})
        request.method = 'POST'
        info = book_add(request)
        self.assertIsInstance(info, HTTPFound)

        added = DBSession.query(Book).filter(Book.id==2).first()

        self.assertEqual(added.name, 'a new book')
        self.assertEqual(added.author, 'a new author')

    def test_book_add_conflict(self):
        from pyramid_simpleform.renderers import FormRenderer
        from .views import book_add
        from .models import Book

        _registerRoutes(self.config)

        request = testing.DummyRequest({'name':'Python',
                                        'author':'a new author',
                                        'ISBN':'a new ISBN',
                                        'desc':'a new desc',
                                        'price':'6.0',
                                        'submit':'save'})
        request.method = 'POST'
        info = book_add(request)
        self.assertIsInstance(info['renderer'], FormRenderer)

        added = DBSession.query(Book).filter(Book.id==1).first()

        self.assertEqual(added.name, 'Python')
        self.assertEqual(added.author, 'chen')
        self.assertEqual(added.ISBN, '978-7-121-06874-4')

    def test_book_edit_form(self):
        from pyramid_simpleform.renderers import FormRenderer
        from .views import book_edit
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = book_edit(request)
        self.assertIsInstance(info['renderer'], FormRenderer)
        self.assertEqual(info['renderer'].form.data['name'], 'Python')

    def test_book_edit_save(self):
        from pyramid.httpexceptions import HTTPFound
        from .views import book_edit
        from .models import Book

        _registerRoutes(self.config)

        request = testing.DummyRequest({'name':'a new book',
                                        'author':'a new author',
                                        'ISBN':'a new ISBN',
                                        'desc':'a new desc',
                                        'price':'6.0',
                                        'submit':'save'})
        request.method = 'POST'
        request.matchdict['id'] = 1
        info = book_edit(request)
        self.assertIsInstance(info, HTTPFound)

        added = DBSession.query(Book).filter(Book.id==1).first()

        self.assertEqual(added.name, 'a new book')
        self.assertEqual(added.author, 'a new author')

    def test_book_edit_conflict(self):
        from pyramid_simpleform.renderers import FormRenderer
        from .views import book_edit
        from .models import Book

        _registerRoutes(self.config)

        new_book  = Book(name='a new book',
                         author='a new author',
                         ISBN='a new ISBN',
                         desc='a new desc',
                         price='6.0')
        DBSession.add(new_book)
        DBSession.flush()
        transaction.commit()

        request = testing.DummyRequest({'name':'Python',
                                        'author':'a new author',
                                        'ISBN':'a new ISBN',
                                        'desc':'a new desc',
                                        'price':'6.0',
                                        'submit':'save'})
        request.method = 'POST'
        request.matchdict['id'] = 2
        info = book_edit(request)
        self.assertIsInstance(info['renderer'], FormRenderer)

        old = DBSession.query(Book).filter(Book.id==2).first()

        self.assertEqual(old.name, 'a new book')
        self.assertEqual(old.author, 'a new author')
        self.assertEqual(old.ISBN, 'a new ISBN')

    def test_book_delete(self):
        from pyramid.httpexceptions import HTTPFound
        from .views import book_delete
        from .models import Book

        _registerRoutes(self.config)

        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = book_delete(request)
        self.assertIsInstance(info, HTTPFound)

        nullobj = DBSession.query(Book).filter(Book.id==1).first()
        self.assertEqual(nullobj, None)

    def test_book_delete_unauthorized(self):
        from pyramid.httpexceptions import HTTPForbidden
        from .views import book_delete
        request = testing.DummyRequest()
        request.matchdict['id'] = 555
        info = book_delete(request)
        self.assertIsInstance(info, HTTPForbidden)
