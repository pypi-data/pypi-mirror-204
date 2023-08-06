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


class Validate400Response(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        
        class properties:
            status = schemas.StrSchema
            kycStatus = schemas.StrSchema
            
            
            class error(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        message = schemas.StrSchema
                        responseCode = schemas.StrSchema
                        __annotations__ = {
                            "message": message,
                            "responseCode": responseCode,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["responseCode"]) -> MetaOapg.properties.responseCode: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["message", "responseCode", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["message"]) -> typing.Union[MetaOapg.properties.message, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["responseCode"]) -> typing.Union[MetaOapg.properties.responseCode, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["message", "responseCode", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, ],
                    message: typing.Union[MetaOapg.properties.message, str, schemas.Unset] = schemas.unset,
                    responseCode: typing.Union[MetaOapg.properties.responseCode, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'error':
                    return super().__new__(
                        cls,
                        *args,
                        message=message,
                        responseCode=responseCode,
                        _configuration=_configuration,
                        **kwargs,
                    )
            requestTimestamp = schemas.StrSchema
            responseTimestamp = schemas.StrSchema
            decentroTxnId = schemas.StrSchema
            __annotations__ = {
                "status": status,
                "kycStatus": kycStatus,
                "error": error,
                "requestTimestamp": requestTimestamp,
                "responseTimestamp": responseTimestamp,
                "decentroTxnId": decentroTxnId,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["kycStatus"]) -> MetaOapg.properties.kycStatus: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["error"]) -> MetaOapg.properties.error: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["requestTimestamp"]) -> MetaOapg.properties.requestTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseTimestamp"]) -> MetaOapg.properties.responseTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["decentroTxnId"]) -> MetaOapg.properties.decentroTxnId: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["status", "kycStatus", "error", "requestTimestamp", "responseTimestamp", "decentroTxnId", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["kycStatus"]) -> typing.Union[MetaOapg.properties.kycStatus, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["error"]) -> typing.Union[MetaOapg.properties.error, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["requestTimestamp"]) -> typing.Union[MetaOapg.properties.requestTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseTimestamp"]) -> typing.Union[MetaOapg.properties.responseTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["decentroTxnId"]) -> typing.Union[MetaOapg.properties.decentroTxnId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["status", "kycStatus", "error", "requestTimestamp", "responseTimestamp", "decentroTxnId", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        kycStatus: typing.Union[MetaOapg.properties.kycStatus, str, schemas.Unset] = schemas.unset,
        error: typing.Union[MetaOapg.properties.error, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        requestTimestamp: typing.Union[MetaOapg.properties.requestTimestamp, str, schemas.Unset] = schemas.unset,
        responseTimestamp: typing.Union[MetaOapg.properties.responseTimestamp, str, schemas.Unset] = schemas.unset,
        decentroTxnId: typing.Union[MetaOapg.properties.decentroTxnId, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Validate400Response':
        return super().__new__(
            cls,
            *args,
            status=status,
            kycStatus=kycStatus,
            error=error,
            requestTimestamp=requestTimestamp,
            responseTimestamp=responseTimestamp,
            decentroTxnId=decentroTxnId,
            _configuration=_configuration,
            **kwargs,
        )
