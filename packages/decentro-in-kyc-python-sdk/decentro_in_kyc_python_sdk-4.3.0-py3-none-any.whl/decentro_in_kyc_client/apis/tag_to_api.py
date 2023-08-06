import typing_extensions

from decentro_in_kyc_client.apis.tags import TagValues
from decentro_in_kyc_client.apis.tags.kyc_api import KYCApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.KYC: KYCApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.KYC: KYCApi,
    }
)
