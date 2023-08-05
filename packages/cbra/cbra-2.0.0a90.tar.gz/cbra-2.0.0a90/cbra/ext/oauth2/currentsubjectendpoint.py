# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .endpoints import AuthorizationServerEndpoint


class CurrentSubjectEndpoint(AuthorizationServerEndpoint):
    name: str = 'oauth2.me'
    path: str = '/me'
    summary: str = 'Current User Endpoint'

    async def get(self) -> dict[str, Any]:
        await self.session
        claims: dict[str, Any] = {
            'sub': 'allUsers',
            'mailboxes': []
        }
        if self.is_authenticated():
            claims['sub'] = 'self'
            subject = await self.get_subject()
            for principal in subject.get_principals():
                if principal.spec.kind != 'EmailAddress':
                    continue
                claims['mailboxes'].append({
                    'principal_id': principal.key,
                    'email': principal.spec.email
                })

        return claims