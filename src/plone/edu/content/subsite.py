import logging

from plone.dexterity.content import Container
from plone.supermodel.model import Schema
from zope.interface import implementer

from plone import api

logger = logging.getLogger(__name__)


class ISubsite(Schema):
    """Subsite content type interface"""


ADD_ROLES = ("Manager", "Site Administrator", "Editor")

SUBSITE_GROUPS = (
    {
        "id": "siteadmins",
        "roles": ("Contributor", "Editor", "Reader", "Reviewer", "SubsiteAdmin"),
    },
    {
        "id": "publishers",
        "roles": ("Contributor", "Editor", "Reader", "Reviewer"),
    },
    {
        "id": "editors",
        "roles": ("Contributor", "Editor", "Reader"),
    },
    {
        "id": "readers",
        "roles": ("Reader",),
    },
)


@implementer(ISubsite)
class Subsite(Container):
    """Subsite content type"""
