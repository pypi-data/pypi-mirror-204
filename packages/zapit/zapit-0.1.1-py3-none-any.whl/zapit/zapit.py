import json
import logging
from typing import List, Optional

from requests import Session
from zapit.exceptions import NoOrganizationError
from zapit.models.network import ConfigNetwork, Network
from zapit.models.network_member import ConfigRequest, NetworkMember
from zapit.models.organizations import (
    Invitation,
    InvitationRequest,
    Member,
    Organization,
)
from zapit.models.user import Token, TokenRequest, User, UserUpdate
from zapit.models.util import RandomToken, Status

from zapit.requestor import RequestException, Requestor

logger = logging.getLogger(__name__)


class Endpoint:
    ...


class Central:
    def __init__(
        self,
        api_key: str,
        session: Optional[Session] = None,
    ) -> None:
        self.api_key = api_key
        self._requestor = Requestor(self.api_key, session=session)

    def list_networks(self) -> List[Network]:
        response = self._requestor.request(
            method="GET",
            path="/network",
            data={},
        )
        logger.info(f"RESPONSE: {json.dumps(response.json(), indent=2)}")
        networks = []
        for network in response.json():
            networks.append(Network(**network))
        return networks

    def create_network(self) -> Network:
        response = self._requestor.request(
            method="POST",
            path="/network",
            data=json.dumps({}),
            headers={"Content-Type": "text/plain"},
        )
        logger.info(f"RESPONSE: {json.dumps(response.json(), indent=2)}")
        if response.status_code != 200:
            raise RequestException(f"Endpoint returned a {response.status_code} error.")
        return Network(**response.json())

    def get_network_by_id(self, network_id: str) -> Network:
        response = self._requestor.request(
            method="GET",
            path=f"/network/{network_id}",
            data={},
        )
        logger.info(f"RESPONSE: {json.dumps(response.json(), indent=2)}")
        return Network(**response.json())

    def update_network_configuration(
        self,
        network_id: str,
        config_network: ConfigNetwork,
    ) -> ConfigNetwork:
        response = self._requestor.request(
            method="POST",
            path=f"/network/{network_id}",
            data=config_network.json(),
        )
        logger.info(f"RESPONSE: {json.dumps(response.json(), indent=2)}")

        return ConfigNetwork(**response.json())

    def delete_network(self, network_id: str) -> None:
        self._requestor.request(
            method="DELETE",
            path=f"/network/{network_id}",
            data={},
        )

    def get_network_members(self, network_id: str) -> List[NetworkMember]:
        response = self._requestor.request(
            method="GET",
            path=f"/network/{network_id}/member",
            data={},
        )
        members = []
        for member in response.json():
            members.append(NetworkMember(**member))
        return members

    def get_network_member_by_id(
        self, network_id: str, member_id: str
    ) -> NetworkMember:
        response = self._requestor.request(
            method="GET",
            path=f"/network/{network_id}/member/{member_id}",
            data={},
        )
        return NetworkMember(**response.json())

    def modify_network_member(
        self,
        network_id: str,
        member_id: str,
        config_request: ConfigRequest,
    ) -> NetworkMember:
        response = self._requestor.request(
            method="POST",
            path=f"/network/{network_id}/member/{member_id}",
            data=config_request.json(),
        )
        return NetworkMember(**response.json())

    def delete_network_member(self, network_id: str, member_id: str) -> None:
        self._requestor.request(
            method="DELETE",
            path=f"/network/{network_id}/member/{member_id}",
            data={},
        )

    def get_user(self, user_id: str) -> User:
        response = self._requestor.request(
            method="GET",
            path=f"/user/{user_id}",
            data={},
        )
        return User(**response.json())

    def update_user(self, user_id: str, user_update: UserUpdate) -> User:
        response = self._requestor.request(
            method="POST",
            path=f"/user/{user_id}",
            data=user_update.json(),
        )
        return User(**response.json())

    def delete_user(self, user_id: str) -> None:
        self._requestor.request(
            method="DELETE",
            path=f"/user/{user_id}",
            data={},
        )

    def add_api_token(self, user_id: str, token: TokenRequest) -> Token:
        response = self._requestor.request(
            method="POST",
            path=f"/user/{user_id}/token",
            data=token.json(),
        )
        return Token(**response.json())

    def delete_api_token(self, user_id: str, token_name: str) -> None:
        self._requestor.request(
            method="DELETE",
            path=f"/user/{user_id}/token/{token_name}",
            data={},
        )

    def get_current_organization(self) -> Organization:
        response = self._requestor.request(
            method="GET",
            path="/org",
            data={},
        )
        decoded_response = response.json()
        if not decoded_response:
            raise NoOrganizationError("Current user does not have an organization.")
        return Organization(**decoded_response)

    def get_organization_by_id(self, org_id: str) -> Organization:
        response = self._requestor.request(
            method="GET",
            path=f"/org/{org_id}",
            data={},
        )
        return Organization(**response.json())

    def get_organization_users(self, org_id: str) -> List[Member]:
        response = self._requestor.request(
            method="GET",
            path=f"/org/{org_id}/user",
            data={},
        )
        members = []
        for member in response.json():
            members.append(Member(**member))
        return members

    def get_organization_invitations(self, org_id: str) -> List[Invitation]:
        response = self._requestor.request(
            method="GET",
            path="/org-invitation",
            data={},
        )
        invitations = []
        for invitation in response.json():
            invitations.append(Invitation(**invitation))
        return invitations

    def invite_user_to_organization(
        self, invitation_request: InvitationRequest
    ) -> Invitation:
        response = self._requestor.request(
            method="POST",
            path="/org-invitation",
            data=invitation_request.json(),
        )
        return Invitation(**response.json())

    def get_organization_invitation_by_id(self, invitation_id: str) -> Invitation:
        response = self._requestor.request(
            method="GET",
            path=f"/org-invitation/{invitation_id}",
            data={},
        )
        return Invitation(**response.json())

    def accept_organization_invitation(self, invitation_id: str) -> Invitation:
        response = self._requestor.request(
            method="POST",
            path=f"/org-invitation/{invitation_id}",
            data={},
        )
        return Invitation(**response.json())

    def decline_organization_invitation(self, invitation_id: str) -> None:
        self._requestor.request(
            method="DELETE",
            path=f"/org-invitation/{invitation_id}",
            data={},
        )

    def get_account_status(self) -> Status:
        response = self._requestor.request(
            method="GET",
            path="/status",
            data={},
        )
        return Status(**response.json())

    def get_random_token(self) -> RandomToken:
        response = self._requestor.request(
            method="GET",
            path="/randomToken",
            data={},
        )
        return RandomToken(**response.json())


class Service:
    ...
