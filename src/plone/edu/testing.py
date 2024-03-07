from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.distribution.testing.layer import PloneDistributionFixture
from plone.testing.zope import WSGI_SERVER_FIXTURE

import plone.edu  # noQA


DEFAULT_ANSWERS = {
    "site_id": "plone",
    "title": "My University",
    "description": "Site created with A new Plone Distribution",
    "default_language": "de",
    "portal_timezone": "Europe/Berlin",
    "setup_content": True,
}


class BaseFixture(PloneDistributionFixture):
    PACKAGE_NAME = "plone.edu"

    SITES = (("edu", DEFAULT_ANSWERS),)


BASE_FIXTURE = BaseFixture()


class Layer(PloneSandboxLayer):
    defaultBases = (BASE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)


FIXTURE = Layer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="Plone.EduLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="Plone.EduLayer:FunctionalTesting",
)
