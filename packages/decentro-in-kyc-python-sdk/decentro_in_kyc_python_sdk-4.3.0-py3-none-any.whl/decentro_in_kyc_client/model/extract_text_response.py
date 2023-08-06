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


class ExtractTextResponse(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        
        class properties:
            ocrStatus = schemas.StrSchema
            status = schemas.StrSchema
            message = schemas.StrSchema
            
            
            class ocrResult(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        cardNo = schemas.StrSchema
                        dateInfo = schemas.StrSchema
                        dateType = schemas.StrSchema
                        fatherName = schemas.StrSchema
                        name = schemas.StrSchema
                        gender = schemas.StrSchema
                        vid = schemas.StrSchema
                        address = schemas.StrSchema
                        sonOf = schemas.StrSchema
                        husbandOf = schemas.StrSchema
                        __annotations__ = {
                            "cardNo": cardNo,
                            "dateInfo": dateInfo,
                            "dateType": dateType,
                            "fatherName": fatherName,
                            "name": name,
                            "gender": gender,
                            "vid": vid,
                            "address": address,
                            "sonOf": sonOf,
                            "husbandOf": husbandOf,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["cardNo"]) -> MetaOapg.properties.cardNo: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["dateInfo"]) -> MetaOapg.properties.dateInfo: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["dateType"]) -> MetaOapg.properties.dateType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["fatherName"]) -> MetaOapg.properties.fatherName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["gender"]) -> MetaOapg.properties.gender: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["vid"]) -> MetaOapg.properties.vid: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["sonOf"]) -> MetaOapg.properties.sonOf: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["husbandOf"]) -> MetaOapg.properties.husbandOf: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["cardNo", "dateInfo", "dateType", "fatherName", "name", "gender", "vid", "address", "sonOf", "husbandOf", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["cardNo"]) -> typing.Union[MetaOapg.properties.cardNo, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["dateInfo"]) -> typing.Union[MetaOapg.properties.dateInfo, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["dateType"]) -> typing.Union[MetaOapg.properties.dateType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["fatherName"]) -> typing.Union[MetaOapg.properties.fatherName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["gender"]) -> typing.Union[MetaOapg.properties.gender, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["vid"]) -> typing.Union[MetaOapg.properties.vid, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["sonOf"]) -> typing.Union[MetaOapg.properties.sonOf, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["husbandOf"]) -> typing.Union[MetaOapg.properties.husbandOf, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["cardNo", "dateInfo", "dateType", "fatherName", "name", "gender", "vid", "address", "sonOf", "husbandOf", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, ],
                    cardNo: typing.Union[MetaOapg.properties.cardNo, str, schemas.Unset] = schemas.unset,
                    dateInfo: typing.Union[MetaOapg.properties.dateInfo, str, schemas.Unset] = schemas.unset,
                    dateType: typing.Union[MetaOapg.properties.dateType, str, schemas.Unset] = schemas.unset,
                    fatherName: typing.Union[MetaOapg.properties.fatherName, str, schemas.Unset] = schemas.unset,
                    name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
                    gender: typing.Union[MetaOapg.properties.gender, str, schemas.Unset] = schemas.unset,
                    vid: typing.Union[MetaOapg.properties.vid, str, schemas.Unset] = schemas.unset,
                    address: typing.Union[MetaOapg.properties.address, str, schemas.Unset] = schemas.unset,
                    sonOf: typing.Union[MetaOapg.properties.sonOf, str, schemas.Unset] = schemas.unset,
                    husbandOf: typing.Union[MetaOapg.properties.husbandOf, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'ocrResult':
                    return super().__new__(
                        cls,
                        *args,
                        cardNo=cardNo,
                        dateInfo=dateInfo,
                        dateType=dateType,
                        fatherName=fatherName,
                        name=name,
                        gender=gender,
                        vid=vid,
                        address=address,
                        sonOf=sonOf,
                        husbandOf=husbandOf,
                        _configuration=_configuration,
                        **kwargs,
                    )
            responseCode = schemas.StrSchema
            requestTimestamp = schemas.StrSchema
            responseTimestamp = schemas.StrSchema
            decentroTxnId = schemas.StrSchema
            __annotations__ = {
                "ocrStatus": ocrStatus,
                "status": status,
                "message": message,
                "ocrResult": ocrResult,
                "responseCode": responseCode,
                "requestTimestamp": requestTimestamp,
                "responseTimestamp": responseTimestamp,
                "decentroTxnId": decentroTxnId,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ocrStatus"]) -> MetaOapg.properties.ocrStatus: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ocrResult"]) -> MetaOapg.properties.ocrResult: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseCode"]) -> MetaOapg.properties.responseCode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["requestTimestamp"]) -> MetaOapg.properties.requestTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseTimestamp"]) -> MetaOapg.properties.responseTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["decentroTxnId"]) -> MetaOapg.properties.decentroTxnId: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["ocrStatus", "status", "message", "ocrResult", "responseCode", "requestTimestamp", "responseTimestamp", "decentroTxnId", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ocrStatus"]) -> typing.Union[MetaOapg.properties.ocrStatus, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["message"]) -> typing.Union[MetaOapg.properties.message, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ocrResult"]) -> typing.Union[MetaOapg.properties.ocrResult, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseCode"]) -> typing.Union[MetaOapg.properties.responseCode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["requestTimestamp"]) -> typing.Union[MetaOapg.properties.requestTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseTimestamp"]) -> typing.Union[MetaOapg.properties.responseTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["decentroTxnId"]) -> typing.Union[MetaOapg.properties.decentroTxnId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["ocrStatus", "status", "message", "ocrResult", "responseCode", "requestTimestamp", "responseTimestamp", "decentroTxnId", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        ocrStatus: typing.Union[MetaOapg.properties.ocrStatus, str, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        message: typing.Union[MetaOapg.properties.message, str, schemas.Unset] = schemas.unset,
        ocrResult: typing.Union[MetaOapg.properties.ocrResult, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        responseCode: typing.Union[MetaOapg.properties.responseCode, str, schemas.Unset] = schemas.unset,
        requestTimestamp: typing.Union[MetaOapg.properties.requestTimestamp, str, schemas.Unset] = schemas.unset,
        responseTimestamp: typing.Union[MetaOapg.properties.responseTimestamp, str, schemas.Unset] = schemas.unset,
        decentroTxnId: typing.Union[MetaOapg.properties.decentroTxnId, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExtractTextResponse':
        return super().__new__(
            cls,
            *args,
            ocrStatus=ocrStatus,
            status=status,
            message=message,
            ocrResult=ocrResult,
            responseCode=responseCode,
            requestTimestamp=requestTimestamp,
            responseTimestamp=responseTimestamp,
            decentroTxnId=decentroTxnId,
            _configuration=_configuration,
            **kwargs,
        )
