# coding: utf-8

"""
    decentro-in-kyc

    KYC & Onboarding

    The version of the OpenAPI document: 1.0.0
    Contact: admin@decentro.tech
    Created by: https://decentro.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from decentro_in_kyc_client import schemas  # noqa: F401


class ExtractTextRequest(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        required = {
            "reference_id",
            "consent",
            "consent_purpose",
            "kyc_validate",
            "document_type",
        }
        
        class properties:
            
            
            class reference_id(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    min_length = 1
                    x_konfig_strip = True
            
            
            class document_type(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    min_length = 1
                    x_konfig_strip = True
            
            
            class consent(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    min_length = 1
                    x_konfig_strip = True
            
            
            class consent_purpose(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    min_length = 1
                    x_konfig_strip = True
            kyc_validate = schemas.IntSchema
            document = schemas.BinarySchema
            document_url = schemas.StrSchema
            document_back = schemas.BinarySchema
            document_back_url = schemas.StrSchema
            __annotations__ = {
                "reference_id": reference_id,
                "document_type": document_type,
                "consent": consent,
                "consent_purpose": consent_purpose,
                "kyc_validate": kyc_validate,
                "document": document,
                "document_url": document_url,
                "document_back": document_back,
                "document_back_url": document_back_url,
            }
    
    reference_id: MetaOapg.properties.reference_id
    consent: MetaOapg.properties.consent
    consent_purpose: MetaOapg.properties.consent_purpose
    kyc_validate: MetaOapg.properties.kyc_validate
    document_type: MetaOapg.properties.document_type
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reference_id"]) -> MetaOapg.properties.reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document_type"]) -> MetaOapg.properties.document_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["consent"]) -> MetaOapg.properties.consent: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["consent_purpose"]) -> MetaOapg.properties.consent_purpose: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["kyc_validate"]) -> MetaOapg.properties.kyc_validate: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document"]) -> MetaOapg.properties.document: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document_url"]) -> MetaOapg.properties.document_url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document_back"]) -> MetaOapg.properties.document_back: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document_back_url"]) -> MetaOapg.properties.document_back_url: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["reference_id", "document_type", "consent", "consent_purpose", "kyc_validate", "document", "document_url", "document_back", "document_back_url", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reference_id"]) -> MetaOapg.properties.reference_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document_type"]) -> MetaOapg.properties.document_type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["consent"]) -> MetaOapg.properties.consent: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["consent_purpose"]) -> MetaOapg.properties.consent_purpose: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["kyc_validate"]) -> MetaOapg.properties.kyc_validate: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document"]) -> typing.Union[MetaOapg.properties.document, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document_url"]) -> typing.Union[MetaOapg.properties.document_url, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document_back"]) -> typing.Union[MetaOapg.properties.document_back, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document_back_url"]) -> typing.Union[MetaOapg.properties.document_back_url, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["reference_id", "document_type", "consent", "consent_purpose", "kyc_validate", "document", "document_url", "document_back", "document_back_url", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        reference_id: typing.Union[MetaOapg.properties.reference_id, str, ],
        consent: typing.Union[MetaOapg.properties.consent, str, ],
        consent_purpose: typing.Union[MetaOapg.properties.consent_purpose, str, ],
        kyc_validate: typing.Union[MetaOapg.properties.kyc_validate, decimal.Decimal, int, ],
        document_type: typing.Union[MetaOapg.properties.document_type, str, ],
        document: typing.Union[MetaOapg.properties.document, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        document_url: typing.Union[MetaOapg.properties.document_url, str, schemas.Unset] = schemas.unset,
        document_back: typing.Union[MetaOapg.properties.document_back, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        document_back_url: typing.Union[MetaOapg.properties.document_back_url, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExtractTextRequest':
        return super().__new__(
            cls,
            *args,
            reference_id=reference_id,
            consent=consent,
            consent_purpose=consent_purpose,
            kyc_validate=kyc_validate,
            document_type=document_type,
            document=document,
            document_url=document_url,
            document_back=document_back,
            document_back_url=document_back_url,
            _configuration=_configuration,
            **kwargs,
        )
