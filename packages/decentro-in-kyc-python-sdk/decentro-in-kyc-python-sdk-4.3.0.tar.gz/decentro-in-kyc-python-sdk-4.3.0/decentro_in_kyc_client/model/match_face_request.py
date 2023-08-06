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


class MatchFaceRequest(
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
        }
        
        class properties:
            
            
            class reference_id(
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
            image1 = schemas.BinarySchema
            image2 = schemas.BinarySchema
            threshold = schemas.IntSchema
            image1_url = schemas.StrSchema
            image2_url = schemas.StrSchema
            __annotations__ = {
                "reference_id": reference_id,
                "consent": consent,
                "consent_purpose": consent_purpose,
                "image1": image1,
                "image2": image2,
                "threshold": threshold,
                "image1_url": image1_url,
                "image2_url": image2_url,
            }
    
    reference_id: MetaOapg.properties.reference_id
    consent: MetaOapg.properties.consent
    consent_purpose: MetaOapg.properties.consent_purpose
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reference_id"]) -> MetaOapg.properties.reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["consent"]) -> MetaOapg.properties.consent: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["consent_purpose"]) -> MetaOapg.properties.consent_purpose: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["image1"]) -> MetaOapg.properties.image1: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["image2"]) -> MetaOapg.properties.image2: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["threshold"]) -> MetaOapg.properties.threshold: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["image1_url"]) -> MetaOapg.properties.image1_url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["image2_url"]) -> MetaOapg.properties.image2_url: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["reference_id", "consent", "consent_purpose", "image1", "image2", "threshold", "image1_url", "image2_url", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reference_id"]) -> MetaOapg.properties.reference_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["consent"]) -> MetaOapg.properties.consent: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["consent_purpose"]) -> MetaOapg.properties.consent_purpose: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["image1"]) -> typing.Union[MetaOapg.properties.image1, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["image2"]) -> typing.Union[MetaOapg.properties.image2, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["threshold"]) -> typing.Union[MetaOapg.properties.threshold, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["image1_url"]) -> typing.Union[MetaOapg.properties.image1_url, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["image2_url"]) -> typing.Union[MetaOapg.properties.image2_url, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["reference_id", "consent", "consent_purpose", "image1", "image2", "threshold", "image1_url", "image2_url", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        reference_id: typing.Union[MetaOapg.properties.reference_id, str, ],
        consent: typing.Union[MetaOapg.properties.consent, str, ],
        consent_purpose: typing.Union[MetaOapg.properties.consent_purpose, str, ],
        image1: typing.Union[MetaOapg.properties.image1, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        image2: typing.Union[MetaOapg.properties.image2, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        threshold: typing.Union[MetaOapg.properties.threshold, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        image1_url: typing.Union[MetaOapg.properties.image1_url, str, schemas.Unset] = schemas.unset,
        image2_url: typing.Union[MetaOapg.properties.image2_url, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'MatchFaceRequest':
        return super().__new__(
            cls,
            *args,
            reference_id=reference_id,
            consent=consent,
            consent_purpose=consent_purpose,
            image1=image1,
            image2=image2,
            threshold=threshold,
            image1_url=image1_url,
            image2_url=image2_url,
            _configuration=_configuration,
            **kwargs,
        )
