# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from decentro_in_kyc_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V2_KYC_IDENTITIES_MASK_AADHAAR_UID = "/v2/kyc/identities/mask_aadhaar_uid"
    V2_KYC_FORENSICS_IMAGE_QUALITY = "/v2/kyc/forensics/image_quality"
    V2_KYC_FORENSICS_FACE_MATCH = "/v2/kyc/forensics/face_match"
    V2_KYC_DOCUMENT_CLASSIFICATION = "/v2/kyc/document_classification"
    V2_KYC_FORENSICS_PHOTOCOPY_CHECK = "/v2/kyc/forensics/photocopy_check"
    KYC_SCAN_EXTRACT_OCR = "/kyc/scan_extract/ocr"
    KYC_PUBLIC_REGISTRY_VALIDATE = "/kyc/public_registry/validate"
    V2_KYC_FORENSICS_VIDEO_LIVENESS = "/v2/kyc/forensics/video_liveness"
