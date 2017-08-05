"""
.. module:: checkin_parking.apps.core.backends
   :synopsis: Checkin Parking Reservation Core Authentication Backends.

.. moduleauthor:: Alex Kavanaugh <alex@kavdev.io>

"""

import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django_cas_ng.backends import CASBackend
from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader
from ldap_groups.groups import ADGroup
from rmsconnector.utils import Resident

from ..administration.models import AdminSettings
from ..zones.models import Building


logger = logging.getLogger(__name__)


class CASLDAPBackend(CASBackend):
    """CAS authentication backend with LDAP attribute retrieval."""

    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""

        user = super(CASLDAPBackend, self).authenticate(ticket, service, request)

        # Populate user attributes
        if user:
            try:
                server = Server(settings.LDAP_GROUPS_SERVER_URI)
                connection = Connection(server=server, auto_bind=True, user=settings.LDAP_GROUPS_BIND_DN, password=settings.LDAP_GROUPS_BIND_PASSWORD, raise_exceptions=True)
                connection.start_tls()

                account_def = ObjectDef('user')
                account_def.add(AttrDef('userPrincipalName'))
                account_def.add(AttrDef('displayName'))
                account_def.add(AttrDef('givenName'))
                account_def.add(AttrDef('sn'))
                account_def.add(AttrDef('mail'))

                account_reader = Reader(connection=connection, object_def=account_def, query="userPrincipalName: {principal_name}".format(principal_name=user.username), base=settings.LDAP_GROUPS_BASE_DN)
                account_reader.search_subtree()

                user_info = account_reader.entries[0]
            except Exception as msg:
                logger.exception(msg)
            else:
                principal_name = str(user_info["userPrincipalName"])

                staff_list = [member["userPrincipalName"] for member in ADGroup(settings.LDAP_ADMIN_GROUP).get_tree_members()]
                scanner_list = [member["userPrincipalName"] for member in ADGroup(settings.LDAP_SCANNER_GROUP).get_tree_members()]
                developer_list = [member["userPrincipalName"] for member in ADGroup(settings.LDAP_DEVELOPER_GROUP).get_tree_members()]

                # Add admin flag
                if principal_name in staff_list:
                    user.is_admin = True

                # Add QR scanner flag (stats will be saved)
                if principal_name in scanner_list:
                    user.is_scanner = True

                # Add superuser flags
                if principal_name in developer_list:
                    user.is_staff = True
                    user.is_superuser = True

                user.building = None
                user.term_type = None

                logger.warning("Username: " + user.username)
                logger.warning("Principal Name: " + str(user_info["userPrincipalName"]))

                user.full_name = user_info["displayName"]
                user.first_name = user_info["givenName"]
                user.last_name = user_info["sn"]
                user.email = user.username
                user.save()

        return user
