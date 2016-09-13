# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.dx.behaviors import IEventBasic
from plone.app.event.interfaces import IEventSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import datetime
import os

from imio.helpers.content import create, richtextval, lead_image


def post_install(context):
    """Post install script."""
    if context.readDataFile('cpskindemo_default.txt') is None:
        return

    portal = context.getSite()
    # frontpage = api.content.get('/front-page')
    # frontpage.processForm()
    # Edit frontpage to have explain text on how use demo site
    add_events(portal)
    add_news(portal)
    add_folders(portal)
    add_album(portal)
    add_users(portal)


def add_events(portal):
    """Add some demo events."""
    timezone = 'Europe/Brussels'
    reg = getUtility(IRegistry)
    settings = reg.forInterface(IEventSettings, prefix="plone.app.event")
    if not settings.portal_timezone:
        settings.portal_timezone = timezone
    event_folder = api.content.get('/evenements')
    now = datetime.datetime.now()
    tomorrow = datetime.datetime(now.year, now.month, now.day + 1)
    today18 = datetime.datetime(now.year, now.month, now.day, 18)
    today21 = datetime.datetime(now.year, now.month, now.day, 21)
    today23 = datetime.datetime(now.year, now.month, now.day, 23)
    # tomorrow18 = today18 + datetime.timedelta(days=1)
    tomorrow21 = today21 + datetime.timedelta(days=1)
    tomorrow23 = today23 + datetime.timedelta(days=1)
    next_week = tomorrow + datetime.timedelta(weeks=1)
    events = [{
        'title': 'Atelier photo',
        'desc': 'Participer à un atelier photo',
        'start': today18,
        'end': today21,
        'img': 'atelierphoto.jpg',
        'alaune': True,
    }, {
        'title': 'Concert',
        'desc': 'Participer à notre concert caritatif',
        'start': tomorrow21,
        'end': tomorrow23,
        'img': 'concert.jpg'
    }, {
        'title': 'Marché aux fleurs',
        'desc': 'Vener découvrir notre marché aux fleurs',
        'start': tomorrow,
        'end': next_week,
        'img': 'marcheauxfleurs.jpg'
    }
    ]
    for e in events:
        event = api.content.create(
            container=event_folder,
            type='Event',
            title=e['title']
        )
        event.title = e['title']
        event.description = e['desc']
        event.timezone = timezone
        behavior = IEventBasic(event)
        behavior.start = e['start']
        behavior.end = e['end']
        add_leadimage_from_file(event, e['img'])
        if e.get('alaune'):
            add_alaune(event)
        api.content.transition(obj=event, transition='publish_and_hide')
        event.reindexObject()


def add_news(portal):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    news = [
        {
            'cont': '/actualites', 'type': 'News Item',
            'title': 'Nouvelle brasserie',
            'attrs': {'description': 'Une nouvelle brasserie va ouvrir ses portes près de chez vous',
                      'text': richtextval('Bonjour, <br /><br />Une nouvelle brasserie va ouvrir ses portes près de '
                                          'chez vous'),
                      'hiddenTags': set([u'a-la-une', ])},
            'functions': [lead_image],
            'extra': {'lead_image': {'filepath': os.path.join(data_path, 'brasserie.jpg')}},
            'trans': ['publish_and_hide'],
        },
        {
            'cont': '/actualites', 'type': 'News Item',
            'title': 'Météo',
            'attrs': {'description': 'Attention à la météo de ces prochains jours',
                      'text': richtextval('Bonjour, <br /><br />Faites attention à la météo de ces prochains jours'),},
            'functions': [lead_image],
            'extra': {'lead_image': {'filepath': os.path.join(data_path, 'meteo.jpg')}},
            'trans': ['publish_and_hide'],
        },
    ]
    create(news)


def add_alaune(obj):
    obj.hiddenTags = set([u'a-la-une', ])
    pass


def add_tag(obj, tag={u'id': u'value'}):
    # XXX get older value before adding one new
    # value = set([tag['value'], ])
    # setattr(obj, tag['id'], value)
    pass


