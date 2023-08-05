# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from cbra.types import PolicyPrincipal


class Binding(pydantic.BaseModel):
    role: str = pydantic.Field(
        default=...,
        title="Role",
        description=(
            "Role that is assigned to the list of `members`, or principals. "
            "For example, `roles/viewer`, `roles/editor`, or `roles/owner`."
        )
    )

    members: list[PolicyPrincipal] = pydantic.Field(
        default=[],
        title="Members",
        description=(
            "Specifies the principals requesting access for a resource. "
            "The `members` array can have the following values:\n\n"
            "- **user:{email}**: an email address that is associated to "
            "a specific account."
        )
    )