import typing_extensions

from decentro_in_kyc_client.paths import PathValues
from decentro_in_kyc_client.apis.paths.v2_kyc_identities_mask_aadhaar_uid import V2KycIdentitiesMaskAadhaarUid
from decentro_in_kyc_client.apis.paths.v2_kyc_forensics_image_quality import V2KycForensicsImageQuality
from decentro_in_kyc_client.apis.paths.v2_kyc_forensics_face_match import V2KycForensicsFaceMatch
from decentro_in_kyc_client.apis.paths.v2_kyc_document_classification import V2KycDocumentClassification
from decentro_in_kyc_client.apis.paths.v2_kyc_forensics_photocopy_check import V2KycForensicsPhotocopyCheck
from decentro_in_kyc_client.apis.paths.kyc_scan_extract_ocr import KycScanExtractOcr
from decentro_in_kyc_client.apis.paths.kyc_public_registry_validate import KycPublicRegistryValidate
from decentro_in_kyc_client.apis.paths.v2_kyc_forensics_video_liveness import V2KycForensicsVideoLiveness

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V2_KYC_IDENTITIES_MASK_AADHAAR_UID: V2KycIdentitiesMaskAadhaarUid,
        PathValues.V2_KYC_FORENSICS_IMAGE_QUALITY: V2KycForensicsImageQuality,
        PathValues.V2_KYC_FORENSICS_FACE_MATCH: V2KycForensicsFaceMatch,
        PathValues.V2_KYC_DOCUMENT_CLASSIFICATION: V2KycDocumentClassification,
        PathValues.V2_KYC_FORENSICS_PHOTOCOPY_CHECK: V2KycForensicsPhotocopyCheck,
        PathValues.KYC_SCAN_EXTRACT_OCR: KycScanExtractOcr,
        PathValues.KYC_PUBLIC_REGISTRY_VALIDATE: KycPublicRegistryValidate,
        PathValues.V2_KYC_FORENSICS_VIDEO_LIVENESS: V2KycForensicsVideoLiveness,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V2_KYC_IDENTITIES_MASK_AADHAAR_UID: V2KycIdentitiesMaskAadhaarUid,
        PathValues.V2_KYC_FORENSICS_IMAGE_QUALITY: V2KycForensicsImageQuality,
        PathValues.V2_KYC_FORENSICS_FACE_MATCH: V2KycForensicsFaceMatch,
        PathValues.V2_KYC_DOCUMENT_CLASSIFICATION: V2KycDocumentClassification,
        PathValues.V2_KYC_FORENSICS_PHOTOCOPY_CHECK: V2KycForensicsPhotocopyCheck,
        PathValues.KYC_SCAN_EXTRACT_OCR: KycScanExtractOcr,
        PathValues.KYC_PUBLIC_REGISTRY_VALIDATE: KycPublicRegistryValidate,
        PathValues.V2_KYC_FORENSICS_VIDEO_LIVENESS: V2KycForensicsVideoLiveness,
    }
)
