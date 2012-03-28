# -*- coding: UTF-8 -*-

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    MyCat,
    MyFile,
    Base,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

#直接在数据库中构建如下初始数据以供演示。
#MySite ---- MyPhoto ---- SportPhoto ---- ski.jpg
#         |            |
#         |            -- PrivatePhoto ---- love.jpg
#         |
#         -- MyNote ---- 20120327.txt
#         |
#         -- MyMP3 ---- paradise.mp3
#         |
#         -- MyVideo ---- hot.avi
def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        my_photo_cat = MyCat(name='MyPhoto', pid=0, desc="photos taken by myself")
        DBSession.add(my_photo_cat)
        my_note_cat = MyCat(name='MyNote', pid=0, desc="take a note a day to save life")
        DBSession.add(my_note_cat)
        my_mp3_cat = MyCat(name='MyMP3', pid=0, desc="my favorite mp3")
        DBSession.add(my_mp3_cat)
        my_video_cat = MyCat(name='MyVideo', pid=0, desc="all my hot videos")
        DBSession.add(my_video_cat)
        DBSession.flush()
        
        my_sport_photo_cat = MyCat(name='SportPhoto', pid=my_photo_cat.id, desc="photos of sports")
        DBSession.add(my_sport_photo_cat)
        my_private_photo_cat = MyCat(name='PrivatePhoto', pid=my_photo_cat.id, desc="secret photos")
        DBSession.add(my_private_photo_cat)
        DBSession.flush()
        
        afile = MyFile(name='ski.jpg', cat=my_sport_photo_cat.id, save_path="", desc="20111112 by canon")
        DBSession.add(afile)
        afile = MyFile(name='love.jpg', cat=my_private_photo_cat.id, save_path="", desc="20111111 by canon")
        DBSession.add(afile)
        afile = MyFile(name='20120327.txt', cat=my_note_cat.id, save_path="", desc="diary 20120327")
        DBSession.add(afile)
        afile = MyFile(name='paradise.mp3', cat=my_mp3_cat.id, save_path="", desc="mp3 download")
        DBSession.add(afile)
        afile = MyFile(name='hot.avi', cat=my_video_cat.id, save_path="", desc="hot video from some place")
        DBSession.add(afile)
