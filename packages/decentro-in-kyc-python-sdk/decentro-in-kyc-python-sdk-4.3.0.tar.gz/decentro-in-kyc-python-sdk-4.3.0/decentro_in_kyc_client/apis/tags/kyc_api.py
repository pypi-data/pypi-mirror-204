# coding: utf-8

"""
    decentro-in-kyc

    KYC & Onboarding

    The version of the OpenAPI document: 1.0.0
    Contact: admin@decentro.tech
    Created by: https://decentro.tech
"""

from decentro_in_kyc_client.paths.v2_kyc_forensics_image_quality.post import CheckImageQuality
from decentro_in_kyc_client.paths.v2_kyc_forensics_photocopy_check.post import CheckPhotocopy
from decentro_in_kyc_client.paths.v2_kyc_forensics_video_liveness.post import CheckVideoLiveness
from decentro_in_kyc_client.paths.v2_kyc_document_classification.post import ClassifyDocument
from decentro_in_kyc_client.paths.kyc_scan_extract_ocr.post import ExtractText
from decentro_in_kyc_client.paths.v2_kyc_identities_mask_aadhaar_uid.post import MaskAadhaarUid
from decentro_in_kyc_client.paths.v2_kyc_forensics_face_match.post import MatchFace
from decentro_in_kyc_client.paths.kyc_public_registry_validate.post import Validate


class KYCApi(
    CheckImageQuality,
    CheckPhotocopy,
    CheckVideoLiveness,
    ClassifyDocument,
    ExtractText,
    MaskAadhaarUid,
    MatchFace,
    Validate,
):
    """NOTE:
    This class is auto generated
    """
    pass
