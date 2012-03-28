

from .models import (
    DBSession,
    MyCat,
    MyFile,
    )

def view_root(context, request):
    print request.resource_url(context)
    return {'context':context, 'items':list(context), 'project':'MyTest'}

def view_cat(context, request):
    print request.resource_url(context)
    return {'context':context, 'items':context.listall(), 'project':'MyTest'}

def view_file(context, request):
    print request.resource_url(context)
    return {'item':context, 'project':'MyTest'}

def view_photo(context, request):
    return {'item':context, 'project':'MyTest'}