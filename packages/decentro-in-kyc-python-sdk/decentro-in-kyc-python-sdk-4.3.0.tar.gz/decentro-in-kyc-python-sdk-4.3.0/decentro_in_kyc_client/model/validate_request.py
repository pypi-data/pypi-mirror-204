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


class ValidateRequest(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        required = {
            "id_number",
            "reference_id",
            "consent",
            "consent_purpose",
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
            
            
            class id_number(
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
            dob = schemas.StrSchema
            name = schemas.StrSchema
            __annotations__ = {
                "reference_id": reference_id,
                "document_type": document_type,
                "id_number": id_number,
                "consent": consent,
                "consent_purpose": consent_purpose,
                "dob": dob,
                "name": name,
            }
    
    id_number: MetaOapg.properties.id_number
    reference_id: MetaOapg.properties.reference_id
    consent: MetaOapg.properties.consent
    consent_purpose: MetaOapg.properties.consent_purpose
    document_type: MetaOapg.properties.document_type
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reference_id"]) -> MetaOapg.properties.reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document_type"]) -> MetaOapg.properties.document_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id_number"]) -> MetaOapg.properties.id_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["consent"]) -> MetaOapg.properties.consent: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["consent_purpose"]) -> MetaOapg.properties.consent_purpose: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dob"]) -> MetaOapg.properties.dob: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["reference_id", "document_type", "id_number", "consent", "consent_purpose", "dob", "name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reference_id"]) -> MetaOapg.properties.reference_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document_type"]) -> MetaOapg.properties.document_type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id_number"]) -> MetaOapg.properties.id_number: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["consent"]) -> MetaOapg.properties.consent: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["consent_purpose"]) -> MetaOapg.properties.consent_purpose: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dob"]) -> typing.Union[MetaOapg.properties.dob, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["reference_id", "document_type", "id_number", "consent", "consent_purpose", "dob", "name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        id_number: typing.Union[MetaOapg.properties.id_number, str, ],
        reference_id: typing.Union[MetaOapg.properties.reference_id, str, ],
        consent: typing.Union[MetaOapg.properties.consent, str, ],
        consent_purpose: typing.Union[MetaOapg.properties.consent_purpose, str, ],
        document_type: typing.Union[MetaOapg.properties.document_type, str, ],
        dob: typing.Union[MetaOapg.properties.dob, str, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ValidateRequest':
        return super().__new__(
            cls,
            *args,
            id_number=id_number,
            reference_id=reference_id,
            consent=consent,
            consent_purpose=consent_purpose,
            document_type=document_type,
            dob=dob,
            name=name,
            _configuration=_configuration,
            **kwargs,
        )
