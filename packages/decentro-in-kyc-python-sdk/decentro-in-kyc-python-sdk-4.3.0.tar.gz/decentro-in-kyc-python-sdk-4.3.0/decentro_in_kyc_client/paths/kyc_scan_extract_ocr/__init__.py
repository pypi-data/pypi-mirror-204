# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from decentro_in_kyc_client.paths.kyc_scan_extract_ocr import Api

from decentro_in_kyc_client.paths import PathValues

path = PathValues.KYC_SCAN_EXTRACT_OCR