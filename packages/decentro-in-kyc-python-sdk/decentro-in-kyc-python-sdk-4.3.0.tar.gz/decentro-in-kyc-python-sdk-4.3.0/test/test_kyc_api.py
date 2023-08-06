"""
    decentro-in-kyc

    KYC & Onboarding  # noqa: E501

    The version of the OpenAPI document: 1.0.0
"""


import unittest

import os
import uuid
import time

from decentro_in_kyc_client import Decentro
from decentro_in_kyc_client.exceptions import ApiException, MissingRequiredParametersError, ClientConfigurationError, SchemaValidationError, InvalidHostConfigurationError


class TestKYCApi(unittest.TestCase):
    """KYCApi unit test stubs"""

    # Just to keep things DRY
    consent_purpose = "Testing Python SDK - Konfig"
    dir = os.path.dirname(__file__)

    def setUp(self):
        self.api = Decentro(
            client_id=os.environ["DECENTRO_CLIENT_ID"],
            client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
            module_secret=os.environ["DECENTRO_MODULE_SECRET"]
        ).kyc

    def tearDown(self):
        pass

    def test_missing_credentials_raises_Error(self):
        # missing client_id
        self.assertRaises(ClientConfigurationError, lambda: Decentro(
            client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
            module_secret=os.environ["DECENTRO_MODULE_SECRET"]
        ))
        self.assertRaises(ClientConfigurationError, lambda: Decentro(
            client_id='',
            client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
            module_secret=os.environ["DECENTRO_MODULE_SECRET"]
        ))
        # missing client_secret
        self.assertRaises(ClientConfigurationError, lambda: Decentro(
            client_id=os.environ["DECENTRO_CLIENT_ID"],
            module_secret=os.environ["DECENTRO_MODULE_SECRET"]
        ))
        self.assertRaises(ClientConfigurationError, lambda: Decentro(
            client_secret='',
            client_id=os.environ["DECENTRO_CLIENT_ID"],
            module_secret=os.environ["DECENTRO_MODULE_SECRET"]
        ))
        # missing module_secret
        self.assertRaises(ClientConfigurationError, lambda: Decentro(
            client_id=os.environ["DECENTRO_CLIENT_ID"],
            client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
        ))
        self.assertRaises(ClientConfigurationError, lambda: Decentro(
            module_secret='',
            client_id=os.environ["DECENTRO_CLIENT_ID"],
            client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
        ))

    def test_check_image_quality(self):
        """Test case for check_image_quality

        Image Quality Check  # noqa: E501
        """

        """
        Invalid type for variable 'score'. Required value type is int and passed
        type was float at
        ['received_data']['data']['image_quality']['quality_scores']['text_quality']['score']
        """
        image = open(os.path.join(self.dir, 'test_kyc_api/randomImage.jpg'), 'rb')
        response = self.api.check_image_quality(body={
            "consent": True, "consent_purpose": self.consent_purpose, "reference_id": str(uuid.uuid4()), "image": image})
        assert response is not None, "Response is null"

    def test_check_photocopy(self):
        """Test case for check_photocopy

        Photocopy Check  # noqa: E501
        """
        image = open(os.path.join(self.dir, 'test_kyc_api/randomImage.jpg'), 'rb')
        response = self.api.check_photocopy(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "image":image})
        assert response is not None, "Response is null"

    def test_check_video_liveness(self):
        """Test case for check_video_liveness

        Liveness Check  # noqa: E501
        """
        video = open(os.path.join(self.dir, 'test_kyc_api/video-5-seconds.mp4'), 'rb')
        response = self.api.check_video_liveness(body={
            "consent":"Y", "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "video":video})
        assert response is not None, "Response is null"

        video = open(os.path.join(self.dir, 'test_kyc_api/video-11-seconds.webm'), 'rb')
        self.assertRaises(ApiException, lambda: self.api.check_video_liveness(body={
            "consent":"Y", "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "video":video}))

    def test_classify_document(self):
        """Test case for classify_document

        ID Classification  # noqa: E501
        """
        document = open(os.path.join(self.dir, 'test_kyc_api/sampleAadhaar.jpeg'), 'rb')
        response = self.api.classify_document(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "document":document, "document_type":"Aadhaar"})
        assert response is not None, "Response is null"

        document = open(os.path.join(self.dir, 'test_kyc_api/sampleDL.jpeg'), 'rb')
        response = self.api.classify_document(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "document":document, "document_type":"Driving_License"})
        assert response is not None, "Response is null"

        document = open(os.path.join(self.dir, 'test_kyc_api/samplePAN.jpeg'), 'rb')
        response = self.api.classify_document(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "document":document, "document_type":"pan"})
        assert response is not None, "Response is null"

        document = open(os.path.join(self.dir, 'test_kyc_api/samplePassport.jpeg'), 'rb')
        response = self.api.classify_document(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "document":document, "document_type":"Passport"})
        assert response is not None, "Response is null"

        document = open(os.path.join(self.dir, 'test_kyc_api/sampleVoterID.png'), 'rb')
        response = self.api.classify_document(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "document":document, "document_type":"Voterid"})
        assert response is not None, "Response is null"

    def test_extract_text(self):
        """Test case for extract_text

        Scan & Extract  # noqa: E501
        """
        document = open(os.path.join(self.dir, 'test_kyc_api/sampleAadhaar.jpeg'), 'rb')
        response = self.api.extract_text(body={
            "consent":"Y", "consent_purpose":self.consent_purpose, "reference_id":str( uuid.uuid4()), "document_type":"Aadhaar", "document":document, "kyc_validate":1})
        assert response is not None, "Response is null"

    def test_mask_aadhaar_uid(self):
        """Test case for mask_aadhaar_uid

        Aadhaar Masking  # noqa: E501
        """
        image = open(os.path.join(self.dir, 'test_kyc_api/sampleAadhaar.jpeg'), 'rb')
        response = self.api.mask_aadhaar_uid(body={
            "consent":True, "consent_purpose":self.consent_purpose, "reference_id":str(uuid.uuid4()), "image":image})
        assert response is not None, "Response is null"

    def test_match_face(self):
        """Test case for match_face

        Face Match  # noqa: E501
        """
        image1 = open(os.path.join(self.dir, 'test_kyc_api/selfie1.jpg'), 'rb')
        image2 = open(os.path.join(self.dir, 'test_kyc_api/selfie2.jpg'), 'rb')
        response = self.api.match_face(body={
            "consent":'Y', "consent_purpose":self.consent_purpose, "reference_id":str( uuid.uuid4()), "image1":image1, "image2":image2})
        assert response is not None, "Response is null"

    def test_validate_invalid_document_type_raises_error(self):
        """Test case for validate

        Invalid Validate 
        """
        self.assertRaises(ApiException, lambda: self.api.validate(body={
            "reference_id":str(uuid.uuid4()), "consent":"Y", "consent_purpose":self.consent_purpose, "document_type":"Some invalid type", "id_number":"UP28A0008214"}
        ))

    def test_validate_missing_required_field_raises_error(self):
        """Test case for validate

        Missing required field
        """
        with self.assertRaises(MissingRequiredParametersError) as cm:
            self.api.validate(body={
                "reference_id":str(uuid.uuid4()), "consent":"Y", "document_type":"Some invalid type", "id_number":"UP28A0008214"}
            )
        self.assertEqual(str(cm.exception), "Missing 1 required parameter: 'consent_purpose'")
        with self.assertRaises(MissingRequiredParametersError) as cm:
            self.api.validate(body={
                "reference_id":str(uuid.uuid4()), "document_type":"Some invalid type", "id_number":"UP28A0008214"}
            )
        self.assertEqual(str(cm.exception), "Missing 2 required parameters: 'consent' and 'consent_purpose'")

    def test_validate_empty_required_field_raises_error(self):
        """Test case for validate

        Empty required field
        """
        with self.assertRaises(SchemaValidationError) as cm:
            self.api.validate(body={
                "reference_id": str(uuid.uuid4()), "consent": "Y", "consent_purpose": "", "document_type": "Some invalid type", "id_number": "UP28A0008214"}
            )
        self.assertEqual(str(cm.exception), '1 invalid argument. Invalid value ``, length must be greater than or equal to `1` at "consent_purpose"')
        # Test stripping of required properties
        with self.assertRaises(SchemaValidationError) as cm:
            self.api.validate(body={
                "reference_id": str(uuid.uuid4()), "consent": "Y", "consent_purpose": " ", "document_type": "Some invalid type", "id_number": "UP28A0008214"}
            )
        self.assertEqual(str(cm.exception), '1 invalid argument. Invalid value ``, length must be greater than or equal to `1` at "consent_purpose"')
    
    def test_trailing_slash_is_removed_from_host(self):
        api = Decentro(
            host="https://example.com/",
            client_id=os.environ["DECENTRO_CLIENT_ID"],
            client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
            module_secret=os.environ["DECENTRO_MODULE_SECRET"]
        )
        self.assertEqual(api.kyc.api_client.configuration.host, "https://example.com")
    
    def test_invalid_host_raises_error(self):
        valid_test_cases = [
            "https://www.example.com/",
            "https://www.example.com/path/to/resource",
            "http://localhost:8000/",
            "https://127.0.0.1/",
        ]

        invalid_test_cases = [
            ("www.example.com", 'Invalid host: "www.example.com", scheme must be "http" or "https"'),
            ("https://www.example.com:", 'Invalid host: "https://www.example.com:", invalid url'),
            ("https://www.example.com/path/to/resource?param1=value1&param2=value2", 'Invalid host: "https://www.example.com/path/to/resource?param1=value1&param2=value2", query string is not allowed'),
            ("https://www.example.com/path/to/resource#fragment", 'Invalid host: "https://www.example.com/path/to/resource#fragment", fragment is not allowed'),
            ("ftp://www.example.com/", 'Invalid host: "ftp://www.example.com/", scheme must be "http" or "https"'),
            ("https://www.ex*mple.com/", 'Invalid host: "https://www.ex*mple.com/", invalid url'),
            ("https://www.example.com/path/to/ resou rce", 'Invalid host: "https://www.example.com/path/to/ resou rce", invalid url'),
            ("https://www.example.com/ path/to/resource", 'Invalid host: "https://www.example.com/ path/to/resource", invalid url'),
        ]

        for valid_url in valid_test_cases:
            Decentro(
                host=valid_url,
                client_id=os.environ["DECENTRO_CLIENT_ID"],
                client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
                module_secret=os.environ["DECENTRO_MODULE_SECRET"]
            )
        for invalid_url, msg in invalid_test_cases:
            with self.assertRaises(InvalidHostConfigurationError) as cm:
                Decentro(
                    host=invalid_url,
                    client_id=os.environ["DECENTRO_CLIENT_ID"],
                    client_secret=os.environ["DECENTRO_CLIENT_SECRET"],
                    module_secret=os.environ["DECENTRO_MODULE_SECRET"]
                )
            self.assertEqual(str(cm.exception), msg)

    def test_validate_incorrect_data_type_and_value_raises_error(self):
        """Test case for validate

        Incorrect data types field
        """
        with self.assertRaises(SchemaValidationError) as cm:
            self.api.validate(body={
                "reference_id": str(uuid.uuid4()),
                "consent": True, # invalid data type
                "consent_purpose": " ", # invalid value
                "document_type": "Some invalid type",
                "id_number": "UP28A0008214"
            })
        self.assertEqual(str(cm.exception), '2 invalid arguments. Got BoolClass(True) for required type str at "consent". Invalid value ``, length must be greater than or equal to `1` at "consent_purpose"')
        with self.assertRaises(SchemaValidationError) as cm:
            self.api.validate(body={
                "reference_id": str(uuid.uuid4()),
                "consent": True, # invalid data type
                "consent_purpose": "Test Consent", # invalid value
                "document_type": 1234,
                "id_number": "UP28A0008214"
            })
        self.assertEqual(str(cm.exception),  '2 invalid arguments. Got BoolClass(True) for required type str at "consent". Got int(1234) for required type str at "document_type"')

    def test_validate_multiple_incorrect_data_type_raises_error(self):
        """Test case for validate

        Incorrect data types field
        """
        with self.assertRaises(SchemaValidationError) as cm:
            self.api.validate(body={
                "reference_id": str(uuid.uuid4()),
                "consent": True, # invalid data type
                "consent_purpose": 1, # invalid data type
                "document_type": "Some invalid type",
                "id_number": "UP28A0008214"
            })
        self.assertEqual(str(cm.exception), '2 invalid arguments. Got BoolClass(True) for required type str at "consent". Got int(1) for required type str at "consent_purpose"')
        

    def test_validate_valid(self):
        """Test case for validate

        Validate  # noqa: E501
        """

        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type": "Udyog_Aadhaar",
            "id_number": "UP28A0008214"
        })
        assert response is not None, "Response is null"
        assert response.round_trip_time is not None, "Round trip time exists"
        assert response.body['kycStatus'] == "SUCCESS", "Status is successful"
        assert response.body['kycResult']['status'] == "ACTIVE", "Result is active"

        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"FSSAI",
            "id_number":"20821012000345"
        })
        assert response is not None, "Response is null"

        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"PAN",
            "id_number":"BDAPC9977L"
        })
        assert response is not None, "Response is null"

        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"VoterID",
            "id_number":"KJC7967979"
        })
        assert response is not None, "Response is null"

        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"CIN",
            "id_number":"U67190TN2014PTC096978"
        })
        assert response is not None, "Response is null"

        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"GSTIN",
            "id_number":"26AAACP3812E1ZV"
        })
        assert response is not None, "Response is null"

        """
        HTTP response body: {"status": "SUCCESS", "kycStatus": "UNKNOWN",
        "error": {"message": "No records found for the given ID.",
        "responseCode": "E00026"}, "requestTimestamp": "2023-01-27
        15:23:28.321986 IST (GMT +0530)", "responseTimestamp": "2023-01-27
        15:23:37.282835 IST (GMT +0530)", "decentroTxnId":
        "6A7E6B2A792049E389F642881536E16E"}
        """
        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"Driving_License",
            "id_number":"GJ0119960040773",
            "dob":"1996-08-13"
        })
        assert response is not None, "Response is null"

        """
        HTTP response body: {"status": "FAILURE", "kycStatus": "UNKNOWN",
        "error": {"message": "Name is mandatory when verifying passport. Hint:
        name (string).", "responseCode": "E00009"}, "requestTimestamp":
        "2023-01-27 15:20:23.805948 IST (GMT +0530)", "responseTimestamp":
        "2023-01-27 15:20:23.817793 IST (GMT +0530)", "decentroTxnId":
        "2E0CE8C0F0FC43F3B4B741B0F8DAE1BA"}
        """
        """
        {"status": "FAILURE", "kycStatus": "UNKNOWN", "error": {"message": "File
        number provided is not valid, It should be exactly of 15 characters
        long. Hint: id_number (string).", "responseCode": "E00009"},
        "requestTimestamp": "2023-02-01 14:33:34.057365 IST (GMT +0530)",
        "responseTimestamp": "2023-02-01 14:33:34.072897 IST (GMT +0530)",
        "decentroTxnId": "7CE473DD50664223A29FD44A768BB948"}
        """
        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"Passport",
            "id_number":"8707305F2709042",
            "name":"J8369854",
            "dob":"1996-08-13"
        })
        assert response is not None, "Response is null"

        """
        HTTP response body: {"status": "FAILURE", "kycStatus": "UNKNOWN",
        "error": {"message": "Internal Server Error. Please try again after
        sometime. If the problem persists, please drop a mail to
        support@decentro.tech.", "responseCode": "E00000"}, "requestTimestamp":
        "2023-01-27 15:21:50.958320 IST (GMT +0530)", "responseTimestamp":
        "2023-01-27 15:21:53.614626 IST (GMT +0530)", "decentroTxnId":
        "C623B47AF92E4A4DB0E3E32D8B5B9F1A"}
        """
        response = self.api.validate(body={
            "reference_id":str(time.time_ns()),
            "consent":"Y",
            "consent_purpose":self.consent_purpose,
            "document_type":"RC",
            "id_number":"TN72AS0765"
        })
        assert response is not None, "Response is null"


if __name__ == '__main__':
    unittest.main()