def add_folders(portal):

    folders = [
        {
            'cid': 100, 'cont': '/ma-commune', 'type': 'Folder',
            'title': u'Vie politique',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 110, 'cont': 100, 'type': 'Folder',
            'title': u'Collège communal',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 111, 'cont': 100, 'type': 'Folder',
            'title': u'Conseil communal',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 200, 'cont': '/ma-commune', 'type': 'Folder',
            'title': u'Services communaux',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 210, 'cont': 200, 'type': 'Folder',
            'title': u'Population-Etat civil',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 220, 'cont': 200, 'type': 'Folder',
            'title': u'Informatique',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 230, 'cont': 200, 'type': 'Folder',
            'title': u"Heures d'ouverture",
            'trans': ['publish_and_hide'],
        },
        {
            'cid': 240, 'cont': 200, 'typ': 'Folder',
            'title': u'Autres services',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 250, 'cont': 240, 'typ': 'Folder',
            'title': u'CPAS',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 260, 'cont': 250, 'typ': 'Folder',
            'title': u'Album photos',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 300, 'cont': '/loisirs', 'typ': 'Folder',
            'title': u'Sports',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 310, 'cont': 300, 'type': 'Folder',
            'title': u'Piscine communale',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 320, 'cont': 300, 'type': 'Folder',
            'title': u'Annuaire des clubs sportifs',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 400, 'cont': '/loisirs', 'type': 'Folder',
            'title': u'Folklores',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 410, 'cont': 400, 'type': 'Folder',
            'title': u'Carnaval',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 420, 'cont': 400, 'type': 'Folder',
            'title': u'Marché de Noël',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 500, 'cont': '/loisirs', 'type': 'Folder',
            'title': u'Tourisme',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 510, 'cont': 500, 'type': 'Folder',
            'title': u'Barrage',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 600, 'cont': '/economie', 'type': 'Folder',
            'title': u"L'entreprenariat",
            'trans': ['publish_and_show'],
        },
        {
            'cid': 610, 'cont': 600, 'type': 'Folder',
            'title': u'CSAM',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 620, 'cont': 600, 'type': 'Folder',
            'title': u'EId',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 700, 'cont': '/economie', 'type': 'Folder',
            'title': u'Zonings',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 710, 'cont': 700, 'type': 'Folder',
            'title': u'Industriels',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 720, 'cont': 700, 'type': 'Folder',
            'title': u'Port',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 800, 'cont': '/je-suis', 'type': 'Folder',
            'title': u'Jeune',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 810, 'cont': '/je-suis', 'type': 'Folder',
            'title': u'Entrepreneur',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 820, 'cont': '/je-suis', 'typ': 'Folder',
            'title': u'Nouvel habitant',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 900, 'cont': '/je-trouve', 'typ': 'Folder',
            'title': u'Démarches administratives',
            'trans': ['publish_and_show'],
        },
        {
            'cid': 910, 'cont': '/je-trouve', 'type': 'Folder',
            'title': u'Taxes',
            'trans': ['publish_and_show'],
        },
    ]

    create(folders)


def add_leadimage_from_file(obj, file_name):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    file_path = os.path.join(data_path, file_name)
    if not obj.hasObject(file_name):
        from plone.namedfile.file import NamedBlobImage
        namedblobimage = NamedBlobImage(
            data=open(file_path, 'r').read(),
            filename=unicode(file_name)
        )
        image = api.content.create(type='Image',
                                   title=file_name,
                                   image=namedblobimage,
                                   container=api.portal.get(),
                                   language='fr')
        image.setTitle(file_name)
        image.reindexObject()
        setattr(obj, 'image', namedblobimage)


def add_news_image_from_file(obj, file_name):
    if not obj.hasObject(file_name):
        # with deterity image
        add_leadimage_from_file(obj, file_name)


def add_image_from_file(container, file_name):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    filePath = os.path.join(data_path, file_name)
    if not container.hasObject(file_name):
        # with deterity image
        from plone.namedfile.file import NamedBlobImage
        namedblobimage = NamedBlobImage(
            data=open(filePath, 'r').read(),
            filename=unicode(file_name)
        )
        image = api.content.create(type='Image',
                                   title=file_name,
                                   image=namedblobimage,
                                   container=container,
                                   language='fr')
        image.setTitle(file_name)
        image.reindexObject()


def add_album(portal):
    folder = api.content.create(
        container=portal,
        type='Folder',
        id='album')
    folder.setTitle("Album")
    folder.reindexObject()
    add_image_from_file(folder, 'moto.jpg')
    add_image_from_file(folder, 'meteo.jpg')
    api.content.transition(obj=folder, transition='publish_and_hide')
    folder.setLayout('galleryview')


def add_users(portal):
    pass
