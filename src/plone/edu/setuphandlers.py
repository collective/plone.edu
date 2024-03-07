import logging
from pathlib import Path
from typing import Iterable

from plone.app.multilingual.browser.setup import SetupMultilingualSite
from Products.CMFCore.indexing import processQueue
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from plone import api

logger = logging.getLogger("plone.edu.setuphandlers")


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return ["plone.edu:uninstall"]


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def package_root_folder() -> Path:
    current_folder = Path(__file__).parent.resolve()
    return current_folder.parent


def post_install(context):
    """Post install script"""
    portal = api.portal.get()

    enable_pam(portal)

    # make sure indexing queue is processed while component site is still active
    processQueue()


def initial_setup(context):
    post_install(context)

def print_error(error_string):  # RED
    print(f"\033[31mERROR: {error_string}\033[0m")  # noqa
    logger.error(f"{error_string}")


def print_info(info_string):  # GREEN
    print(f"\033[33m{info_string}\033[0m")  # noqa
    logger.info(f"{info_string}")


def create_object(path, is_folder=False):
    """Recursively create object and folder structure if necessary"""
    obj = api.content.get(path=path)
    if obj is not None:
        return obj

    path_parent, obj_id = path.rsplit("/", 1)
    if path_parent == "":
        parent = api.portal.get()
    else:
        parent = create_object(path_parent, is_folder=True)

    print_info(f'Creating "{path}"')

    obj = api.content.create(
        container=parent, type="Folder" if is_folder else "Document", id=obj_id
    )
    api.content.transition(obj=obj, transition="publish")
    return obj


def enable_pam(portal):
    # Setup the plone.app.multilingual data
    # (we can go back to using the version in kitconcept.volto
    # once https://github.com/plone/plone.app.multilingual/pull/404
    # is released)
    sms = SetupMultilingualSite(portal)
    sms.setupSite(portal)
    enable_translatable_behavior(portal)
    if "de" in portal and "assets" in portal.de:
        api.content.delete(obj=portal.de.assets, check_linkintegrity=False)
    if "en" in portal and "assets" in portal.en:
        api.content.delete(obj=portal.en.assets, check_linkintegrity=False)


def enable_translatable_behavior(portal):
    types_tool = portal.portal_types

    # Iterate through all Dexterity content type, except the site root
    all_ftis = types_tool.listTypeInfo()
    dx_ftis = (
        fti
        for fti in all_ftis
        if getattr(fti, "behaviors", False) and fti.getId() != "Plone Site"
    )
    for fti in dx_ftis:
        # Enable translatable behavior for all types
        behaviors = list(fti.behaviors)
        if "plone.translatable" not in behaviors:
            behaviors.append("plone.translatable")
            fti._updateProperty("behaviors", tuple(behaviors))