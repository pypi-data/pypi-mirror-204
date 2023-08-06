# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from decentro_in_kyc_client.paths.kyc_public_registry_validate import Api

from decentro_in_kyc_client.paths import PathValues

path = PathValues.KYC_PUBLIC_REGISTRY_VALIDATE