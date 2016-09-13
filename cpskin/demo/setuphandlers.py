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


def exists(portal, parent, id='', title='', type=''):
    pc = portal.portal_catalog
    params = {'path': {'query': '/'.join(parent.getPhysicalPath()), 'depth': 1}}
    if id:
        params['id'] = id
    if title:
        params['Title'] = title
    if type:
        params['portal_type'] = type
    brains = pc(**params)
    if brains:
        return brains[0].getObject()
    return None


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

    def create_folders(portal, folders, transition='publish_and_show'):
        for dic1 in folders:
            for f1_id in dic1:
                f1 = portal.get(f1_id)
                dic2 = dic1[f1_id]
                if isinstance(dic2, dict):
                    for f2_tit in dic2:
                        f2 = exists(portal, f1, title=f2_tit)
                        if not f2:
                            f2 = api.content.create(container=f1, type='Folder', title=f2_tit)
                            api.content.transition(obj=f2, transition=transition)

                        for f3_tit in dic2[f2_tit]:
                            f3 = exists(portal, f2, title=f3_tit)
                            if not f3:
                                f3 = api.content.create(container=f2, type='Folder', title=f3_tit)
                                api.content.transition(obj=f3, transition=transition)
                if isinstance(dic2, list):
                    for f2_tit in dic2:
                        f2 = exists(portal, f1, title=f2_tit)
                        if not f2:
                            f2 = api.content.create(container=f1, type='Folder', title=f2_tit)
                            api.content.transition(obj=f2, transition=transition)

    folders_to_show = [
        {'ma-commune': {
            u'Vie politique': [u'Collège communal', u'Conseil communal'],
            u'Services communaux': [u'Population-Etat civil', u'Informatique']
        }},
        {'loisirs': {
            u'Sports': [u'Piscine communale', u'Annuaire des clubs sportifs'],
            u'Folklores': [u'Carnaval', u'Marché de Noël'],
            u'Tourisme': [u'Barrage']
        }},
        {'economie': {
            u"L'entreprenariat": [u'CSAM', u'EId'],
            u'Zonings': [u'Industriels', u'Port'],
        }},
        {'je-suis': [u'Jeune', u'Entrepreneur']},
        {'je-trouve': [u'Démarches administratives', u'Taxes']},
    ]
    create_folders(portal, folders_to_show)

    folders_to_hide = [
        {'ma-commune': {
            u'Services communaux': [u"Heures d'ouverture"]
        }},
    ]
    create_folders(portal, folders_to_hide, transition='publish_and_hide')


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
