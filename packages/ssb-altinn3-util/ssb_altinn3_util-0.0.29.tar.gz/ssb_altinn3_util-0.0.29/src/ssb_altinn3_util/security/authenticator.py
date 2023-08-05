from typing import List

from fastapi import Request, HTTPException

from ssb_altinn3_util.security.authorization_result import AuthorizationResult
from ssb_altinn3_util.security.helpers import jwt_helper
from ssb_altinn3_util.security.helpers import auth_service_client

import ssb_altinn3_util.security.authenticator_constants as constants


class Authenticator:
    """
    Authorization component to be injected in api-endpoint as a dependency.  Requires the following to function
    properly:
    Env variable AUTH_SERVICE_URL must be set with the full absolute url to the authorization service endpoint.
    The request object (fastapi.Request) must be present as a function argument in the function using the component.
    The role-argument must be one of the roles defined in authenticator_constants (in ssb_altinn3_util.security).

    Form access must be validated in the actual endpoint code, calling the verify_access function of the
    authenticator.  Example:

    @app.get("/stuff")
    def do_stuff(form: str, request: Request, auth: Authenticator = Depends(Authenticator(role=ROLE_USER):
        auth.verify_access(form)
        ....

    """

    required_role: str
    allowed_forms: List[str]

    def __init__(self, role: str):
        if role not in constants.VALID_ROLES:
            raise ValueError(f"Supplied role '{role}' is not a valid role!")
        self.required_role = role
        self.allowed_forms = []

    def __call__(self, request: Request):
        auth_header = request.headers.get("authorization", None)
        if not auth_header:
            raise HTTPException(status_code=401, detail="No token provided")
        user_email = jwt_helper.get_user_email_from_token(auth_header)
        if not user_email:
            raise HTTPException(
                status_code=401, detail="Unable to find user email in supplied token!"
            )
        result: AuthorizationResult = auth_service_client.verify_access(
            user_email, self.required_role
        )
        if not result.access_granted:
            raise HTTPException(
                status_code=result.status_code, detail=result.error_message
            )
        self.allowed_forms = result.allowed_forms
        return self

    def verify_form_access(self, form: str) -> bool:
        if (
            constants.FORM_ACCESS_ALL in self.allowed_forms
            or form in self.allowed_forms
        ):
            return True
        raise HTTPException(
            status_code=403, detail=f"User has insufficient access to form '{form}'"
        )
