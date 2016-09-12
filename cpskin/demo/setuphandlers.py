# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.dx.behaviors import IEventBasic
from plone.app.event.interfaces import IEventSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import datetime
import os


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
    news_folder = api.content.get('/actualites')
    news = [{
        'title': 'Nouvelle brasserie',
        'desc': 'Une nouvelle brasserie va ouvrir ses portes près de chez vous',
        'text': 'Bonjour, <br /><br />Une nouvelle brasserie va ouvrir ses portes près de chez vous',
        'img': 'brasserie.jpg',
        'alaune': True,
    }, {
        'title': 'Météo',
        'desc': 'Attention à la météo de ces prochains jours',
        'text': 'Bonjour, <br /><br />Faites attention à la météo de ces prochains jours',
        'img': 'meteo.jpg'
    },
    ]
    for actualite in news:
        actu = api.content.create(
            container=news_folder,
            type='News Item',
            title=actualite['title']
        )
        actu.title = actualite['title']
        add_news_image_from_file(actu, actualite['img'])
        if actualite.get('alaune'):
            add_alaune(actu)
        api.content.transition(obj=actu, transition='publish_and_hide')
        actu.reindexObject()


def add_alaune(obj):
    obj.hiddenTags = set([u'a-la-une', ])
    pass


def add_tag(obj, tag={u'id': u'value'}):
    # XXX get older value before adding one new
    # value = set([tag['value'], ])
    # setattr(obj, tag['id'], value)
    pass


def add_folders(portal):
    folders = [{
        'ma-commune': {
            u'Vie politique':
                [u'Collège communal', u'Conseil communal'],
            u'Services communaux':
                [ u'Population-Etat civil', u'Informatique', u'Heures d\'ouverture']
        },
        'loisirs': {
            u'Sports':
                [u'Piscine communale', u'Annuaire des clubs sportifs'],
            u'Folklores':
                [u'Carnaval', u'Marché de Noël'],
            u'Tourisme':
                [u'Barrage']
        },
        'economie': {
            u'L\'entreprenariat':
                [u'CSAM', u'EId'],
            u'Zonings':
                [u'Industriels', u'Port'],
        },
        'je-suis': [u'Jeune', u'Entrepreneur'],
        'je-trouve': [u'Démarches administratives', u'Taxes'],
    }]
    for f in folders:
        for f_id in f.keys():
            folder_first_level = portal.get(f_id)
            folder_dict = f[f_id]
            if isinstance(folder_dict, dict):
                for f_second_level_title in folder_dict.keys():
                    f_second_level = api.content.create(
                        container=folder_first_level,
                        type='Folder',
                        title=f_second_level_title)
                    f_second_level.setTitle(f_second_level_title)
                    f_second_level.reindexObject()
                    api.content.transition(
                        obj=f_second_level,
                        transition='publish_and_show')

                    for f_third_level_title in folder_dict[f_second_level_title]:
                        f_third_level = api.content.create(
                            container=f_second_level,
                            type='Folder',
                            title=f_third_level_title)
                        f_third_level.setTitle(f_third_level_title)
                        f_third_level.reindexObject()
                        api.content.transition(
                            obj=f_third_level,
                            transition='publish_and_show')
            if isinstance(folder_dict, list):
                for f_third_level_title in folder_dict:
                        f_third_level = api.content.create(
                            container=folder_first_level,
                            type='Folder',
                            title=f_third_level_title)
                        f_third_level.setTitle(f_third_level_title)
                        f_third_level.reindexObject()
                        api.content.transition(
                            obj=f_third_level,
                            transition='publish_and_show')


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
