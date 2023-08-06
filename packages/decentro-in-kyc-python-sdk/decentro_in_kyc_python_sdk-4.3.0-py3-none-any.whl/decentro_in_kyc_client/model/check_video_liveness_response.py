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


class CheckVideoLivenessResponse(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        
        class properties:
            
            
            class data(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        confidence = schemas.StrSchema
                        status = schemas.StrSchema
                        __annotations__ = {
                            "confidence": confidence,
                            "status": status,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["confidence"]) -> MetaOapg.properties.confidence: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["confidence", "status", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["confidence"]) -> typing.Union[MetaOapg.properties.confidence, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["confidence", "status", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, ],
                    confidence: typing.Union[MetaOapg.properties.confidence, str, schemas.Unset] = schemas.unset,
                    status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'data':
                    return super().__new__(
                        cls,
                        *args,
                        confidence=confidence,
                        status=status,
                        _configuration=_configuration,
                        **kwargs,
                    )
            decentroTxnId = schemas.StrSchema
            message = schemas.StrSchema
            responseCode = schemas.StrSchema
            status = schemas.StrSchema
            __annotations__ = {
                "data": data,
                "decentroTxnId": decentroTxnId,
                "message": message,
                "responseCode": responseCode,
                "status": status,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["decentroTxnId"]) -> MetaOapg.properties.decentroTxnId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseCode"]) -> MetaOapg.properties.responseCode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["data", "decentroTxnId", "message", "responseCode", "status", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> typing.Union[MetaOapg.properties.data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["decentroTxnId"]) -> typing.Union[MetaOapg.properties.decentroTxnId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["message"]) -> typing.Union[MetaOapg.properties.message, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseCode"]) -> typing.Union[MetaOapg.properties.responseCode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["data", "decentroTxnId", "message", "responseCode", "status", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        data: typing.Union[MetaOapg.properties.data, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        decentroTxnId: typing.Union[MetaOapg.properties.decentroTxnId, str, schemas.Unset] = schemas.unset,
        message: typing.Union[MetaOapg.properties.message, str, schemas.Unset] = schemas.unset,
        responseCode: typing.Union[MetaOapg.properties.responseCode, str, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CheckVideoLivenessResponse':
        return super().__new__(
            cls,
            *args,
            data=data,
            decentroTxnId=decentroTxnId,
            message=message,
            responseCode=responseCode,
            status=status,
            _configuration=_configuration,
            **kwargs,
        )
