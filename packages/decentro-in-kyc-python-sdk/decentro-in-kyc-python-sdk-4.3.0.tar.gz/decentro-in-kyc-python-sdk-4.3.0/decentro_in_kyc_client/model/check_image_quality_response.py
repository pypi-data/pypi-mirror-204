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


class CheckImageQualityResponse(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        
        class properties:
            decentroTxnId = schemas.StrSchema
            status = schemas.StrSchema
            responseCode = schemas.StrSchema
            message = schemas.StrSchema
            
            
            class data(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        
                        
                        class imageQuality(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    summary = schemas.StrSchema
                                    
                                    
                                    class qualityScores(
                                        schemas.DictSchema
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            
                                            class properties:
                                                
                                                
                                                class textQuality(
                                                    schemas.DictSchema
                                                ):
                                                
                                                
                                                    class MetaOapg:
                                                        
                                                        class properties:
                                                            valid = schemas.StrSchema
                                                            score = schemas.NumberSchema
                                                            __annotations__ = {
                                                                "valid": valid,
                                                                "score": score,
                                                            }
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["valid"]) -> MetaOapg.properties.valid: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                                    
                                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        # dict_instance[name] accessor
                                                        return super().__getitem__(name)
                                                    
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["valid"]) -> typing.Union[MetaOapg.properties.valid, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["score"]) -> typing.Union[MetaOapg.properties.score, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                                    
                                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        return super().get_item_oapg(name)
                                                    
                                                
                                                    def __new__(
                                                        cls,
                                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                                        valid: typing.Union[MetaOapg.properties.valid, str, schemas.Unset] = schemas.unset,
                                                        score: typing.Union[MetaOapg.properties.score, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                                    ) -> 'textQuality':
                                                        return super().__new__(
                                                            cls,
                                                            *args,
                                                            valid=valid,
                                                            score=score,
                                                            _configuration=_configuration,
                                                            **kwargs,
                                                        )
                                                
                                                
                                                class sharpness(
                                                    schemas.DictSchema
                                                ):
                                                
                                                
                                                    class MetaOapg:
                                                        
                                                        class properties:
                                                            valid = schemas.StrSchema
                                                            score = schemas.NumberSchema
                                                            __annotations__ = {
                                                                "valid": valid,
                                                                "score": score,
                                                            }
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["valid"]) -> MetaOapg.properties.valid: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                                    
                                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        # dict_instance[name] accessor
                                                        return super().__getitem__(name)
                                                    
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["valid"]) -> typing.Union[MetaOapg.properties.valid, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["score"]) -> typing.Union[MetaOapg.properties.score, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                                    
                                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        return super().get_item_oapg(name)
                                                    
                                                
                                                    def __new__(
                                                        cls,
                                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                                        valid: typing.Union[MetaOapg.properties.valid, str, schemas.Unset] = schemas.unset,
                                                        score: typing.Union[MetaOapg.properties.score, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                                    ) -> 'sharpness':
                                                        return super().__new__(
                                                            cls,
                                                            *args,
                                                            valid=valid,
                                                            score=score,
                                                            _configuration=_configuration,
                                                            **kwargs,
                                                        )
                                                
                                                
                                                class brightness(
                                                    schemas.DictSchema
                                                ):
                                                
                                                
                                                    class MetaOapg:
                                                        
                                                        class properties:
                                                            valid = schemas.StrSchema
                                                            score = schemas.NumberSchema
                                                            __annotations__ = {
                                                                "valid": valid,
                                                                "score": score,
                                                            }
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["valid"]) -> MetaOapg.properties.valid: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                                    
                                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        # dict_instance[name] accessor
                                                        return super().__getitem__(name)
                                                    
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["valid"]) -> typing.Union[MetaOapg.properties.valid, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["score"]) -> typing.Union[MetaOapg.properties.score, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                                    
                                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        return super().get_item_oapg(name)
                                                    
                                                
                                                    def __new__(
                                                        cls,
                                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                                        valid: typing.Union[MetaOapg.properties.valid, str, schemas.Unset] = schemas.unset,
                                                        score: typing.Union[MetaOapg.properties.score, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                                    ) -> 'brightness':
                                                        return super().__new__(
                                                            cls,
                                                            *args,
                                                            valid=valid,
                                                            score=score,
                                                            _configuration=_configuration,
                                                            **kwargs,
                                                        )
                                                
                                                
                                                class compressionQuality(
                                                    schemas.DictSchema
                                                ):
                                                
                                                
                                                    class MetaOapg:
                                                        
                                                        class properties:
                                                            valid = schemas.StrSchema
                                                            score = schemas.NumberSchema
                                                            __annotations__ = {
                                                                "valid": valid,
                                                                "score": score,
                                                            }
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["valid"]) -> MetaOapg.properties.valid: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
                                                    
                                                    @typing.overload
                                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                                    
                                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        # dict_instance[name] accessor
                                                        return super().__getitem__(name)
                                                    
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["valid"]) -> typing.Union[MetaOapg.properties.valid, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: typing_extensions.Literal["score"]) -> typing.Union[MetaOapg.properties.score, schemas.Unset]: ...
                                                    
                                                    @typing.overload
                                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                                    
                                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["valid", "score", ], str]):
                                                        return super().get_item_oapg(name)
                                                    
                                                
                                                    def __new__(
                                                        cls,
                                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                                        valid: typing.Union[MetaOapg.properties.valid, str, schemas.Unset] = schemas.unset,
                                                        score: typing.Union[MetaOapg.properties.score, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                                    ) -> 'compressionQuality':
                                                        return super().__new__(
                                                            cls,
                                                            *args,
                                                            valid=valid,
                                                            score=score,
                                                            _configuration=_configuration,
                                                            **kwargs,
                                                        )
                                                __annotations__ = {
                                                    "textQuality": textQuality,
                                                    "sharpness": sharpness,
                                                    "brightness": brightness,
                                                    "compressionQuality": compressionQuality,
                                                }
                                        
                                        @typing.overload
                                        def __getitem__(self, name: typing_extensions.Literal["textQuality"]) -> MetaOapg.properties.textQuality: ...
                                        
                                        @typing.overload
                                        def __getitem__(self, name: typing_extensions.Literal["sharpness"]) -> MetaOapg.properties.sharpness: ...
                                        
                                        @typing.overload
                                        def __getitem__(self, name: typing_extensions.Literal["brightness"]) -> MetaOapg.properties.brightness: ...
                                        
                                        @typing.overload
                                        def __getitem__(self, name: typing_extensions.Literal["compressionQuality"]) -> MetaOapg.properties.compressionQuality: ...
                                        
                                        @typing.overload
                                        def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                        
                                        def __getitem__(self, name: typing.Union[typing_extensions.Literal["textQuality", "sharpness", "brightness", "compressionQuality", ], str]):
                                            # dict_instance[name] accessor
                                            return super().__getitem__(name)
                                        
                                        
                                        @typing.overload
                                        def get_item_oapg(self, name: typing_extensions.Literal["textQuality"]) -> typing.Union[MetaOapg.properties.textQuality, schemas.Unset]: ...
                                        
                                        @typing.overload
                                        def get_item_oapg(self, name: typing_extensions.Literal["sharpness"]) -> typing.Union[MetaOapg.properties.sharpness, schemas.Unset]: ...
                                        
                                        @typing.overload
                                        def get_item_oapg(self, name: typing_extensions.Literal["brightness"]) -> typing.Union[MetaOapg.properties.brightness, schemas.Unset]: ...
                                        
                                        @typing.overload
                                        def get_item_oapg(self, name: typing_extensions.Literal["compressionQuality"]) -> typing.Union[MetaOapg.properties.compressionQuality, schemas.Unset]: ...
                                        
                                        @typing.overload
                                        def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                        
                                        def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["textQuality", "sharpness", "brightness", "compressionQuality", ], str]):
                                            return super().get_item_oapg(name)
                                        
                                    
                                        def __new__(
                                            cls,
                                            *args: typing.Union[dict, frozendict.frozendict, ],
                                            textQuality: typing.Union[MetaOapg.properties.textQuality, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                                            sharpness: typing.Union[MetaOapg.properties.sharpness, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                                            brightness: typing.Union[MetaOapg.properties.brightness, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                                            compressionQuality: typing.Union[MetaOapg.properties.compressionQuality, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                            **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                        ) -> 'qualityScores':
                                            return super().__new__(
                                                cls,
                                                *args,
                                                textQuality=textQuality,
                                                sharpness=sharpness,
                                                brightness=brightness,
                                                compressionQuality=compressionQuality,
                                                _configuration=_configuration,
                                                **kwargs,
                                            )
                                    extractionQuality = schemas.StrSchema
                                    score = schemas.NumberSchema
                                    msg = schemas.StrSchema
                                    __annotations__ = {
                                        "summary": summary,
                                        "qualityScores": qualityScores,
                                        "extractionQuality": extractionQuality,
                                        "score": score,
                                        "msg": msg,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["summary"]) -> MetaOapg.properties.summary: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["qualityScores"]) -> MetaOapg.properties.qualityScores: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["extractionQuality"]) -> MetaOapg.properties.extractionQuality: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["msg"]) -> MetaOapg.properties.msg: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["summary", "qualityScores", "extractionQuality", "score", "msg", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["summary"]) -> typing.Union[MetaOapg.properties.summary, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["qualityScores"]) -> typing.Union[MetaOapg.properties.qualityScores, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["extractionQuality"]) -> typing.Union[MetaOapg.properties.extractionQuality, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["score"]) -> typing.Union[MetaOapg.properties.score, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["msg"]) -> typing.Union[MetaOapg.properties.msg, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["summary", "qualityScores", "extractionQuality", "score", "msg", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                summary: typing.Union[MetaOapg.properties.summary, str, schemas.Unset] = schemas.unset,
                                qualityScores: typing.Union[MetaOapg.properties.qualityScores, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                                extractionQuality: typing.Union[MetaOapg.properties.extractionQuality, str, schemas.Unset] = schemas.unset,
                                score: typing.Union[MetaOapg.properties.score, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                                msg: typing.Union[MetaOapg.properties.msg, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'imageQuality':
                                return super().__new__(
                                    cls,
                                    *args,
                                    summary=summary,
                                    qualityScores=qualityScores,
                                    extractionQuality=extractionQuality,
                                    score=score,
                                    msg=msg,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        __annotations__ = {
                            "imageQuality": imageQuality,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["imageQuality"]) -> MetaOapg.properties.imageQuality: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["imageQuality", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["imageQuality"]) -> typing.Union[MetaOapg.properties.imageQuality, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["imageQuality", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, ],
                    imageQuality: typing.Union[MetaOapg.properties.imageQuality, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'data':
                    return super().__new__(
                        cls,
                        *args,
                        imageQuality=imageQuality,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "decentroTxnId": decentroTxnId,
                "status": status,
                "responseCode": responseCode,
                "message": message,
                "data": data,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["decentroTxnId"]) -> MetaOapg.properties.decentroTxnId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseCode"]) -> MetaOapg.properties.responseCode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["decentroTxnId", "status", "responseCode", "message", "data", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["decentroTxnId"]) -> typing.Union[MetaOapg.properties.decentroTxnId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseCode"]) -> typing.Union[MetaOapg.properties.responseCode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["message"]) -> typing.Union[MetaOapg.properties.message, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> typing.Union[MetaOapg.properties.data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["decentroTxnId", "status", "responseCode", "message", "data", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        decentroTxnId: typing.Union[MetaOapg.properties.decentroTxnId, str, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        responseCode: typing.Union[MetaOapg.properties.responseCode, str, schemas.Unset] = schemas.unset,
        message: typing.Union[MetaOapg.properties.message, str, schemas.Unset] = schemas.unset,
        data: typing.Union[MetaOapg.properties.data, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CheckImageQualityResponse':
        return super().__new__(
            cls,
            *args,
            decentroTxnId=decentroTxnId,
            status=status,
            responseCode=responseCode,
            message=message,
            data=data,
            _configuration=_configuration,
            **kwargs,
        )
