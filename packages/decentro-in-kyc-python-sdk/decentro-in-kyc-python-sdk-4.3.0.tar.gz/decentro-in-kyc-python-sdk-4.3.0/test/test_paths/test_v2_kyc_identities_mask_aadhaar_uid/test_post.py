# coding: utf-8

"""
    decentro-in-kyc

    KYC & Onboarding

    The version of the OpenAPI document: 1.0.0
    Contact: admin@decentro.tech
    Created by: https://decentro.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import decentro_in_kyc_client
from decentro_in_kyc_client.paths.v2_kyc_identities_mask_aadhaar_uid import post
from decentro_in_kyc_client import configuration, schemas, api_client

from .. import ApiTestMixin


class TestV2KycIdentitiesMaskAadhaarUid(ApiTestMixin, unittest.TestCase):
    """
    V2KycIdentitiesMaskAadhaarUid unit test stubs
        Aadhaar Masking
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    response_status = 200




if __name__ == '__main__':
    unittest.main()
