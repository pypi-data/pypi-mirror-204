# coding: utf-8
"""
    decentro-in-kyc

    KYC & Onboarding

    The version of the OpenAPI document: 1.0.0
    Contact: admin@decentro.tech
    Created by: https://decentro.tech
"""

from decentro_in_kyc_client.configuration import Configuration
from decentro_in_kyc_client.api_client import ApiClient
from decentro_in_kyc_client.apis.tags.kyc_api import KYCApi


class Decentro:

    def __init__(self, configuration: Configuration = None, **kwargs):
        if (len(kwargs) > 0):
            configuration = Configuration(**kwargs)
        if (configuration is None):
            raise Exception("configuration is required")
        api_client = ApiClient(configuration)
        self.kyc = KYCApi(api_client)
