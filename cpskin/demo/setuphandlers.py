# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.interfaces import IEventSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import datetime
import os

from imio.helpers.content import create, richtextval, add_image

data_path = os.path.join(os.path.dirname(__file__), "data")


def get_path(filename):
    return os.path.join(data_path, filename)


def post_install(context):
    """Post install script."""
    if context.readDataFile("cpskindemo_default.txt") is None:
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
    add_document(portal)
    # add_directory(portal)


def add_events(portal):
    """Add some demo events."""
    timezone = "Europe/Brussels"
    reg = getUtility(IRegistry)
    settings = reg.forInterface(IEventSettings, prefix="plone.app.event")
    if not settings.portal_timezone:
        settings.portal_timezone = timezone
    now = datetime.datetime.now()
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    events = [
        {
            "cont": "/evenements",
            "type": "Event",
            "title": "Atelier photo",
            "attrs": {
                "description": "Participer à un atelier photo",
                "start": datetime.datetime(now.year, now.month, now.day, 18),
                "end": datetime.datetime(now.year, now.month, now.day, 21),
                "timezone": timezone,
                "hiddenTags": set([u"a-la-une",]),
            },
            "functions": [(add_image, [], {"filepath": get_path("atelierphoto.jpg")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cont": "/evenements",
            "type": "Event",
            "title": "Concert",
            "attrs": {
                "description": "Participer à notre concert caritatif",
                "start": datetime.datetime(
                    tomorrow.year, tomorrow.month, tomorrow.day, 21
                ),
                "end": datetime.datetime(
                    tomorrow.year, tomorrow.month, tomorrow.day, 23
                ),
                "timezone": timezone,
            },
            "functions": [(add_image, [], {"filepath": get_path("concert.jpg")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cont": "/evenements",
            "type": "Event",
            "title": "Marché aux fleurs",
            "attrs": {
                "description": "Vener découvrir notre marché aux fleurs",
                "start": tomorrow,
                "end": tomorrow + datetime.timedelta(weeks=1),
                "timezone": timezone,
            },
            "functions": [
                (add_image, [], {"filepath": get_path("marcheauxfleurs.jpg")})
            ],
            "trans": ["publish_and_hide"],
        },
        {
            "cont": "/evenements",
            "type": "Event",
            "title": "Carnaval",
            "attrs": {
                "description": "Venez fêter le carnaval",
                "start": datetime.datetime(
                    tomorrow.year, tomorrow.month, tomorrow.day, 15
                ),
                "end": datetime.datetime(
                    tomorrow.year, tomorrow.month, tomorrow.day, 18
                ),
                "timezone": timezone,
            },
            "functions": [(add_image, [], {"filepath": get_path("sorciere.jpg")})],
            "trans": ["publish_and_hide"],
        },
    ]
    create(events)


def add_news(portal):
    news = [
        {
            "cont": "/actualites",
            "type": "News Item",
            "title": "Nouvelle brasserie",
            "attrs": {
                "description": "Une nouvelle brasserie va ouvrir ses portes près de chez vous",
                "text": richtextval(
                    "Bonjour, <br /><br />Une nouvelle brasserie va ouvrir ses portes près de "
                    "chez vous"
                ),
                "hiddenTags": set([u"a-la-une",]),
            },
            "functions": [(add_image, [], {"filepath": get_path("brasserie.jpg")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cont": "/actualites",
            "type": "News Item",
            "title": "Météo",
            "attrs": {
                "description": "Attention à la météo de ces prochains jours",
                "text": richtextval(
                    "Bonjour, <br /><br />Faites attention à la météo de ces prochains jours"
                ),
            },
            "functions": [(add_image, [], {"filepath": get_path("meteo.jpg")})],
            "trans": ["publish_and_hide"],
        },
    ]
    create(news)


def add_document(portal):
    document = [
        {
            "cont": "/",
            "type": "Document",
            "title": "Mot clés",
            "attrs": {
                "iamTags": set([u"jeune", u"entrepreneur", u"nouvel habitant"]),
                "isearchTags": set([u"démarches administrative"]),
            },
        },
        {
            "cont": 110,
            "type": "Document",
            "title": "Le collège communal",
            "attrs": {"description": "Présentation collège communal",},
            "trans": ["publish_and_show"],
        },
    ]
    create(document, globl=True)


def add_folders(portal):

    folders = [
        {
            "cid": 100,
            "cont": "/ma-commune",
            "type": "Folder",
            "title": u"Vie politique",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 110,
            "cont": 100,
            "type": "Folder",
            "title": u"Collège communal",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 111,
            "cont": 100,
            "type": "Folder",
            "title": u"Conseil communal",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 200,
            "cont": "/ma-commune",
            "type": "Folder",
            "title": u"Services communaux",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 210,
            "cont": 200,
            "type": "Folder",
            "title": u"Population-Etat civil",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 220,
            "cont": 200,
            "type": "Folder",
            "title": u"Informatique",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 230,
            "cont": 200,
            "type": "Folder",
            "title": u"Heures d'ouverture",
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 240,
            "cont": 200,
            "type": "Folder",
            "title": u"Autres services",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 250,
            "cont": 240,
            "type": "Folder",
            "title": u"CPAS",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 260,
            "cont": 250,
            "type": "Folder",
            "title": u"Album photos",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 300,
            "cont": "/loisirs",
            "type": "Folder",
            "title": u"Sports",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 310,
            "cont": 300,
            "type": "Folder",
            "title": u"Piscine communale",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 320,
            "cont": 300,
            "type": "Folder",
            "title": u"Annuaire des clubs sportifs",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 400,
            "cont": "/loisirs",
            "type": "Folder",
            "title": u"Folklores",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 410,
            "cont": 400,
            "type": "Folder",
            "title": u"Carnaval",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 415,
            "cont": 400,
            "type": "Folder",
            "title": u"Images folklores",
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 420,
            "cont": 400,
            "type": "Folder",
            "title": u"Marché de Noël",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 500,
            "cont": "/loisirs",
            "type": "Folder",
            "title": u"Tourisme",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 510,
            "cont": 500,
            "type": "Folder",
            "title": u"Barrage",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 600,
            "cont": "/economie",
            "type": "Folder",
            "title": u"L'entreprenariat",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 610,
            "cont": 600,
            "type": "Folder",
            "title": u"CSAM",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 620,
            "cont": 600,
            "type": "Folder",
            "title": u"EId",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 700,
            "cont": "/economie",
            "type": "Folder",
            "title": u"Zonings",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 710,
            "cont": 700,
            "type": "Folder",
            "title": u"Industriels",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 720,
            "cont": 700,
            "type": "Folder",
            "title": u"Port",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 800,
            "cont": "/je-suis",
            "type": "Folder",
            "title": u"Jeune",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 810,
            "cont": "/je-suis",
            "type": "Folder",
            "title": u"Entrepreneur",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 820,
            "cont": "/je-suis",
            "type": "Folder",
            "title": u"Nouvel habitant",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 900,
            "cont": "/je-trouve",
            "type": "Folder",
            "title": u"Démarches administratives",
            "trans": ["publish_and_show"],
        },
        {
            "cid": 910,
            "cont": "/je-trouve",
            "type": "Folder",
            "title": u"Taxes",
            "trans": ["publish_and_show"],
        },
    ]

    create(folders, globl=True)


def add_leadimage_from_file(obj, file_name):
    data_path = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(data_path, file_name)
    if not obj.hasObject(file_name):
        from plone.namedfile.file import NamedBlobImage

        namedblobimage = NamedBlobImage(
            data=open(file_path, "r").read(), filename=unicode(file_name)
        )
        image = api.content.create(
            type="Image",
            title=file_name,
            image=namedblobimage,
            container=api.portal.get(),
            language="fr",
        )
        image.setTitle(file_name)
        image.reindexObject()
        setattr(obj, "image", namedblobimage)


def add_news_image_from_file(obj, file_name):
    if not obj.hasObject(file_name):
        # with deterity image
        add_leadimage_from_file(obj, file_name)


def add_image_from_file(container, file_name):
    data_path = os.path.join(os.path.dirname(__file__), "data")
    filePath = os.path.join(data_path, file_name)
    if not container.hasObject(file_name):
        # with deterity image
        from plone.namedfile.file import NamedBlobImage

        namedblobimage = NamedBlobImage(
            data=open(filePath, "r").read(), filename=unicode(file_name)
        )
        image = api.content.create(
            type="Image",
            title=file_name,
            image=namedblobimage,
            container=container,
            language="fr",
        )
        image.setTitle(file_name)
        image.reindexObject()


def add_album(portal):
    objects = [
        {
            "cid": 10,
            "cont": "/",
            "type": "Folder",
            "title": "Album",
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 15,
            "cont": 10,
            "type": "Image",
            "title": "Moto",
            "functions": [(add_image, [], {"filepath": get_path("moto.jpg")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 20,
            "cont": 10,
            "type": "Image",
            "title": "Météo",
            "functions": [(add_image, [], {"filepath": get_path("meteo.jpg")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 25,
            "cont": 110,
            "type": "Image",
            "title": "Collège",
            "functions": [(add_image, [], {"filepath": get_path("college.png")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 30,
            "cont": 415,
            "type": "Image",
            "title": "fille en rouge",
            "functions": [(add_image, [], {"filepath": get_path("fille-rouge.jpg")})],
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 31,
            "cont": 415,
            "type": "Image",
            "title": "carnaval plume",
            "functions": [
                (add_image, [], {"filepath": get_path("carnaval-plume.jpg")})
            ],
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 32,
            "cont": 415,
            "type": "Image",
            "title": "masque carnanval",
            "functions": [
                (add_image, [], {"filepath": get_path("masque-carnaval.jpg")})
            ],
            "trans": ["publish_and_hide"],
        },
        {
            "cid": 33,
            "cont": 415,
            "type": "Image",
            "title": "Sorcière",
            "functions": [(add_image, [], {"filepath": get_path("sorciere.jpg")})],
            "trans": ["publish_and_hide"],
        },
    ]
    cids = create(objects, globl=True)
    cids[10].setLayout("galleryview")


def add_users(portal):
    pass


def add_directory(portal):
    position_types = [{"name": u"Directeur", "token": u"directeur"}]
    organization_types = [
        {"name": u"Communal", "token": u"communal"},
        {"name": u"Privé", "token": u"prive"},
    ]
    organization_levels = [
        {"name": u"Intérieur", "token": u"interieur"},
        {"name": u"Exttérieur", "token": u"exterieur"},
    ]

    params = {
        "position_types": position_types,
        "organization_types": organization_types,
        "organization_levels": organization_levels,
    }
    sportif = api.content.create(
        container=portal,
        type="directory",
        id="annuaire-club-sportifs",
        title=u"Annuaire des clubs sportifs",
        **params
    )

    params = {
        "title": u"Imio",
        "organization_type": u"communal",
    }
    organization1 = api.content.create(
        container=sportif, type="organization", id="imio", **params
    )

    params = {
        "position_types": position_types,
        "organization_types": organization_types,
        "organization_levels": organization_levels,
    }
    fonctionnaires = api.content.create(
        container=portal,
        type="directory",
        id="annuaire-des-fonctionnaires",
        title="Annuaire des fonctionnaires",
        **params
    )

    person = api.content.create(container=fonctionnaires, type="person", id="foobar")
    person.firstname = u"Foo"
    person.lastname = u"Bar"
    person.gender = u"F"
    person.street = u"Zoning Industriel"
    person.number = u"34"
    person.zip_code = u"5190"
    person.city = u"Mornimont"

    params = {
        "title": u"Anciens fonctionnaires",
        "organization_type": u"prive",
    }
    organization2 = api.content.create(
        container=fonctionnaires, type="organization", id="organization2", **params
    )
