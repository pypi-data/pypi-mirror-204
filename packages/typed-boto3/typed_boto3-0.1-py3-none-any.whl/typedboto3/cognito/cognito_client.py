from typing import Any

import boto3

from typedboto3.cognito.request import (
    AdminInitiateAuthRequest,
    AdminUpdateUserAttributesRequest,
    ChangePasswordRequest,
    ConfirmForgotPasswordRequest,
    ConfirmSignUpRequest,
    ForgotPasswordRequest,
    InitiateAuthRequest,
    ResendConfirmationCodeRequest,
    RevokeTokenRequest,
    SignUpRequest,
)
from typedboto3.cognito.response import (
    AdminInitiateAuthResponse,
    GetCognitoUserResponse,
    InitiateAuthResponse,
    SignUpResponse,
)

from typedboto3.util.convert import convert_to_dict


class CognitoClient:
    client: Any = None

    def __init__(self, region_name: str):
        if self.client is None:
            self.client = boto3.client("cognito-idp", region_name=region_name)

    def admin_initiate_auth(self, request: AdminInitiateAuthRequest):
        request_raw = convert_to_dict(request)
        response_raw = self.client.admin_initiate_auth(**request_raw)

        return AdminInitiateAuthResponse(**response_raw)

    def initiate_auth(self, request: InitiateAuthRequest):
        request_raw = convert_to_dict(request)
        response_raw = self.client.initiate_auth(**request_raw)

        return InitiateAuthResponse(**response_raw)

    def sign_up(self, request: SignUpRequest):
        if request.UserAttributes:
            request.UserAttributes = [dict(elem) for elem in request.UserAttributes]

        request_raw = convert_to_dict(request)
        response_raw = self.client.sign_up(**request_raw)

        return SignUpResponse(**response_raw)

    def confirm_sign_up(self, request: ConfirmSignUpRequest):
        request_raw = convert_to_dict(request)
        self.client.confirm_sign_up(**request_raw)

    def get_user(self, access_token: str):
        response_raw = self.client.get_user(AccessToken=access_token)

        return GetCognitoUserResponse(**response_raw)

    def resend_confirmation_code(self, request: ResendConfirmationCodeRequest):
        request_raw = convert_to_dict(request)
        self.client.resend_confirmation_code(**request_raw)

    def forgot_password(self, request: ForgotPasswordRequest):
        request_raw = convert_to_dict(request)
        self.client.forgot_password(**request_raw)

    def confirm_forgot_password(self, request: ConfirmForgotPasswordRequest):
        request_raw = convert_to_dict(request)
        self.client.confirm_forgot_password(**request_raw)

    def revoke_token(self, request: RevokeTokenRequest):
        request_raw = convert_to_dict(request)
        self.client.revoke_token(**request_raw)

    def admin_update_user_attributes(self, request: AdminUpdateUserAttributesRequest):
        if request.UserAttributes:
            request.UserAttributes = [dict(elem) for elem in request.UserAttributes]

        request_raw = convert_to_dict(request)
        self.client.admin_update_user_attributes(**request_raw)

    def change_password(self, request: ChangePasswordRequest):
        request_raw = convert_to_dict(request)
        self.client.change_password(**request_raw)
