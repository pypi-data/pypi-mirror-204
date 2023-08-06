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


class ValidateResponse(
    schemas.DictSchema
):
    """
    This class is auto generated
    """


    class MetaOapg:
        
        class properties:
            kycStatus = schemas.StrSchema
            status = schemas.StrSchema
            message = schemas.StrSchema
            
            
            class kycResult(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        idNumber = schemas.StrSchema
                        idStatus = schemas.StrSchema
                        name = schemas.StrSchema
                        licenseType = schemas.StrSchema
                        entityName = schemas.StrSchema
                        status = schemas.StrSchema
                        
                        
                        class premissesAddress(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    district = schemas.StrSchema
                                    address = schemas.StrSchema
                                    state = schemas.StrSchema
                                    pincode = schemas.StrSchema
                                    __annotations__ = {
                                        "district": district,
                                        "address": address,
                                        "state": state,
                                        "pincode": pincode,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["district"]) -> MetaOapg.properties.district: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["pincode"]) -> MetaOapg.properties.pincode: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["district", "address", "state", "pincode", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["district"]) -> typing.Union[MetaOapg.properties.district, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union[MetaOapg.properties.state, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["pincode"]) -> typing.Union[MetaOapg.properties.pincode, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["district", "address", "state", "pincode", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                district: typing.Union[MetaOapg.properties.district, str, schemas.Unset] = schemas.unset,
                                address: typing.Union[MetaOapg.properties.address, str, schemas.Unset] = schemas.unset,
                                state: typing.Union[MetaOapg.properties.state, str, schemas.Unset] = schemas.unset,
                                pincode: typing.Union[MetaOapg.properties.pincode, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'premissesAddress':
                                return super().__new__(
                                    cls,
                                    *args,
                                    district=district,
                                    address=address,
                                    state=state,
                                    pincode=pincode,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        
                        
                        class products(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                
                                class items(
                                    schemas.DictSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        
                                        class properties:
                                            slNo = schemas.StrSchema
                                            foodProductCategory = schemas.StrSchema
                                            __annotations__ = {
                                                "slNo": slNo,
                                                "foodProductCategory": foodProductCategory,
                                            }
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["slNo"]) -> MetaOapg.properties.slNo: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["foodProductCategory"]) -> MetaOapg.properties.foodProductCategory: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                    
                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["slNo", "foodProductCategory", ], str]):
                                        # dict_instance[name] accessor
                                        return super().__getitem__(name)
                                    
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["slNo"]) -> typing.Union[MetaOapg.properties.slNo, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["foodProductCategory"]) -> typing.Union[MetaOapg.properties.foodProductCategory, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                    
                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["slNo", "foodProductCategory", ], str]):
                                        return super().get_item_oapg(name)
                                    
                                
                                    def __new__(
                                        cls,
                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                        slNo: typing.Union[MetaOapg.properties.slNo, str, schemas.Unset] = schemas.unset,
                                        foodProductCategory: typing.Union[MetaOapg.properties.foodProductCategory, str, schemas.Unset] = schemas.unset,
                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                    ) -> 'items':
                                        return super().__new__(
                                            cls,
                                            *args,
                                            slNo=slNo,
                                            foodProductCategory=foodProductCategory,
                                            _configuration=_configuration,
                                            **kwargs,
                                        )
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'products':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        
                        
                        class address(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    
                                    
                                    class district(
                                        schemas.ListSchema
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            items = schemas.StrSchema
                                    
                                        def __new__(
                                            cls,
                                            arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                        ) -> 'district':
                                            return super().__new__(
                                                cls,
                                                arg,
                                                _configuration=_configuration,
                                            )
                                    
                                        def __getitem__(self, i: int) -> MetaOapg.items:
                                            return super().__getitem__(i)
                                    
                                    
                                    class state(
                                        schemas.ComposedSchema,
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            
                                            
                                            class one_of_0(
                                                schemas.ListSchema
                                            ):
                                            
                                            
                                                class MetaOapg:
                                                    
                                                    
                                                    class items(
                                                        schemas.ListSchema
                                                    ):
                                                    
                                                    
                                                        class MetaOapg:
                                                            items = schemas.StrSchema
                                                    
                                                        def __new__(
                                                            cls,
                                                            arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                                        ) -> 'items':
                                                            return super().__new__(
                                                                cls,
                                                                arg,
                                                                _configuration=_configuration,
                                                            )
                                                    
                                                        def __getitem__(self, i: int) -> MetaOapg.items:
                                                            return super().__getitem__(i)
                                            
                                                def __new__(
                                                    cls,
                                                    arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, list, tuple, ]], typing.List[typing.Union[MetaOapg.items, list, tuple, ]]],
                                                    _configuration: typing.Optional[schemas.Configuration] = None,
                                                ) -> 'one_of_0':
                                                    return super().__new__(
                                                        cls,
                                                        arg,
                                                        _configuration=_configuration,
                                                    )
                                            
                                                def __getitem__(self, i: int) -> MetaOapg.items:
                                                    return super().__getitem__(i)
                                            one_of_1 = schemas.StrSchema
                                            
                                            @classmethod
                                            @functools.lru_cache()
                                            def one_of(cls):
                                                # we need this here to make our import statements work
                                                # we must store _composed_schemas in here so the code is only run
                                                # when we invoke this method. If we kept this at the class
                                                # level we would get an error because the class level
                                                # code would be run when this module is imported, and these composed
                                                # classes don't exist yet because their module has not finished
                                                # loading
                                                return [
                                                    cls.one_of_0,
                                                    cls.one_of_1,
                                                ]
                                    
                                    
                                        def __new__(
                                            cls,
                                            *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                            **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                        ) -> 'state':
                                            return super().__new__(
                                                cls,
                                                *args,
                                                _configuration=_configuration,
                                                **kwargs,
                                            )
                                    
                                    
                                    class city(
                                        schemas.ListSchema
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            items = schemas.StrSchema
                                    
                                        def __new__(
                                            cls,
                                            arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                        ) -> 'city':
                                            return super().__new__(
                                                cls,
                                                arg,
                                                _configuration=_configuration,
                                            )
                                    
                                        def __getitem__(self, i: int) -> MetaOapg.items:
                                            return super().__getitem__(i)
                                    pincode = schemas.StrSchema
                                    
                                    
                                    class country(
                                        schemas.ListSchema
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            items = schemas.StrSchema
                                    
                                        def __new__(
                                            cls,
                                            arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                        ) -> 'country':
                                            return super().__new__(
                                                cls,
                                                arg,
                                                _configuration=_configuration,
                                            )
                                    
                                        def __getitem__(self, i: int) -> MetaOapg.items:
                                            return super().__getitem__(i)
                                    addressLine = schemas.StrSchema
                                    districtCode = schemas.StrSchema
                                    districtName = schemas.StrSchema
                                    districtNameVernacular = schemas.StrSchema
                                    stateCode = schemas.StrSchema
                                    __annotations__ = {
                                        "district": district,
                                        "state": state,
                                        "city": city,
                                        "pincode": pincode,
                                        "country": country,
                                        "addressLine": addressLine,
                                        "districtCode": districtCode,
                                        "districtName": districtName,
                                        "districtNameVernacular": districtNameVernacular,
                                        "stateCode": stateCode,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["district"]) -> MetaOapg.properties.district: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["city"]) -> MetaOapg.properties.city: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["pincode"]) -> MetaOapg.properties.pincode: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["country"]) -> MetaOapg.properties.country: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["addressLine"]) -> MetaOapg.properties.addressLine: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["districtCode"]) -> MetaOapg.properties.districtCode: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["districtName"]) -> MetaOapg.properties.districtName: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["districtNameVernacular"]) -> MetaOapg.properties.districtNameVernacular: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["stateCode"]) -> MetaOapg.properties.stateCode: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["district", "state", "city", "pincode", "country", "addressLine", "districtCode", "districtName", "districtNameVernacular", "stateCode", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["district"]) -> typing.Union[MetaOapg.properties.district, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union[MetaOapg.properties.state, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["city"]) -> typing.Union[MetaOapg.properties.city, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["pincode"]) -> typing.Union[MetaOapg.properties.pincode, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["country"]) -> typing.Union[MetaOapg.properties.country, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["addressLine"]) -> typing.Union[MetaOapg.properties.addressLine, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["districtCode"]) -> typing.Union[MetaOapg.properties.districtCode, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["districtName"]) -> typing.Union[MetaOapg.properties.districtName, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["districtNameVernacular"]) -> typing.Union[MetaOapg.properties.districtNameVernacular, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["stateCode"]) -> typing.Union[MetaOapg.properties.stateCode, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["district", "state", "city", "pincode", "country", "addressLine", "districtCode", "districtName", "districtNameVernacular", "stateCode", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                district: typing.Union[MetaOapg.properties.district, list, tuple, schemas.Unset] = schemas.unset,
                                state: typing.Union[MetaOapg.properties.state, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
                                city: typing.Union[MetaOapg.properties.city, list, tuple, schemas.Unset] = schemas.unset,
                                pincode: typing.Union[MetaOapg.properties.pincode, str, schemas.Unset] = schemas.unset,
                                country: typing.Union[MetaOapg.properties.country, list, tuple, schemas.Unset] = schemas.unset,
                                addressLine: typing.Union[MetaOapg.properties.addressLine, str, schemas.Unset] = schemas.unset,
                                districtCode: typing.Union[MetaOapg.properties.districtCode, str, schemas.Unset] = schemas.unset,
                                districtName: typing.Union[MetaOapg.properties.districtName, str, schemas.Unset] = schemas.unset,
                                districtNameVernacular: typing.Union[MetaOapg.properties.districtNameVernacular, str, schemas.Unset] = schemas.unset,
                                stateCode: typing.Union[MetaOapg.properties.stateCode, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'address':
                                return super().__new__(
                                    cls,
                                    *args,
                                    district=district,
                                    state=state,
                                    city=city,
                                    pincode=pincode,
                                    country=country,
                                    addressLine=addressLine,
                                    districtCode=districtCode,
                                    districtName=districtName,
                                    districtNameVernacular=districtNameVernacular,
                                    stateCode=stateCode,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        uamNumber = schemas.StrSchema
                        enterpriseName = schemas.StrSchema
                        majorActivity = schemas.StrSchema
                        socialCategory = schemas.StrSchema
                        enterpriseType = schemas.StrSchema
                        dateOfCommencement = schemas.StrSchema
                        district = schemas.StrSchema
                        state = schemas.StrSchema
                        appliedDate = schemas.StrSchema
                        modifiedDate = schemas.StrSchema
                        expiryDate = schemas.StrSchema
                        nic_2Digit = schemas.StrSchema
                        nic_4Digit = schemas.StrSchema
                        nic_5Digit = schemas.StrSchema
                        panStatus = schemas.StrSchema
                        lastName = schemas.StrSchema
                        firstName = schemas.StrSchema
                        fullName = schemas.StrSchema
                        idHolderTitle = schemas.StrSchema
                        idLastUpdated = schemas.StrSchema
                        aadhaarSeedingStatus = schemas.StrSchema
                        
                        
                        class addresses(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                
                                class items(
                                    schemas.DictSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        
                                        class properties:
                                            addressLine = schemas.StrSchema
                                            completeAddress = schemas.StrSchema
                                            country = schemas.StrSchema
                                            district = schemas.StrSchema
                                            pin = schemas.StrSchema
                                            state = schemas.StrSchema
                                            type = schemas.StrSchema
                                            __annotations__ = {
                                                "addressLine": addressLine,
                                                "completeAddress": completeAddress,
                                                "country": country,
                                                "district": district,
                                                "pin": pin,
                                                "state": state,
                                                "type": type,
                                            }
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["addressLine"]) -> MetaOapg.properties.addressLine: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["completeAddress"]) -> MetaOapg.properties.completeAddress: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["country"]) -> MetaOapg.properties.country: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["district"]) -> MetaOapg.properties.district: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["pin"]) -> MetaOapg.properties.pin: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                    
                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["addressLine", "completeAddress", "country", "district", "pin", "state", "type", ], str]):
                                        # dict_instance[name] accessor
                                        return super().__getitem__(name)
                                    
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["addressLine"]) -> typing.Union[MetaOapg.properties.addressLine, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["completeAddress"]) -> typing.Union[MetaOapg.properties.completeAddress, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["country"]) -> typing.Union[MetaOapg.properties.country, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["district"]) -> typing.Union[MetaOapg.properties.district, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["pin"]) -> typing.Union[MetaOapg.properties.pin, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union[MetaOapg.properties.state, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> typing.Union[MetaOapg.properties.type, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                    
                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["addressLine", "completeAddress", "country", "district", "pin", "state", "type", ], str]):
                                        return super().get_item_oapg(name)
                                    
                                
                                    def __new__(
                                        cls,
                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                        addressLine: typing.Union[MetaOapg.properties.addressLine, str, schemas.Unset] = schemas.unset,
                                        completeAddress: typing.Union[MetaOapg.properties.completeAddress, str, schemas.Unset] = schemas.unset,
                                        country: typing.Union[MetaOapg.properties.country, str, schemas.Unset] = schemas.unset,
                                        district: typing.Union[MetaOapg.properties.district, str, schemas.Unset] = schemas.unset,
                                        pin: typing.Union[MetaOapg.properties.pin, str, schemas.Unset] = schemas.unset,
                                        state: typing.Union[MetaOapg.properties.state, str, schemas.Unset] = schemas.unset,
                                        type: typing.Union[MetaOapg.properties.type, str, schemas.Unset] = schemas.unset,
                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                    ) -> 'items':
                                        return super().__new__(
                                            cls,
                                            *args,
                                            addressLine=addressLine,
                                            completeAddress=completeAddress,
                                            country=country,
                                            district=district,
                                            pin=pin,
                                            state=state,
                                            type=type,
                                            _configuration=_configuration,
                                            **kwargs,
                                        )
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'addresses':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        
                        
                        class allClassOfVehicle(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                
                                class items(
                                    schemas.DictSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        
                                        class properties:
                                            cov = schemas.StrSchema
                                            expiryDate = schemas.StrSchema
                                            issueDate = schemas.StrSchema
                                            covCategory = schemas.StrSchema
                                            __annotations__ = {
                                                "cov": cov,
                                                "expiryDate": expiryDate,
                                                "issueDate": issueDate,
                                                "covCategory": covCategory,
                                            }
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["cov"]) -> MetaOapg.properties.cov: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["expiryDate"]) -> MetaOapg.properties.expiryDate: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["issueDate"]) -> MetaOapg.properties.issueDate: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["covCategory"]) -> MetaOapg.properties.covCategory: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                    
                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["cov", "expiryDate", "issueDate", "covCategory", ], str]):
                                        # dict_instance[name] accessor
                                        return super().__getitem__(name)
                                    
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["cov"]) -> typing.Union[MetaOapg.properties.cov, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["expiryDate"]) -> typing.Union[MetaOapg.properties.expiryDate, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["issueDate"]) -> typing.Union[MetaOapg.properties.issueDate, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["covCategory"]) -> typing.Union[MetaOapg.properties.covCategory, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                    
                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["cov", "expiryDate", "issueDate", "covCategory", ], str]):
                                        return super().get_item_oapg(name)
                                    
                                
                                    def __new__(
                                        cls,
                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                        cov: typing.Union[MetaOapg.properties.cov, str, schemas.Unset] = schemas.unset,
                                        expiryDate: typing.Union[MetaOapg.properties.expiryDate, str, schemas.Unset] = schemas.unset,
                                        issueDate: typing.Union[MetaOapg.properties.issueDate, str, schemas.Unset] = schemas.unset,
                                        covCategory: typing.Union[MetaOapg.properties.covCategory, str, schemas.Unset] = schemas.unset,
                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                    ) -> 'items':
                                        return super().__new__(
                                            cls,
                                            *args,
                                            cov=cov,
                                            expiryDate=expiryDate,
                                            issueDate=issueDate,
                                            covCategory=covCategory,
                                            _configuration=_configuration,
                                            **kwargs,
                                        )
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'allClassOfVehicle':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        drivingLicenseNumber = schemas.StrSchema
                        dateOfBirth = schemas.StrSchema
                        endorseDate = schemas.StrSchema
                        endorseNumber = schemas.StrSchema
                        fatherOrHusbandName = schemas.StrSchema
                        validFrom = schemas.StrSchema
                        validTo = schemas.StrSchema
                        epicNo = schemas.StrSchema
                        nameInVernacular = schemas.StrSchema
                        gender = schemas.StrSchema
                        age = schemas.NumberSchema
                        relativeName = schemas.StrSchema
                        relativeNameInVernacular = schemas.StrSchema
                        relativeRelationType = schemas.StrSchema
                        houseNumber = schemas.StrSchema
                        partOrLocationInConstituency = schemas.StrSchema
                        partNumberOrLocationNumberInConstituency = schemas.StrSchema
                        parliamentaryConstituency = schemas.StrSchema
                        assemblyConstituency = schemas.StrSchema
                        sectionOfConstituencyPart = schemas.StrSchema
                        cardSerialNumberInPollingList = schemas.StrSchema
                        lastUpdateDate = schemas.StrSchema
                        
                        
                        class pollingBoothDetails(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    latLong = schemas.StrSchema
                                    name = schemas.StrSchema
                                    nameVernacular = schemas.StrSchema
                                    number = schemas.StrSchema
                                    __annotations__ = {
                                        "latLong": latLong,
                                        "name": name,
                                        "nameVernacular": nameVernacular,
                                        "number": number,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["latLong"]) -> MetaOapg.properties.latLong: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["nameVernacular"]) -> MetaOapg.properties.nameVernacular: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["number"]) -> MetaOapg.properties.number: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["latLong", "name", "nameVernacular", "number", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["latLong"]) -> typing.Union[MetaOapg.properties.latLong, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["nameVernacular"]) -> typing.Union[MetaOapg.properties.nameVernacular, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["number"]) -> typing.Union[MetaOapg.properties.number, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["latLong", "name", "nameVernacular", "number", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                latLong: typing.Union[MetaOapg.properties.latLong, str, schemas.Unset] = schemas.unset,
                                name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
                                nameVernacular: typing.Union[MetaOapg.properties.nameVernacular, str, schemas.Unset] = schemas.unset,
                                number: typing.Union[MetaOapg.properties.number, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'pollingBoothDetails':
                                return super().__new__(
                                    cls,
                                    *args,
                                    latLong=latLong,
                                    name=name,
                                    nameVernacular=nameVernacular,
                                    number=number,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        emailId = schemas.StrSchema
                        mobileNumber = schemas.StrSchema
                        stateCode = schemas.StrSchema
                        pollingBoothCoordinates = schemas.StrSchema
                        pollingBoothAddress = schemas.StrSchema
                        pollingBoothNumber = schemas.StrSchema
                        id = schemas.StrSchema
                        blacklistStatus = schemas.StrSchema
                        registrationDate = schemas.StrSchema
                        registrationLocation = schemas.StrSchema
                        propertyClass = schemas.StrSchema
                        maker = schemas.StrSchema
                        ownerName = schemas.StrSchema
                        chassisNumber = schemas.StrSchema
                        registrationNumber = schemas.StrSchema
                        engineNumber = schemas.StrSchema
                        fuelType = schemas.StrSchema
                        fitUpto = schemas.StrSchema
                        insuranceUpto = schemas.StrSchema
                        taxUpto = schemas.StrSchema
                        insuranceDetails = schemas.StrSchema
                        insuranceValidity = schemas.StrSchema
                        permitType = schemas.StrSchema
                        permitValidUpto = schemas.StrSchema
                        pollutionControlValidity = schemas.StrSchema
                        pollutionNorms = schemas.StrSchema
                        licenseAddress = schemas.StrSchema
                        registrationAddress = schemas.StrSchema
                        ownerFatherName = schemas.StrSchema
                        ownerPresentAddress = schemas.StrSchema
                        bodyType = schemas.StrSchema
                        category = schemas.StrSchema
                        color = schemas.StrSchema
                        engineCubicCapacity = schemas.StrSchema
                        numberCylinders = schemas.StrSchema
                        unladenWeight = schemas.StrSchema
                        grossWeight = schemas.StrSchema
                        wheelbase = schemas.StrSchema
                        manufacturedMonthYear = schemas.StrSchema
                        makerDescription = schemas.StrSchema
                        nocDetails = schemas.StrSchema
                        normsDescription = schemas.StrSchema
                        financier = schemas.StrSchema
                        permitIssueDate = schemas.StrSchema
                        permitNumber = schemas.StrSchema
                        permitValidFrom = schemas.StrSchema
                        seatingCapacity = schemas.StrSchema
                        sleepingCapacity = schemas.StrSchema
                        standingCapacity = schemas.StrSchema
                        statusAsOn = schemas.StrSchema
                        
                        
                        class primaryBusinessContact(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    email = schemas.StrSchema
                                    
                                    
                                    class address(
                                        schemas.ComposedSchema,
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            one_of_0 = schemas.StrSchema
                                            
                                            
                                            class one_of_1(
                                                schemas.DictSchema
                                            ):
                                            
                                            
                                                class MetaOapg:
                                                    
                                                    class properties:
                                                        buildingName = schemas.StrSchema
                                                        streetName = schemas.StrSchema
                                                        location = schemas.StrSchema
                                                        buildingNumber = schemas.StrSchema
                                                        district = schemas.StrSchema
                                                        stateName = schemas.StrSchema
                                                        pincode = schemas.StrSchema
                                                        __annotations__ = {
                                                            "buildingName": buildingName,
                                                            "streetName": streetName,
                                                            "location": location,
                                                            "buildingNumber": buildingNumber,
                                                            "district": district,
                                                            "stateName": stateName,
                                                            "pincode": pincode,
                                                        }
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["buildingName"]) -> MetaOapg.properties.buildingName: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["streetName"]) -> MetaOapg.properties.streetName: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["location"]) -> MetaOapg.properties.location: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["buildingNumber"]) -> MetaOapg.properties.buildingNumber: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["district"]) -> MetaOapg.properties.district: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["stateName"]) -> MetaOapg.properties.stateName: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: typing_extensions.Literal["pincode"]) -> MetaOapg.properties.pincode: ...
                                                
                                                @typing.overload
                                                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                                
                                                def __getitem__(self, name: typing.Union[typing_extensions.Literal["buildingName", "streetName", "location", "buildingNumber", "district", "stateName", "pincode", ], str]):
                                                    # dict_instance[name] accessor
                                                    return super().__getitem__(name)
                                                
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["buildingName"]) -> typing.Union[MetaOapg.properties.buildingName, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["streetName"]) -> typing.Union[MetaOapg.properties.streetName, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["location"]) -> typing.Union[MetaOapg.properties.location, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["buildingNumber"]) -> typing.Union[MetaOapg.properties.buildingNumber, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["district"]) -> typing.Union[MetaOapg.properties.district, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["stateName"]) -> typing.Union[MetaOapg.properties.stateName, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: typing_extensions.Literal["pincode"]) -> typing.Union[MetaOapg.properties.pincode, schemas.Unset]: ...
                                                
                                                @typing.overload
                                                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                                
                                                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["buildingName", "streetName", "location", "buildingNumber", "district", "stateName", "pincode", ], str]):
                                                    return super().get_item_oapg(name)
                                                
                                            
                                                def __new__(
                                                    cls,
                                                    *args: typing.Union[dict, frozendict.frozendict, ],
                                                    buildingName: typing.Union[MetaOapg.properties.buildingName, str, schemas.Unset] = schemas.unset,
                                                    streetName: typing.Union[MetaOapg.properties.streetName, str, schemas.Unset] = schemas.unset,
                                                    location: typing.Union[MetaOapg.properties.location, str, schemas.Unset] = schemas.unset,
                                                    buildingNumber: typing.Union[MetaOapg.properties.buildingNumber, str, schemas.Unset] = schemas.unset,
                                                    district: typing.Union[MetaOapg.properties.district, str, schemas.Unset] = schemas.unset,
                                                    stateName: typing.Union[MetaOapg.properties.stateName, str, schemas.Unset] = schemas.unset,
                                                    pincode: typing.Union[MetaOapg.properties.pincode, str, schemas.Unset] = schemas.unset,
                                                    _configuration: typing.Optional[schemas.Configuration] = None,
                                                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                                ) -> 'one_of_1':
                                                    return super().__new__(
                                                        cls,
                                                        *args,
                                                        buildingName=buildingName,
                                                        streetName=streetName,
                                                        location=location,
                                                        buildingNumber=buildingNumber,
                                                        district=district,
                                                        stateName=stateName,
                                                        pincode=pincode,
                                                        _configuration=_configuration,
                                                        **kwargs,
                                                    )
                                            
                                            @classmethod
                                            @functools.lru_cache()
                                            def one_of(cls):
                                                # we need this here to make our import statements work
                                                # we must store _composed_schemas in here so the code is only run
                                                # when we invoke this method. If we kept this at the class
                                                # level we would get an error because the class level
                                                # code would be run when this module is imported, and these composed
                                                # classes don't exist yet because their module has not finished
                                                # loading
                                                return [
                                                    cls.one_of_0,
                                                    cls.one_of_1,
                                                ]
                                    
                                    
                                        def __new__(
                                            cls,
                                            *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                            **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                        ) -> 'address':
                                            return super().__new__(
                                                cls,
                                                *args,
                                                _configuration=_configuration,
                                                **kwargs,
                                            )
                                    
                                    
                                    class mobileNumber(
                                        schemas.ComposedSchema,
                                    ):
                                    
                                    
                                        class MetaOapg:
                                            one_of_0 = schemas.StrSchema
                                            one_of_1 = schemas.NumberSchema
                                            
                                            @classmethod
                                            @functools.lru_cache()
                                            def one_of(cls):
                                                # we need this here to make our import statements work
                                                # we must store _composed_schemas in here so the code is only run
                                                # when we invoke this method. If we kept this at the class
                                                # level we would get an error because the class level
                                                # code would be run when this module is imported, and these composed
                                                # classes don't exist yet because their module has not finished
                                                # loading
                                                return [
                                                    cls.one_of_0,
                                                    cls.one_of_1,
                                                ]
                                    
                                    
                                        def __new__(
                                            cls,
                                            *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                                            _configuration: typing.Optional[schemas.Configuration] = None,
                                            **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                        ) -> 'mobileNumber':
                                            return super().__new__(
                                                cls,
                                                *args,
                                                _configuration=_configuration,
                                                **kwargs,
                                            )
                                    natureOfBusinessAtAddress = schemas.StrSchema
                                    lastUpdatedDate = schemas.StrSchema
                                    __annotations__ = {
                                        "email": email,
                                        "address": address,
                                        "mobileNumber": mobileNumber,
                                        "natureOfBusinessAtAddress": natureOfBusinessAtAddress,
                                        "lastUpdatedDate": lastUpdatedDate,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["email"]) -> MetaOapg.properties.email: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["mobileNumber"]) -> MetaOapg.properties.mobileNumber: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["natureOfBusinessAtAddress"]) -> MetaOapg.properties.natureOfBusinessAtAddress: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["lastUpdatedDate"]) -> MetaOapg.properties.lastUpdatedDate: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["email", "address", "mobileNumber", "natureOfBusinessAtAddress", "lastUpdatedDate", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["email"]) -> typing.Union[MetaOapg.properties.email, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["mobileNumber"]) -> typing.Union[MetaOapg.properties.mobileNumber, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["natureOfBusinessAtAddress"]) -> typing.Union[MetaOapg.properties.natureOfBusinessAtAddress, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["lastUpdatedDate"]) -> typing.Union[MetaOapg.properties.lastUpdatedDate, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["email", "address", "mobileNumber", "natureOfBusinessAtAddress", "lastUpdatedDate", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                email: typing.Union[MetaOapg.properties.email, str, schemas.Unset] = schemas.unset,
                                address: typing.Union[MetaOapg.properties.address, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
                                mobileNumber: typing.Union[MetaOapg.properties.mobileNumber, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
                                natureOfBusinessAtAddress: typing.Union[MetaOapg.properties.natureOfBusinessAtAddress, str, schemas.Unset] = schemas.unset,
                                lastUpdatedDate: typing.Union[MetaOapg.properties.lastUpdatedDate, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'primaryBusinessContact':
                                return super().__new__(
                                    cls,
                                    *args,
                                    email=email,
                                    address=address,
                                    mobileNumber=mobileNumber,
                                    natureOfBusinessAtAddress=natureOfBusinessAtAddress,
                                    lastUpdatedDate=lastUpdatedDate,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        stateJurisdiction = schemas.StrSchema
                        stateJurisdictionCode = schemas.StrSchema
                        taxpayerType = schemas.StrSchema
                        constitutionOfBusiness = schemas.StrSchema
                        gstnStatus = schemas.StrSchema
                        tradeName = schemas.StrSchema
                        gstin = schemas.StrSchema
                        
                        
                        class additionalPlacesOfBusinessInState(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                items = schemas.StrSchema
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'additionalPlacesOfBusinessInState':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        legalName = schemas.StrSchema
                        
                        
                        class natureOfBusiness(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                items = schemas.StrSchema
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'natureOfBusiness':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        centralJurisdiction = schemas.StrSchema
                        centralJurisdictionCode = schemas.StrSchema
                        pan = schemas.StrSchema
                        authorizedSignatories = schemas.StrSchema
                        complianceRating = schemas.StrSchema
                        cxdt = schemas.StrSchema
                        
                        
                        class businessDetails(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                
                                class items(
                                    schemas.DictSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        
                                        class properties:
                                            hsn = schemas.StrSchema
                                            serviceDetail = schemas.StrSchema
                                            __annotations__ = {
                                                "hsn": hsn,
                                                "serviceDetail": serviceDetail,
                                            }
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["hsn"]) -> MetaOapg.properties.hsn: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["serviceDetail"]) -> MetaOapg.properties.serviceDetail: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                    
                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["hsn", "serviceDetail", ], str]):
                                        # dict_instance[name] accessor
                                        return super().__getitem__(name)
                                    
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["hsn"]) -> typing.Union[MetaOapg.properties.hsn, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["serviceDetail"]) -> typing.Union[MetaOapg.properties.serviceDetail, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                    
                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["hsn", "serviceDetail", ], str]):
                                        return super().get_item_oapg(name)
                                    
                                
                                    def __new__(
                                        cls,
                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                        hsn: typing.Union[MetaOapg.properties.hsn, str, schemas.Unset] = schemas.unset,
                                        serviceDetail: typing.Union[MetaOapg.properties.serviceDetail, str, schemas.Unset] = schemas.unset,
                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                    ) -> 'items':
                                        return super().__new__(
                                            cls,
                                            *args,
                                            hsn=hsn,
                                            serviceDetail=serviceDetail,
                                            _configuration=_configuration,
                                            **kwargs,
                                        )
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'businessDetails':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        annualAggregateTurnover = schemas.StrSchema
                        mandatoryEInvoicing = schemas.StrSchema
                        grossTotalIncome = schemas.StrSchema
                        grossTotalIncomeFinancialYear = schemas.StrSchema
                        isFieldVisitConducted = schemas.StrSchema
                        
                        
                        class filingStatus(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                
                                class items(
                                    schemas.DictSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        
                                        class properties:
                                            filingYear = schemas.StrSchema
                                            filingForMonth = schemas.StrSchema
                                            filingMethod = schemas.StrSchema
                                            filingDate = schemas.StrSchema
                                            filingGstType = schemas.StrSchema
                                            filingAnnualReturn = schemas.StrSchema
                                            filingStatus = schemas.StrSchema
                                            __annotations__ = {
                                                "filingYear": filingYear,
                                                "filingForMonth": filingForMonth,
                                                "filingMethod": filingMethod,
                                                "filingDate": filingDate,
                                                "filingGstType": filingGstType,
                                                "filingAnnualReturn": filingAnnualReturn,
                                                "filingStatus": filingStatus,
                                            }
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingYear"]) -> MetaOapg.properties.filingYear: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingForMonth"]) -> MetaOapg.properties.filingForMonth: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingMethod"]) -> MetaOapg.properties.filingMethod: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingDate"]) -> MetaOapg.properties.filingDate: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingGstType"]) -> MetaOapg.properties.filingGstType: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingAnnualReturn"]) -> MetaOapg.properties.filingAnnualReturn: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: typing_extensions.Literal["filingStatus"]) -> MetaOapg.properties.filingStatus: ...
                                    
                                    @typing.overload
                                    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                    
                                    def __getitem__(self, name: typing.Union[typing_extensions.Literal["filingYear", "filingForMonth", "filingMethod", "filingDate", "filingGstType", "filingAnnualReturn", "filingStatus", ], str]):
                                        # dict_instance[name] accessor
                                        return super().__getitem__(name)
                                    
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingYear"]) -> typing.Union[MetaOapg.properties.filingYear, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingForMonth"]) -> typing.Union[MetaOapg.properties.filingForMonth, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingMethod"]) -> typing.Union[MetaOapg.properties.filingMethod, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingDate"]) -> typing.Union[MetaOapg.properties.filingDate, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingGstType"]) -> typing.Union[MetaOapg.properties.filingGstType, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingAnnualReturn"]) -> typing.Union[MetaOapg.properties.filingAnnualReturn, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: typing_extensions.Literal["filingStatus"]) -> typing.Union[MetaOapg.properties.filingStatus, schemas.Unset]: ...
                                    
                                    @typing.overload
                                    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                    
                                    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["filingYear", "filingForMonth", "filingMethod", "filingDate", "filingGstType", "filingAnnualReturn", "filingStatus", ], str]):
                                        return super().get_item_oapg(name)
                                    
                                
                                    def __new__(
                                        cls,
                                        *args: typing.Union[dict, frozendict.frozendict, ],
                                        filingYear: typing.Union[MetaOapg.properties.filingYear, str, schemas.Unset] = schemas.unset,
                                        filingForMonth: typing.Union[MetaOapg.properties.filingForMonth, str, schemas.Unset] = schemas.unset,
                                        filingMethod: typing.Union[MetaOapg.properties.filingMethod, str, schemas.Unset] = schemas.unset,
                                        filingDate: typing.Union[MetaOapg.properties.filingDate, str, schemas.Unset] = schemas.unset,
                                        filingGstType: typing.Union[MetaOapg.properties.filingGstType, str, schemas.Unset] = schemas.unset,
                                        filingAnnualReturn: typing.Union[MetaOapg.properties.filingAnnualReturn, str, schemas.Unset] = schemas.unset,
                                        filingStatus: typing.Union[MetaOapg.properties.filingStatus, str, schemas.Unset] = schemas.unset,
                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                    ) -> 'items':
                                        return super().__new__(
                                            cls,
                                            *args,
                                            filingYear=filingYear,
                                            filingForMonth=filingForMonth,
                                            filingMethod=filingMethod,
                                            filingDate=filingDate,
                                            filingGstType=filingGstType,
                                            filingAnnualReturn=filingAnnualReturn,
                                            filingStatus=filingStatus,
                                            _configuration=_configuration,
                                            **kwargs,
                                        )
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'filingStatus':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        
                        
                        class directors(
                            schemas.ComposedSchema,
                        ):
                        
                        
                            class MetaOapg:
                                one_of_0 = schemas.StrSchema
                                
                                
                                class one_of_1(
                                    schemas.ListSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        
                                        
                                        class items(
                                            schemas.DictSchema
                                        ):
                                        
                                        
                                            class MetaOapg:
                                                
                                                class properties:
                                                    endDate = schemas.StrSchema
                                                    surrenderedDin = schemas.StrSchema
                                                    dinOrPan = schemas.StrSchema
                                                    beginDate = schemas.StrSchema
                                                    name = schemas.StrSchema
                                                    __annotations__ = {
                                                        "endDate": endDate,
                                                        "surrenderedDin": surrenderedDin,
                                                        "dinOrPan": dinOrPan,
                                                        "beginDate": beginDate,
                                                        "name": name,
                                                    }
                                            
                                            @typing.overload
                                            def __getitem__(self, name: typing_extensions.Literal["endDate"]) -> MetaOapg.properties.endDate: ...
                                            
                                            @typing.overload
                                            def __getitem__(self, name: typing_extensions.Literal["surrenderedDin"]) -> MetaOapg.properties.surrenderedDin: ...
                                            
                                            @typing.overload
                                            def __getitem__(self, name: typing_extensions.Literal["dinOrPan"]) -> MetaOapg.properties.dinOrPan: ...
                                            
                                            @typing.overload
                                            def __getitem__(self, name: typing_extensions.Literal["beginDate"]) -> MetaOapg.properties.beginDate: ...
                                            
                                            @typing.overload
                                            def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                                            
                                            @typing.overload
                                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                                            
                                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["endDate", "surrenderedDin", "dinOrPan", "beginDate", "name", ], str]):
                                                # dict_instance[name] accessor
                                                return super().__getitem__(name)
                                            
                                            
                                            @typing.overload
                                            def get_item_oapg(self, name: typing_extensions.Literal["endDate"]) -> typing.Union[MetaOapg.properties.endDate, schemas.Unset]: ...
                                            
                                            @typing.overload
                                            def get_item_oapg(self, name: typing_extensions.Literal["surrenderedDin"]) -> typing.Union[MetaOapg.properties.surrenderedDin, schemas.Unset]: ...
                                            
                                            @typing.overload
                                            def get_item_oapg(self, name: typing_extensions.Literal["dinOrPan"]) -> typing.Union[MetaOapg.properties.dinOrPan, schemas.Unset]: ...
                                            
                                            @typing.overload
                                            def get_item_oapg(self, name: typing_extensions.Literal["beginDate"]) -> typing.Union[MetaOapg.properties.beginDate, schemas.Unset]: ...
                                            
                                            @typing.overload
                                            def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
                                            
                                            @typing.overload
                                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                                            
                                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["endDate", "surrenderedDin", "dinOrPan", "beginDate", "name", ], str]):
                                                return super().get_item_oapg(name)
                                            
                                        
                                            def __new__(
                                                cls,
                                                *args: typing.Union[dict, frozendict.frozendict, ],
                                                endDate: typing.Union[MetaOapg.properties.endDate, str, schemas.Unset] = schemas.unset,
                                                surrenderedDin: typing.Union[MetaOapg.properties.surrenderedDin, str, schemas.Unset] = schemas.unset,
                                                dinOrPan: typing.Union[MetaOapg.properties.dinOrPan, str, schemas.Unset] = schemas.unset,
                                                beginDate: typing.Union[MetaOapg.properties.beginDate, str, schemas.Unset] = schemas.unset,
                                                name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
                                                _configuration: typing.Optional[schemas.Configuration] = None,
                                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                                            ) -> 'items':
                                                return super().__new__(
                                                    cls,
                                                    *args,
                                                    endDate=endDate,
                                                    surrenderedDin=surrenderedDin,
                                                    dinOrPan=dinOrPan,
                                                    beginDate=beginDate,
                                                    name=name,
                                                    _configuration=_configuration,
                                                    **kwargs,
                                                )
                                
                                    def __new__(
                                        cls,
                                        arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                                        _configuration: typing.Optional[schemas.Configuration] = None,
                                    ) -> 'one_of_1':
                                        return super().__new__(
                                            cls,
                                            arg,
                                            _configuration=_configuration,
                                        )
                                
                                    def __getitem__(self, i: int) -> MetaOapg.items:
                                        return super().__getitem__(i)
                                
                                @classmethod
                                @functools.lru_cache()
                                def one_of(cls):
                                    # we need this here to make our import statements work
                                    # we must store _composed_schemas in here so the code is only run
                                    # when we invoke this method. If we kept this at the class
                                    # level we would get an error because the class level
                                    # code would be run when this module is imported, and these composed
                                    # classes don't exist yet because their module has not finished
                                    # loading
                                    return [
                                        cls.one_of_0,
                                        cls.one_of_1,
                                    ]
                        
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'directors':
                                return super().__new__(
                                    cls,
                                    *args,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        
                        
                        class companyMasterData(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    companyCategory = schemas.StrSchema
                                    emailId = schemas.StrSchema
                                    classOfCompany = schemas.StrSchema
                                    numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital = schemas.StrSchema
                                    addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained = schemas.StrSchema
                                    dateOfLastAgm = schemas.StrSchema
                                    registeredAddress = schemas.StrSchema
                                    activeCompliance = schemas.StrSchema
                                    registrationNumber = schemas.StrSchema
                                    paidUpCapitalInInr = schemas.StrSchema
                                    whetherListedOrNot = schemas.StrSchema
                                    suspendedAtStockExchange = schemas.StrSchema
                                    companySubcategory = schemas.StrSchema
                                    authorisedCapitalInInr = schemas.StrSchema
                                    companyStatusForEFiling = schemas.StrSchema
                                    rocCode = schemas.StrSchema
                                    dateOfBalanceSheet = schemas.StrSchema
                                    dateOfIncorporation = schemas.StrSchema
                                    cin = schemas.StrSchema
                                    companyName = schemas.StrSchema
                                    __annotations__ = {
                                        "companyCategory": companyCategory,
                                        "emailId": emailId,
                                        "classOfCompany": classOfCompany,
                                        "numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital": numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital,
                                        "addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained": addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained,
                                        "dateOfLastAgm": dateOfLastAgm,
                                        "registeredAddress": registeredAddress,
                                        "activeCompliance": activeCompliance,
                                        "registrationNumber": registrationNumber,
                                        "paidUpCapitalInInr": paidUpCapitalInInr,
                                        "whetherListedOrNot": whetherListedOrNot,
                                        "suspendedAtStockExchange": suspendedAtStockExchange,
                                        "companySubcategory": companySubcategory,
                                        "authorisedCapitalInInr": authorisedCapitalInInr,
                                        "companyStatusForEFiling": companyStatusForEFiling,
                                        "rocCode": rocCode,
                                        "dateOfBalanceSheet": dateOfBalanceSheet,
                                        "dateOfIncorporation": dateOfIncorporation,
                                        "cin ": cin,
                                        "companyName": companyName,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["companyCategory"]) -> MetaOapg.properties.companyCategory: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["emailId"]) -> MetaOapg.properties.emailId: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["classOfCompany"]) -> MetaOapg.properties.classOfCompany: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital"]) -> MetaOapg.properties.numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained"]) -> MetaOapg.properties.addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfLastAgm"]) -> MetaOapg.properties.dateOfLastAgm: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["registeredAddress"]) -> MetaOapg.properties.registeredAddress: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["activeCompliance"]) -> MetaOapg.properties.activeCompliance: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["registrationNumber"]) -> MetaOapg.properties.registrationNumber: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["paidUpCapitalInInr"]) -> MetaOapg.properties.paidUpCapitalInInr: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["whetherListedOrNot"]) -> MetaOapg.properties.whetherListedOrNot: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["suspendedAtStockExchange"]) -> MetaOapg.properties.suspendedAtStockExchange: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["companySubcategory"]) -> MetaOapg.properties.companySubcategory: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["authorisedCapitalInInr"]) -> MetaOapg.properties.authorisedCapitalInInr: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["companyStatusForEFiling"]) -> MetaOapg.properties.companyStatusForEFiling: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["rocCode"]) -> MetaOapg.properties.rocCode: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfBalanceSheet"]) -> MetaOapg.properties.dateOfBalanceSheet: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfIncorporation"]) -> MetaOapg.properties.dateOfIncorporation: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["cin "]) -> MetaOapg.properties.cin: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["companyName"]) -> MetaOapg.properties.companyName: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["companyCategory", "emailId", "classOfCompany", "numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital", "addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained", "dateOfLastAgm", "registeredAddress", "activeCompliance", "registrationNumber", "paidUpCapitalInInr", "whetherListedOrNot", "suspendedAtStockExchange", "companySubcategory", "authorisedCapitalInInr", "companyStatusForEFiling", "rocCode", "dateOfBalanceSheet", "dateOfIncorporation", "cin ", "companyName", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["companyCategory"]) -> typing.Union[MetaOapg.properties.companyCategory, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["emailId"]) -> typing.Union[MetaOapg.properties.emailId, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["classOfCompany"]) -> typing.Union[MetaOapg.properties.classOfCompany, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital"]) -> typing.Union[MetaOapg.properties.numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained"]) -> typing.Union[MetaOapg.properties.addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfLastAgm"]) -> typing.Union[MetaOapg.properties.dateOfLastAgm, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["registeredAddress"]) -> typing.Union[MetaOapg.properties.registeredAddress, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["activeCompliance"]) -> typing.Union[MetaOapg.properties.activeCompliance, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["registrationNumber"]) -> typing.Union[MetaOapg.properties.registrationNumber, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["paidUpCapitalInInr"]) -> typing.Union[MetaOapg.properties.paidUpCapitalInInr, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["whetherListedOrNot"]) -> typing.Union[MetaOapg.properties.whetherListedOrNot, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["suspendedAtStockExchange"]) -> typing.Union[MetaOapg.properties.suspendedAtStockExchange, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["companySubcategory"]) -> typing.Union[MetaOapg.properties.companySubcategory, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["authorisedCapitalInInr"]) -> typing.Union[MetaOapg.properties.authorisedCapitalInInr, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["companyStatusForEFiling"]) -> typing.Union[MetaOapg.properties.companyStatusForEFiling, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["rocCode"]) -> typing.Union[MetaOapg.properties.rocCode, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfBalanceSheet"]) -> typing.Union[MetaOapg.properties.dateOfBalanceSheet, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfIncorporation"]) -> typing.Union[MetaOapg.properties.dateOfIncorporation, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["cin "]) -> typing.Union[MetaOapg.properties.cin, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["companyName"]) -> typing.Union[MetaOapg.properties.companyName, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["companyCategory", "emailId", "classOfCompany", "numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital", "addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained", "dateOfLastAgm", "registeredAddress", "activeCompliance", "registrationNumber", "paidUpCapitalInInr", "whetherListedOrNot", "suspendedAtStockExchange", "companySubcategory", "authorisedCapitalInInr", "companyStatusForEFiling", "rocCode", "dateOfBalanceSheet", "dateOfIncorporation", "cin ", "companyName", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                companyCategory: typing.Union[MetaOapg.properties.companyCategory, str, schemas.Unset] = schemas.unset,
                                emailId: typing.Union[MetaOapg.properties.emailId, str, schemas.Unset] = schemas.unset,
                                classOfCompany: typing.Union[MetaOapg.properties.classOfCompany, str, schemas.Unset] = schemas.unset,
                                numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital: typing.Union[MetaOapg.properties.numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital, str, schemas.Unset] = schemas.unset,
                                addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained: typing.Union[MetaOapg.properties.addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained, str, schemas.Unset] = schemas.unset,
                                dateOfLastAgm: typing.Union[MetaOapg.properties.dateOfLastAgm, str, schemas.Unset] = schemas.unset,
                                registeredAddress: typing.Union[MetaOapg.properties.registeredAddress, str, schemas.Unset] = schemas.unset,
                                activeCompliance: typing.Union[MetaOapg.properties.activeCompliance, str, schemas.Unset] = schemas.unset,
                                registrationNumber: typing.Union[MetaOapg.properties.registrationNumber, str, schemas.Unset] = schemas.unset,
                                paidUpCapitalInInr: typing.Union[MetaOapg.properties.paidUpCapitalInInr, str, schemas.Unset] = schemas.unset,
                                whetherListedOrNot: typing.Union[MetaOapg.properties.whetherListedOrNot, str, schemas.Unset] = schemas.unset,
                                suspendedAtStockExchange: typing.Union[MetaOapg.properties.suspendedAtStockExchange, str, schemas.Unset] = schemas.unset,
                                companySubcategory: typing.Union[MetaOapg.properties.companySubcategory, str, schemas.Unset] = schemas.unset,
                                authorisedCapitalInInr: typing.Union[MetaOapg.properties.authorisedCapitalInInr, str, schemas.Unset] = schemas.unset,
                                companyStatusForEFiling: typing.Union[MetaOapg.properties.companyStatusForEFiling, str, schemas.Unset] = schemas.unset,
                                rocCode: typing.Union[MetaOapg.properties.rocCode, str, schemas.Unset] = schemas.unset,
                                dateOfBalanceSheet: typing.Union[MetaOapg.properties.dateOfBalanceSheet, str, schemas.Unset] = schemas.unset,
                                dateOfIncorporation: typing.Union[MetaOapg.properties.dateOfIncorporation, str, schemas.Unset] = schemas.unset,
                                companyName: typing.Union[MetaOapg.properties.companyName, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'companyMasterData':
                                return super().__new__(
                                    cls,
                                    *args,
                                    companyCategory=companyCategory,
                                    emailId=emailId,
                                    classOfCompany=classOfCompany,
                                    numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital=numberOfMembersApplicableInCaseOfCompanyWithoutShareCapital,
                                    addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained=addressOtherThanRegisteredOfficeWhereAllOrAnyBooksOfAccountAndPapersAreMaintained,
                                    dateOfLastAgm=dateOfLastAgm,
                                    registeredAddress=registeredAddress,
                                    activeCompliance=activeCompliance,
                                    registrationNumber=registrationNumber,
                                    paidUpCapitalInInr=paidUpCapitalInInr,
                                    whetherListedOrNot=whetherListedOrNot,
                                    suspendedAtStockExchange=suspendedAtStockExchange,
                                    companySubcategory=companySubcategory,
                                    authorisedCapitalInInr=authorisedCapitalInInr,
                                    companyStatusForEFiling=companyStatusForEFiling,
                                    rocCode=rocCode,
                                    dateOfBalanceSheet=dateOfBalanceSheet,
                                    dateOfIncorporation=dateOfIncorporation,
                                    companyName=companyName,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        
                        
                        class charges(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                items = schemas.StrSchema
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'charges':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        
                        
                        class llpData(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                items = schemas.StrSchema
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'llpData':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        
                        
                        class companyData(
                            schemas.ListSchema
                        ):
                        
                        
                            class MetaOapg:
                                items = schemas.StrSchema
                        
                            def __new__(
                                cls,
                                arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                            ) -> 'companyData':
                                return super().__new__(
                                    cls,
                                    arg,
                                    _configuration=_configuration,
                                )
                        
                            def __getitem__(self, i: int) -> MetaOapg.items:
                                return super().__getitem__(i)
                        
                        
                        class directorData(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    din = schemas.StrSchema
                                    name = schemas.StrSchema
                                    __annotations__ = {
                                        "din": din,
                                        "name": name,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["din"]) -> MetaOapg.properties.din: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["din", "name", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["din"]) -> typing.Union[MetaOapg.properties.din, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["din", "name", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                din: typing.Union[MetaOapg.properties.din, str, schemas.Unset] = schemas.unset,
                                name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'directorData':
                                return super().__new__(
                                    cls,
                                    *args,
                                    din=din,
                                    name=name,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        
                        
                        class llpMasterData(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    emailId = schemas.StrSchema
                                    registeredAddress = schemas.StrSchema
                                    dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled = schemas.StrSchema
                                    dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled = schemas.StrSchema
                                    mainDivisionOfBusinessActivityToBeCarriedOutInIndia = schemas.StrSchema
                                    previousFircompanyDetailifApplicable = schemas.StrSchema
                                    rocCode = schemas.StrSchema
                                    numberOfDesignatedPartners = schemas.StrSchema
                                    dateOfIncorporation = schemas.StrSchema
                                    llpName = schemas.StrSchema
                                    totalObligationOfContribution = schemas.StrSchema
                                    llpin = schemas.StrSchema
                                    llpStatus = schemas.StrSchema
                                    descriptionOfMainDivision = schemas.StrSchema
                                    numberOfPartners = schemas.StrSchema
                                    __annotations__ = {
                                        "emailId": emailId,
                                        "registeredAddress": registeredAddress,
                                        "dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled": dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled,
                                        "dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled": dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled,
                                        "mainDivisionOfBusinessActivityToBeCarriedOutInIndia": mainDivisionOfBusinessActivityToBeCarriedOutInIndia,
                                        "previousFircompanyDetailifApplicable": previousFircompanyDetailifApplicable,
                                        "rocCode": rocCode,
                                        "numberOfDesignatedPartners": numberOfDesignatedPartners,
                                        "dateOfIncorporation": dateOfIncorporation,
                                        "llpName": llpName,
                                        "totalObligationOfContribution": totalObligationOfContribution,
                                        "llpin ": llpin,
                                        "llpStatus": llpStatus,
                                        "descriptionOfMainDivision": descriptionOfMainDivision,
                                        "numberOfPartners": numberOfPartners,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["emailId"]) -> MetaOapg.properties.emailId: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["registeredAddress"]) -> MetaOapg.properties.registeredAddress: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled"]) -> MetaOapg.properties.dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled"]) -> MetaOapg.properties.dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["mainDivisionOfBusinessActivityToBeCarriedOutInIndia"]) -> MetaOapg.properties.mainDivisionOfBusinessActivityToBeCarriedOutInIndia: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["previousFircompanyDetailifApplicable"]) -> MetaOapg.properties.previousFircompanyDetailifApplicable: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["rocCode"]) -> MetaOapg.properties.rocCode: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["numberOfDesignatedPartners"]) -> MetaOapg.properties.numberOfDesignatedPartners: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfIncorporation"]) -> MetaOapg.properties.dateOfIncorporation: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["llpName"]) -> MetaOapg.properties.llpName: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["totalObligationOfContribution"]) -> MetaOapg.properties.totalObligationOfContribution: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["llpin "]) -> MetaOapg.properties.llpin: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["llpStatus"]) -> MetaOapg.properties.llpStatus: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["descriptionOfMainDivision"]) -> MetaOapg.properties.descriptionOfMainDivision: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["numberOfPartners"]) -> MetaOapg.properties.numberOfPartners: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["emailId", "registeredAddress", "dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled", "dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled", "mainDivisionOfBusinessActivityToBeCarriedOutInIndia", "previousFircompanyDetailifApplicable", "rocCode", "numberOfDesignatedPartners", "dateOfIncorporation", "llpName", "totalObligationOfContribution", "llpin ", "llpStatus", "descriptionOfMainDivision", "numberOfPartners", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["emailId"]) -> typing.Union[MetaOapg.properties.emailId, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["registeredAddress"]) -> typing.Union[MetaOapg.properties.registeredAddress, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled"]) -> typing.Union[MetaOapg.properties.dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled"]) -> typing.Union[MetaOapg.properties.dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["mainDivisionOfBusinessActivityToBeCarriedOutInIndia"]) -> typing.Union[MetaOapg.properties.mainDivisionOfBusinessActivityToBeCarriedOutInIndia, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["previousFircompanyDetailifApplicable"]) -> typing.Union[MetaOapg.properties.previousFircompanyDetailifApplicable, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["rocCode"]) -> typing.Union[MetaOapg.properties.rocCode, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["numberOfDesignatedPartners"]) -> typing.Union[MetaOapg.properties.numberOfDesignatedPartners, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfIncorporation"]) -> typing.Union[MetaOapg.properties.dateOfIncorporation, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["llpName"]) -> typing.Union[MetaOapg.properties.llpName, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["totalObligationOfContribution"]) -> typing.Union[MetaOapg.properties.totalObligationOfContribution, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["llpin "]) -> typing.Union[MetaOapg.properties.llpin, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["llpStatus"]) -> typing.Union[MetaOapg.properties.llpStatus, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["descriptionOfMainDivision"]) -> typing.Union[MetaOapg.properties.descriptionOfMainDivision, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["numberOfPartners"]) -> typing.Union[MetaOapg.properties.numberOfPartners, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["emailId", "registeredAddress", "dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled", "dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled", "mainDivisionOfBusinessActivityToBeCarriedOutInIndia", "previousFircompanyDetailifApplicable", "rocCode", "numberOfDesignatedPartners", "dateOfIncorporation", "llpName", "totalObligationOfContribution", "llpin ", "llpStatus", "descriptionOfMainDivision", "numberOfPartners", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                emailId: typing.Union[MetaOapg.properties.emailId, str, schemas.Unset] = schemas.unset,
                                registeredAddress: typing.Union[MetaOapg.properties.registeredAddress, str, schemas.Unset] = schemas.unset,
                                dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled: typing.Union[MetaOapg.properties.dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled, str, schemas.Unset] = schemas.unset,
                                dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled: typing.Union[MetaOapg.properties.dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled, str, schemas.Unset] = schemas.unset,
                                mainDivisionOfBusinessActivityToBeCarriedOutInIndia: typing.Union[MetaOapg.properties.mainDivisionOfBusinessActivityToBeCarriedOutInIndia, str, schemas.Unset] = schemas.unset,
                                previousFircompanyDetailifApplicable: typing.Union[MetaOapg.properties.previousFircompanyDetailifApplicable, str, schemas.Unset] = schemas.unset,
                                rocCode: typing.Union[MetaOapg.properties.rocCode, str, schemas.Unset] = schemas.unset,
                                numberOfDesignatedPartners: typing.Union[MetaOapg.properties.numberOfDesignatedPartners, str, schemas.Unset] = schemas.unset,
                                dateOfIncorporation: typing.Union[MetaOapg.properties.dateOfIncorporation, str, schemas.Unset] = schemas.unset,
                                llpName: typing.Union[MetaOapg.properties.llpName, str, schemas.Unset] = schemas.unset,
                                totalObligationOfContribution: typing.Union[MetaOapg.properties.totalObligationOfContribution, str, schemas.Unset] = schemas.unset,
                                llpStatus: typing.Union[MetaOapg.properties.llpStatus, str, schemas.Unset] = schemas.unset,
                                descriptionOfMainDivision: typing.Union[MetaOapg.properties.descriptionOfMainDivision, str, schemas.Unset] = schemas.unset,
                                numberOfPartners: typing.Union[MetaOapg.properties.numberOfPartners, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'llpMasterData':
                                return super().__new__(
                                    cls,
                                    *args,
                                    emailId=emailId,
                                    registeredAddress=registeredAddress,
                                    dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled=dateOfLastFinancialYearEndDateForWhichAnnualReturnFiled,
                                    dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled=dateOfLastFinancialYearEndDateForWhichStatementOfAccountsAndSolvencyFiled,
                                    mainDivisionOfBusinessActivityToBeCarriedOutInIndia=mainDivisionOfBusinessActivityToBeCarriedOutInIndia,
                                    previousFircompanyDetailifApplicable=previousFircompanyDetailifApplicable,
                                    rocCode=rocCode,
                                    numberOfDesignatedPartners=numberOfDesignatedPartners,
                                    dateOfIncorporation=dateOfIncorporation,
                                    llpName=llpName,
                                    totalObligationOfContribution=totalObligationOfContribution,
                                    llpStatus=llpStatus,
                                    descriptionOfMainDivision=descriptionOfMainDivision,
                                    numberOfPartners=numberOfPartners,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        
                        
                        class foreignCompanyMasterData(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                
                                class properties:
                                    emailId = schemas.StrSchema
                                    foreignCompanyWithShareCapital = schemas.StrSchema
                                    registeredAddress = schemas.StrSchema
                                    typeOfOffice = schemas.StrSchema
                                    dateOfIncorporation = schemas.StrSchema
                                    countryOfIncorporation = schemas.StrSchema
                                    companyName = schemas.StrSchema
                                    companyStatus = schemas.StrSchema
                                    details = schemas.StrSchema
                                    fcrn = schemas.StrSchema
                                    descriptionOfMainDivision = schemas.StrSchema
                                    mainDivisionOfBusinessActivityToBeCarriedOutInIndia = schemas.StrSchema
                                    __annotations__ = {
                                        "emailId": emailId,
                                        "foreignCompanyWithShareCapital": foreignCompanyWithShareCapital,
                                        "registeredAddress": registeredAddress,
                                        "typeOfOffice": typeOfOffice,
                                        "dateOfIncorporation": dateOfIncorporation,
                                        "countryOfIncorporation": countryOfIncorporation,
                                        "companyName": companyName,
                                        "companyStatus": companyStatus,
                                        "details": details,
                                        "fcrn ": fcrn,
                                        "descriptionOfMainDivision": descriptionOfMainDivision,
                                        "mainDivisionOfBusinessActivityToBeCarriedOutInIndia": mainDivisionOfBusinessActivityToBeCarriedOutInIndia,
                                    }
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["emailId"]) -> MetaOapg.properties.emailId: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["foreignCompanyWithShareCapital"]) -> MetaOapg.properties.foreignCompanyWithShareCapital: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["registeredAddress"]) -> MetaOapg.properties.registeredAddress: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["typeOfOffice"]) -> MetaOapg.properties.typeOfOffice: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["dateOfIncorporation"]) -> MetaOapg.properties.dateOfIncorporation: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["countryOfIncorporation"]) -> MetaOapg.properties.countryOfIncorporation: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["companyName"]) -> MetaOapg.properties.companyName: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["companyStatus"]) -> MetaOapg.properties.companyStatus: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["details"]) -> MetaOapg.properties.details: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["fcrn "]) -> MetaOapg.properties.fcrn: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["descriptionOfMainDivision"]) -> MetaOapg.properties.descriptionOfMainDivision: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["mainDivisionOfBusinessActivityToBeCarriedOutInIndia"]) -> MetaOapg.properties.mainDivisionOfBusinessActivityToBeCarriedOutInIndia: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["emailId", "foreignCompanyWithShareCapital", "registeredAddress", "typeOfOffice", "dateOfIncorporation", "countryOfIncorporation", "companyName", "companyStatus", "details", "fcrn ", "descriptionOfMainDivision", "mainDivisionOfBusinessActivityToBeCarriedOutInIndia", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["emailId"]) -> typing.Union[MetaOapg.properties.emailId, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["foreignCompanyWithShareCapital"]) -> typing.Union[MetaOapg.properties.foreignCompanyWithShareCapital, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["registeredAddress"]) -> typing.Union[MetaOapg.properties.registeredAddress, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["typeOfOffice"]) -> typing.Union[MetaOapg.properties.typeOfOffice, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["dateOfIncorporation"]) -> typing.Union[MetaOapg.properties.dateOfIncorporation, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["countryOfIncorporation"]) -> typing.Union[MetaOapg.properties.countryOfIncorporation, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["companyName"]) -> typing.Union[MetaOapg.properties.companyName, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["companyStatus"]) -> typing.Union[MetaOapg.properties.companyStatus, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["details"]) -> typing.Union[MetaOapg.properties.details, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["fcrn "]) -> typing.Union[MetaOapg.properties.fcrn, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["descriptionOfMainDivision"]) -> typing.Union[MetaOapg.properties.descriptionOfMainDivision, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["mainDivisionOfBusinessActivityToBeCarriedOutInIndia"]) -> typing.Union[MetaOapg.properties.mainDivisionOfBusinessActivityToBeCarriedOutInIndia, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["emailId", "foreignCompanyWithShareCapital", "registeredAddress", "typeOfOffice", "dateOfIncorporation", "countryOfIncorporation", "companyName", "companyStatus", "details", "fcrn ", "descriptionOfMainDivision", "mainDivisionOfBusinessActivityToBeCarriedOutInIndia", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *args: typing.Union[dict, frozendict.frozendict, ],
                                emailId: typing.Union[MetaOapg.properties.emailId, str, schemas.Unset] = schemas.unset,
                                foreignCompanyWithShareCapital: typing.Union[MetaOapg.properties.foreignCompanyWithShareCapital, str, schemas.Unset] = schemas.unset,
                                registeredAddress: typing.Union[MetaOapg.properties.registeredAddress, str, schemas.Unset] = schemas.unset,
                                typeOfOffice: typing.Union[MetaOapg.properties.typeOfOffice, str, schemas.Unset] = schemas.unset,
                                dateOfIncorporation: typing.Union[MetaOapg.properties.dateOfIncorporation, str, schemas.Unset] = schemas.unset,
                                countryOfIncorporation: typing.Union[MetaOapg.properties.countryOfIncorporation, str, schemas.Unset] = schemas.unset,
                                companyName: typing.Union[MetaOapg.properties.companyName, str, schemas.Unset] = schemas.unset,
                                companyStatus: typing.Union[MetaOapg.properties.companyStatus, str, schemas.Unset] = schemas.unset,
                                details: typing.Union[MetaOapg.properties.details, str, schemas.Unset] = schemas.unset,
                                descriptionOfMainDivision: typing.Union[MetaOapg.properties.descriptionOfMainDivision, str, schemas.Unset] = schemas.unset,
                                mainDivisionOfBusinessActivityToBeCarriedOutInIndia: typing.Union[MetaOapg.properties.mainDivisionOfBusinessActivityToBeCarriedOutInIndia, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'foreignCompanyMasterData':
                                return super().__new__(
                                    cls,
                                    *args,
                                    emailId=emailId,
                                    foreignCompanyWithShareCapital=foreignCompanyWithShareCapital,
                                    registeredAddress=registeredAddress,
                                    typeOfOffice=typeOfOffice,
                                    dateOfIncorporation=dateOfIncorporation,
                                    countryOfIncorporation=countryOfIncorporation,
                                    companyName=companyName,
                                    companyStatus=companyStatus,
                                    details=details,
                                    descriptionOfMainDivision=descriptionOfMainDivision,
                                    mainDivisionOfBusinessActivityToBeCarriedOutInIndia=mainDivisionOfBusinessActivityToBeCarriedOutInIndia,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        __annotations__ = {
                            "idNumber": idNumber,
                            "idStatus": idStatus,
                            "name": name,
                            "licenseType": licenseType,
                            "entityName": entityName,
                            "status": status,
                            "premissesAddress": premissesAddress,
                            "products": products,
                            "address": address,
                            "uamNumber": uamNumber,
                            "enterpriseName": enterpriseName,
                            "majorActivity": majorActivity,
                            "socialCategory": socialCategory,
                            "enterpriseType": enterpriseType,
                            "dateOfCommencement": dateOfCommencement,
                            "district": district,
                            "state": state,
                            "appliedDate": appliedDate,
                            "modifiedDate": modifiedDate,
                            "expiryDate": expiryDate,
                            "nic_2Digit": nic_2Digit,
                            "nic_4Digit": nic_4Digit,
                            "nic_5Digit": nic_5Digit,
                            "panStatus": panStatus,
                            "lastName": lastName,
                            "firstName": firstName,
                            "fullName": fullName,
                            "idHolderTitle": idHolderTitle,
                            "idLastUpdated": idLastUpdated,
                            "aadhaarSeedingStatus": aadhaarSeedingStatus,
                            "addresses": addresses,
                            "allClassOfVehicle": allClassOfVehicle,
                            "drivingLicenseNumber": drivingLicenseNumber,
                            "dateOfBirth": dateOfBirth,
                            "endorseDate": endorseDate,
                            "endorseNumber": endorseNumber,
                            "fatherOrHusbandName": fatherOrHusbandName,
                            "validFrom": validFrom,
                            "validTo": validTo,
                            "epicNo": epicNo,
                            "nameInVernacular": nameInVernacular,
                            "gender": gender,
                            "age": age,
                            "relativeName": relativeName,
                            "relativeNameInVernacular": relativeNameInVernacular,
                            "relativeRelationType": relativeRelationType,
                            "houseNumber": houseNumber,
                            "partOrLocationInConstituency": partOrLocationInConstituency,
                            "partNumberOrLocationNumberInConstituency": partNumberOrLocationNumberInConstituency,
                            "parliamentaryConstituency": parliamentaryConstituency,
                            "assemblyConstituency": assemblyConstituency,
                            "sectionOfConstituencyPart": sectionOfConstituencyPart,
                            "cardSerialNumberInPollingList": cardSerialNumberInPollingList,
                            "lastUpdateDate": lastUpdateDate,
                            "pollingBoothDetails": pollingBoothDetails,
                            "emailId": emailId,
                            "mobileNumber": mobileNumber,
                            "stateCode": stateCode,
                            "pollingBoothCoordinates": pollingBoothCoordinates,
                            "pollingBoothAddress": pollingBoothAddress,
                            "pollingBoothNumber": pollingBoothNumber,
                            "id": id,
                            "blacklistStatus": blacklistStatus,
                            "registrationDate": registrationDate,
                            "registrationLocation": registrationLocation,
                            "class": propertyClass,
                            "maker": maker,
                            "ownerName": ownerName,
                            "chassisNumber": chassisNumber,
                            "registrationNumber": registrationNumber,
                            "engineNumber": engineNumber,
                            "fuelType": fuelType,
                            "fitUpto": fitUpto,
                            "insuranceUpto": insuranceUpto,
                            "taxUpto": taxUpto,
                            "insuranceDetails": insuranceDetails,
                            "insuranceValidity": insuranceValidity,
                            "permitType": permitType,
                            "permitValidUpto": permitValidUpto,
                            "pollutionControlValidity": pollutionControlValidity,
                            "pollutionNorms": pollutionNorms,
                            "licenseAddress": licenseAddress,
                            "registrationAddress": registrationAddress,
                            "ownerFatherName": ownerFatherName,
                            "ownerPresentAddress": ownerPresentAddress,
                            "bodyType": bodyType,
                            "category": category,
                            "color": color,
                            "engineCubicCapacity": engineCubicCapacity,
                            "numberCylinders": numberCylinders,
                            "unladenWeight": unladenWeight,
                            "grossWeight": grossWeight,
                            "wheelbase": wheelbase,
                            "manufacturedMonthYear": manufacturedMonthYear,
                            "makerDescription": makerDescription,
                            "nocDetails": nocDetails,
                            "normsDescription": normsDescription,
                            "financier": financier,
                            "permitIssueDate": permitIssueDate,
                            "permitNumber": permitNumber,
                            "permitValidFrom": permitValidFrom,
                            "seatingCapacity": seatingCapacity,
                            "sleepingCapacity": sleepingCapacity,
                            "standingCapacity": standingCapacity,
                            "statusAsOn": statusAsOn,
                            "primaryBusinessContact": primaryBusinessContact,
                            "stateJurisdiction": stateJurisdiction,
                            "stateJurisdictionCode": stateJurisdictionCode,
                            "taxpayerType": taxpayerType,
                            "constitutionOfBusiness": constitutionOfBusiness,
                            "gstnStatus": gstnStatus,
                            "tradeName": tradeName,
                            "gstin": gstin,
                            "additionalPlacesOfBusinessInState": additionalPlacesOfBusinessInState,
                            "legalName": legalName,
                            "natureOfBusiness": natureOfBusiness,
                            "centralJurisdiction": centralJurisdiction,
                            "centralJurisdictionCode": centralJurisdictionCode,
                            "pan": pan,
                            "authorizedSignatories": authorizedSignatories,
                            "complianceRating": complianceRating,
                            "cxdt": cxdt,
                            "businessDetails": businessDetails,
                            "annualAggregateTurnover": annualAggregateTurnover,
                            "mandatoryEInvoicing": mandatoryEInvoicing,
                            "grossTotalIncome": grossTotalIncome,
                            "grossTotalIncomeFinancialYear": grossTotalIncomeFinancialYear,
                            "isFieldVisitConducted": isFieldVisitConducted,
                            "filingStatus": filingStatus,
                            "directors": directors,
                            "companyMasterData": companyMasterData,
                            "charges": charges,
                            "llpData": llpData,
                            "companyData": companyData,
                            "directorData": directorData,
                            "llpMasterData": llpMasterData,
                            "foreignCompanyMasterData": foreignCompanyMasterData,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["idNumber"]) -> MetaOapg.properties.idNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["idStatus"]) -> MetaOapg.properties.idStatus: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["licenseType"]) -> MetaOapg.properties.licenseType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["entityName"]) -> MetaOapg.properties.entityName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["premissesAddress"]) -> MetaOapg.properties.premissesAddress: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["products"]) -> MetaOapg.properties.products: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["uamNumber"]) -> MetaOapg.properties.uamNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["enterpriseName"]) -> MetaOapg.properties.enterpriseName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["majorActivity"]) -> MetaOapg.properties.majorActivity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["socialCategory"]) -> MetaOapg.properties.socialCategory: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["enterpriseType"]) -> MetaOapg.properties.enterpriseType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["dateOfCommencement"]) -> MetaOapg.properties.dateOfCommencement: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["district"]) -> MetaOapg.properties.district: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["appliedDate"]) -> MetaOapg.properties.appliedDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["modifiedDate"]) -> MetaOapg.properties.modifiedDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["expiryDate"]) -> MetaOapg.properties.expiryDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["nic_2Digit"]) -> MetaOapg.properties.nic_2Digit: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["nic_4Digit"]) -> MetaOapg.properties.nic_4Digit: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["nic_5Digit"]) -> MetaOapg.properties.nic_5Digit: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["panStatus"]) -> MetaOapg.properties.panStatus: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["lastName"]) -> MetaOapg.properties.lastName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["firstName"]) -> MetaOapg.properties.firstName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["fullName"]) -> MetaOapg.properties.fullName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["idHolderTitle"]) -> MetaOapg.properties.idHolderTitle: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["idLastUpdated"]) -> MetaOapg.properties.idLastUpdated: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["aadhaarSeedingStatus"]) -> MetaOapg.properties.aadhaarSeedingStatus: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["addresses"]) -> MetaOapg.properties.addresses: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["allClassOfVehicle"]) -> MetaOapg.properties.allClassOfVehicle: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["drivingLicenseNumber"]) -> MetaOapg.properties.drivingLicenseNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["dateOfBirth"]) -> MetaOapg.properties.dateOfBirth: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["endorseDate"]) -> MetaOapg.properties.endorseDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["endorseNumber"]) -> MetaOapg.properties.endorseNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["fatherOrHusbandName"]) -> MetaOapg.properties.fatherOrHusbandName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["validFrom"]) -> MetaOapg.properties.validFrom: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["validTo"]) -> MetaOapg.properties.validTo: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["epicNo"]) -> MetaOapg.properties.epicNo: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["nameInVernacular"]) -> MetaOapg.properties.nameInVernacular: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["gender"]) -> MetaOapg.properties.gender: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["age"]) -> MetaOapg.properties.age: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["relativeName"]) -> MetaOapg.properties.relativeName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["relativeNameInVernacular"]) -> MetaOapg.properties.relativeNameInVernacular: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["relativeRelationType"]) -> MetaOapg.properties.relativeRelationType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["houseNumber"]) -> MetaOapg.properties.houseNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["partOrLocationInConstituency"]) -> MetaOapg.properties.partOrLocationInConstituency: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["partNumberOrLocationNumberInConstituency"]) -> MetaOapg.properties.partNumberOrLocationNumberInConstituency: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["parliamentaryConstituency"]) -> MetaOapg.properties.parliamentaryConstituency: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["assemblyConstituency"]) -> MetaOapg.properties.assemblyConstituency: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["sectionOfConstituencyPart"]) -> MetaOapg.properties.sectionOfConstituencyPart: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["cardSerialNumberInPollingList"]) -> MetaOapg.properties.cardSerialNumberInPollingList: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["lastUpdateDate"]) -> MetaOapg.properties.lastUpdateDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pollingBoothDetails"]) -> MetaOapg.properties.pollingBoothDetails: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["emailId"]) -> MetaOapg.properties.emailId: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["mobileNumber"]) -> MetaOapg.properties.mobileNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["stateCode"]) -> MetaOapg.properties.stateCode: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pollingBoothCoordinates"]) -> MetaOapg.properties.pollingBoothCoordinates: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pollingBoothAddress"]) -> MetaOapg.properties.pollingBoothAddress: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pollingBoothNumber"]) -> MetaOapg.properties.pollingBoothNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["blacklistStatus"]) -> MetaOapg.properties.blacklistStatus: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["registrationDate"]) -> MetaOapg.properties.registrationDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["registrationLocation"]) -> MetaOapg.properties.registrationLocation: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["class"]) -> MetaOapg.properties.propertyClass: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["maker"]) -> MetaOapg.properties.maker: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["ownerName"]) -> MetaOapg.properties.ownerName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["chassisNumber"]) -> MetaOapg.properties.chassisNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["registrationNumber"]) -> MetaOapg.properties.registrationNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["engineNumber"]) -> MetaOapg.properties.engineNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["fuelType"]) -> MetaOapg.properties.fuelType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["fitUpto"]) -> MetaOapg.properties.fitUpto: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["insuranceUpto"]) -> MetaOapg.properties.insuranceUpto: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["taxUpto"]) -> MetaOapg.properties.taxUpto: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["insuranceDetails"]) -> MetaOapg.properties.insuranceDetails: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["insuranceValidity"]) -> MetaOapg.properties.insuranceValidity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["permitType"]) -> MetaOapg.properties.permitType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["permitValidUpto"]) -> MetaOapg.properties.permitValidUpto: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pollutionControlValidity"]) -> MetaOapg.properties.pollutionControlValidity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pollutionNorms"]) -> MetaOapg.properties.pollutionNorms: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["licenseAddress"]) -> MetaOapg.properties.licenseAddress: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["registrationAddress"]) -> MetaOapg.properties.registrationAddress: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["ownerFatherName"]) -> MetaOapg.properties.ownerFatherName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["ownerPresentAddress"]) -> MetaOapg.properties.ownerPresentAddress: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["bodyType"]) -> MetaOapg.properties.bodyType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["category"]) -> MetaOapg.properties.category: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["color"]) -> MetaOapg.properties.color: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["engineCubicCapacity"]) -> MetaOapg.properties.engineCubicCapacity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["numberCylinders"]) -> MetaOapg.properties.numberCylinders: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["unladenWeight"]) -> MetaOapg.properties.unladenWeight: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["grossWeight"]) -> MetaOapg.properties.grossWeight: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["wheelbase"]) -> MetaOapg.properties.wheelbase: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["manufacturedMonthYear"]) -> MetaOapg.properties.manufacturedMonthYear: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["makerDescription"]) -> MetaOapg.properties.makerDescription: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["nocDetails"]) -> MetaOapg.properties.nocDetails: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["normsDescription"]) -> MetaOapg.properties.normsDescription: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["financier"]) -> MetaOapg.properties.financier: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["permitIssueDate"]) -> MetaOapg.properties.permitIssueDate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["permitNumber"]) -> MetaOapg.properties.permitNumber: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["permitValidFrom"]) -> MetaOapg.properties.permitValidFrom: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["seatingCapacity"]) -> MetaOapg.properties.seatingCapacity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["sleepingCapacity"]) -> MetaOapg.properties.sleepingCapacity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["standingCapacity"]) -> MetaOapg.properties.standingCapacity: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["statusAsOn"]) -> MetaOapg.properties.statusAsOn: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["primaryBusinessContact"]) -> MetaOapg.properties.primaryBusinessContact: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["stateJurisdiction"]) -> MetaOapg.properties.stateJurisdiction: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["stateJurisdictionCode"]) -> MetaOapg.properties.stateJurisdictionCode: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["taxpayerType"]) -> MetaOapg.properties.taxpayerType: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["constitutionOfBusiness"]) -> MetaOapg.properties.constitutionOfBusiness: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["gstnStatus"]) -> MetaOapg.properties.gstnStatus: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["tradeName"]) -> MetaOapg.properties.tradeName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["gstin"]) -> MetaOapg.properties.gstin: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["additionalPlacesOfBusinessInState"]) -> MetaOapg.properties.additionalPlacesOfBusinessInState: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["legalName"]) -> MetaOapg.properties.legalName: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["natureOfBusiness"]) -> MetaOapg.properties.natureOfBusiness: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["centralJurisdiction"]) -> MetaOapg.properties.centralJurisdiction: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["centralJurisdictionCode"]) -> MetaOapg.properties.centralJurisdictionCode: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pan"]) -> MetaOapg.properties.pan: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["authorizedSignatories"]) -> MetaOapg.properties.authorizedSignatories: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["complianceRating"]) -> MetaOapg.properties.complianceRating: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["cxdt"]) -> MetaOapg.properties.cxdt: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["businessDetails"]) -> MetaOapg.properties.businessDetails: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["annualAggregateTurnover"]) -> MetaOapg.properties.annualAggregateTurnover: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["mandatoryEInvoicing"]) -> MetaOapg.properties.mandatoryEInvoicing: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["grossTotalIncome"]) -> MetaOapg.properties.grossTotalIncome: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["grossTotalIncomeFinancialYear"]) -> MetaOapg.properties.grossTotalIncomeFinancialYear: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["isFieldVisitConducted"]) -> MetaOapg.properties.isFieldVisitConducted: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["filingStatus"]) -> MetaOapg.properties.filingStatus: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["directors"]) -> MetaOapg.properties.directors: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["companyMasterData"]) -> MetaOapg.properties.companyMasterData: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["charges"]) -> MetaOapg.properties.charges: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["llpData"]) -> MetaOapg.properties.llpData: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["companyData"]) -> MetaOapg.properties.companyData: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["directorData"]) -> MetaOapg.properties.directorData: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["llpMasterData"]) -> MetaOapg.properties.llpMasterData: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["foreignCompanyMasterData"]) -> MetaOapg.properties.foreignCompanyMasterData: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["idNumber", "idStatus", "name", "licenseType", "entityName", "status", "premissesAddress", "products", "address", "uamNumber", "enterpriseName", "majorActivity", "socialCategory", "enterpriseType", "dateOfCommencement", "district", "state", "appliedDate", "modifiedDate", "expiryDate", "nic_2Digit", "nic_4Digit", "nic_5Digit", "panStatus", "lastName", "firstName", "fullName", "idHolderTitle", "idLastUpdated", "aadhaarSeedingStatus", "addresses", "allClassOfVehicle", "drivingLicenseNumber", "dateOfBirth", "endorseDate", "endorseNumber", "fatherOrHusbandName", "validFrom", "validTo", "epicNo", "nameInVernacular", "gender", "age", "relativeName", "relativeNameInVernacular", "relativeRelationType", "houseNumber", "partOrLocationInConstituency", "partNumberOrLocationNumberInConstituency", "parliamentaryConstituency", "assemblyConstituency", "sectionOfConstituencyPart", "cardSerialNumberInPollingList", "lastUpdateDate", "pollingBoothDetails", "emailId", "mobileNumber", "stateCode", "pollingBoothCoordinates", "pollingBoothAddress", "pollingBoothNumber", "id", "blacklistStatus", "registrationDate", "registrationLocation", "class", "maker", "ownerName", "chassisNumber", "registrationNumber", "engineNumber", "fuelType", "fitUpto", "insuranceUpto", "taxUpto", "insuranceDetails", "insuranceValidity", "permitType", "permitValidUpto", "pollutionControlValidity", "pollutionNorms", "licenseAddress", "registrationAddress", "ownerFatherName", "ownerPresentAddress", "bodyType", "category", "color", "engineCubicCapacity", "numberCylinders", "unladenWeight", "grossWeight", "wheelbase", "manufacturedMonthYear", "makerDescription", "nocDetails", "normsDescription", "financier", "permitIssueDate", "permitNumber", "permitValidFrom", "seatingCapacity", "sleepingCapacity", "standingCapacity", "statusAsOn", "primaryBusinessContact", "stateJurisdiction", "stateJurisdictionCode", "taxpayerType", "constitutionOfBusiness", "gstnStatus", "tradeName", "gstin", "additionalPlacesOfBusinessInState", "legalName", "natureOfBusiness", "centralJurisdiction", "centralJurisdictionCode", "pan", "authorizedSignatories", "complianceRating", "cxdt", "businessDetails", "annualAggregateTurnover", "mandatoryEInvoicing", "grossTotalIncome", "grossTotalIncomeFinancialYear", "isFieldVisitConducted", "filingStatus", "directors", "companyMasterData", "charges", "llpData", "companyData", "directorData", "llpMasterData", "foreignCompanyMasterData", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["idNumber"]) -> typing.Union[MetaOapg.properties.idNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["idStatus"]) -> typing.Union[MetaOapg.properties.idStatus, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["licenseType"]) -> typing.Union[MetaOapg.properties.licenseType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["entityName"]) -> typing.Union[MetaOapg.properties.entityName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["premissesAddress"]) -> typing.Union[MetaOapg.properties.premissesAddress, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["products"]) -> typing.Union[MetaOapg.properties.products, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["uamNumber"]) -> typing.Union[MetaOapg.properties.uamNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["enterpriseName"]) -> typing.Union[MetaOapg.properties.enterpriseName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["majorActivity"]) -> typing.Union[MetaOapg.properties.majorActivity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["socialCategory"]) -> typing.Union[MetaOapg.properties.socialCategory, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["enterpriseType"]) -> typing.Union[MetaOapg.properties.enterpriseType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["dateOfCommencement"]) -> typing.Union[MetaOapg.properties.dateOfCommencement, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["district"]) -> typing.Union[MetaOapg.properties.district, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union[MetaOapg.properties.state, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["appliedDate"]) -> typing.Union[MetaOapg.properties.appliedDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["modifiedDate"]) -> typing.Union[MetaOapg.properties.modifiedDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["expiryDate"]) -> typing.Union[MetaOapg.properties.expiryDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["nic_2Digit"]) -> typing.Union[MetaOapg.properties.nic_2Digit, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["nic_4Digit"]) -> typing.Union[MetaOapg.properties.nic_4Digit, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["nic_5Digit"]) -> typing.Union[MetaOapg.properties.nic_5Digit, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["panStatus"]) -> typing.Union[MetaOapg.properties.panStatus, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["lastName"]) -> typing.Union[MetaOapg.properties.lastName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["firstName"]) -> typing.Union[MetaOapg.properties.firstName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["fullName"]) -> typing.Union[MetaOapg.properties.fullName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["idHolderTitle"]) -> typing.Union[MetaOapg.properties.idHolderTitle, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["idLastUpdated"]) -> typing.Union[MetaOapg.properties.idLastUpdated, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["aadhaarSeedingStatus"]) -> typing.Union[MetaOapg.properties.aadhaarSeedingStatus, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["addresses"]) -> typing.Union[MetaOapg.properties.addresses, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["allClassOfVehicle"]) -> typing.Union[MetaOapg.properties.allClassOfVehicle, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["drivingLicenseNumber"]) -> typing.Union[MetaOapg.properties.drivingLicenseNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["dateOfBirth"]) -> typing.Union[MetaOapg.properties.dateOfBirth, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["endorseDate"]) -> typing.Union[MetaOapg.properties.endorseDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["endorseNumber"]) -> typing.Union[MetaOapg.properties.endorseNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["fatherOrHusbandName"]) -> typing.Union[MetaOapg.properties.fatherOrHusbandName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["validFrom"]) -> typing.Union[MetaOapg.properties.validFrom, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["validTo"]) -> typing.Union[MetaOapg.properties.validTo, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["epicNo"]) -> typing.Union[MetaOapg.properties.epicNo, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["nameInVernacular"]) -> typing.Union[MetaOapg.properties.nameInVernacular, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["gender"]) -> typing.Union[MetaOapg.properties.gender, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["age"]) -> typing.Union[MetaOapg.properties.age, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["relativeName"]) -> typing.Union[MetaOapg.properties.relativeName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["relativeNameInVernacular"]) -> typing.Union[MetaOapg.properties.relativeNameInVernacular, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["relativeRelationType"]) -> typing.Union[MetaOapg.properties.relativeRelationType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["houseNumber"]) -> typing.Union[MetaOapg.properties.houseNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["partOrLocationInConstituency"]) -> typing.Union[MetaOapg.properties.partOrLocationInConstituency, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["partNumberOrLocationNumberInConstituency"]) -> typing.Union[MetaOapg.properties.partNumberOrLocationNumberInConstituency, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["parliamentaryConstituency"]) -> typing.Union[MetaOapg.properties.parliamentaryConstituency, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["assemblyConstituency"]) -> typing.Union[MetaOapg.properties.assemblyConstituency, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["sectionOfConstituencyPart"]) -> typing.Union[MetaOapg.properties.sectionOfConstituencyPart, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["cardSerialNumberInPollingList"]) -> typing.Union[MetaOapg.properties.cardSerialNumberInPollingList, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["lastUpdateDate"]) -> typing.Union[MetaOapg.properties.lastUpdateDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pollingBoothDetails"]) -> typing.Union[MetaOapg.properties.pollingBoothDetails, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["emailId"]) -> typing.Union[MetaOapg.properties.emailId, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["mobileNumber"]) -> typing.Union[MetaOapg.properties.mobileNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["stateCode"]) -> typing.Union[MetaOapg.properties.stateCode, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pollingBoothCoordinates"]) -> typing.Union[MetaOapg.properties.pollingBoothCoordinates, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pollingBoothAddress"]) -> typing.Union[MetaOapg.properties.pollingBoothAddress, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pollingBoothNumber"]) -> typing.Union[MetaOapg.properties.pollingBoothNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["blacklistStatus"]) -> typing.Union[MetaOapg.properties.blacklistStatus, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["registrationDate"]) -> typing.Union[MetaOapg.properties.registrationDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["registrationLocation"]) -> typing.Union[MetaOapg.properties.registrationLocation, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["class"]) -> typing.Union[MetaOapg.properties.propertyClass, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["maker"]) -> typing.Union[MetaOapg.properties.maker, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["ownerName"]) -> typing.Union[MetaOapg.properties.ownerName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["chassisNumber"]) -> typing.Union[MetaOapg.properties.chassisNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["registrationNumber"]) -> typing.Union[MetaOapg.properties.registrationNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["engineNumber"]) -> typing.Union[MetaOapg.properties.engineNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["fuelType"]) -> typing.Union[MetaOapg.properties.fuelType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["fitUpto"]) -> typing.Union[MetaOapg.properties.fitUpto, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["insuranceUpto"]) -> typing.Union[MetaOapg.properties.insuranceUpto, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["taxUpto"]) -> typing.Union[MetaOapg.properties.taxUpto, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["insuranceDetails"]) -> typing.Union[MetaOapg.properties.insuranceDetails, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["insuranceValidity"]) -> typing.Union[MetaOapg.properties.insuranceValidity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["permitType"]) -> typing.Union[MetaOapg.properties.permitType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["permitValidUpto"]) -> typing.Union[MetaOapg.properties.permitValidUpto, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pollutionControlValidity"]) -> typing.Union[MetaOapg.properties.pollutionControlValidity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pollutionNorms"]) -> typing.Union[MetaOapg.properties.pollutionNorms, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["licenseAddress"]) -> typing.Union[MetaOapg.properties.licenseAddress, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["registrationAddress"]) -> typing.Union[MetaOapg.properties.registrationAddress, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["ownerFatherName"]) -> typing.Union[MetaOapg.properties.ownerFatherName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["ownerPresentAddress"]) -> typing.Union[MetaOapg.properties.ownerPresentAddress, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["bodyType"]) -> typing.Union[MetaOapg.properties.bodyType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["category"]) -> typing.Union[MetaOapg.properties.category, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["color"]) -> typing.Union[MetaOapg.properties.color, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["engineCubicCapacity"]) -> typing.Union[MetaOapg.properties.engineCubicCapacity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["numberCylinders"]) -> typing.Union[MetaOapg.properties.numberCylinders, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["unladenWeight"]) -> typing.Union[MetaOapg.properties.unladenWeight, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["grossWeight"]) -> typing.Union[MetaOapg.properties.grossWeight, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["wheelbase"]) -> typing.Union[MetaOapg.properties.wheelbase, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["manufacturedMonthYear"]) -> typing.Union[MetaOapg.properties.manufacturedMonthYear, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["makerDescription"]) -> typing.Union[MetaOapg.properties.makerDescription, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["nocDetails"]) -> typing.Union[MetaOapg.properties.nocDetails, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["normsDescription"]) -> typing.Union[MetaOapg.properties.normsDescription, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["financier"]) -> typing.Union[MetaOapg.properties.financier, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["permitIssueDate"]) -> typing.Union[MetaOapg.properties.permitIssueDate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["permitNumber"]) -> typing.Union[MetaOapg.properties.permitNumber, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["permitValidFrom"]) -> typing.Union[MetaOapg.properties.permitValidFrom, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["seatingCapacity"]) -> typing.Union[MetaOapg.properties.seatingCapacity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["sleepingCapacity"]) -> typing.Union[MetaOapg.properties.sleepingCapacity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["standingCapacity"]) -> typing.Union[MetaOapg.properties.standingCapacity, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["statusAsOn"]) -> typing.Union[MetaOapg.properties.statusAsOn, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["primaryBusinessContact"]) -> typing.Union[MetaOapg.properties.primaryBusinessContact, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["stateJurisdiction"]) -> typing.Union[MetaOapg.properties.stateJurisdiction, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["stateJurisdictionCode"]) -> typing.Union[MetaOapg.properties.stateJurisdictionCode, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["taxpayerType"]) -> typing.Union[MetaOapg.properties.taxpayerType, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["constitutionOfBusiness"]) -> typing.Union[MetaOapg.properties.constitutionOfBusiness, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["gstnStatus"]) -> typing.Union[MetaOapg.properties.gstnStatus, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["tradeName"]) -> typing.Union[MetaOapg.properties.tradeName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["gstin"]) -> typing.Union[MetaOapg.properties.gstin, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["additionalPlacesOfBusinessInState"]) -> typing.Union[MetaOapg.properties.additionalPlacesOfBusinessInState, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["legalName"]) -> typing.Union[MetaOapg.properties.legalName, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["natureOfBusiness"]) -> typing.Union[MetaOapg.properties.natureOfBusiness, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["centralJurisdiction"]) -> typing.Union[MetaOapg.properties.centralJurisdiction, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["centralJurisdictionCode"]) -> typing.Union[MetaOapg.properties.centralJurisdictionCode, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pan"]) -> typing.Union[MetaOapg.properties.pan, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["authorizedSignatories"]) -> typing.Union[MetaOapg.properties.authorizedSignatories, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["complianceRating"]) -> typing.Union[MetaOapg.properties.complianceRating, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["cxdt"]) -> typing.Union[MetaOapg.properties.cxdt, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["businessDetails"]) -> typing.Union[MetaOapg.properties.businessDetails, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["annualAggregateTurnover"]) -> typing.Union[MetaOapg.properties.annualAggregateTurnover, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["mandatoryEInvoicing"]) -> typing.Union[MetaOapg.properties.mandatoryEInvoicing, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["grossTotalIncome"]) -> typing.Union[MetaOapg.properties.grossTotalIncome, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["grossTotalIncomeFinancialYear"]) -> typing.Union[MetaOapg.properties.grossTotalIncomeFinancialYear, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["isFieldVisitConducted"]) -> typing.Union[MetaOapg.properties.isFieldVisitConducted, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["filingStatus"]) -> typing.Union[MetaOapg.properties.filingStatus, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["directors"]) -> typing.Union[MetaOapg.properties.directors, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["companyMasterData"]) -> typing.Union[MetaOapg.properties.companyMasterData, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["charges"]) -> typing.Union[MetaOapg.properties.charges, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["llpData"]) -> typing.Union[MetaOapg.properties.llpData, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["companyData"]) -> typing.Union[MetaOapg.properties.companyData, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["directorData"]) -> typing.Union[MetaOapg.properties.directorData, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["llpMasterData"]) -> typing.Union[MetaOapg.properties.llpMasterData, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["foreignCompanyMasterData"]) -> typing.Union[MetaOapg.properties.foreignCompanyMasterData, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["idNumber", "idStatus", "name", "licenseType", "entityName", "status", "premissesAddress", "products", "address", "uamNumber", "enterpriseName", "majorActivity", "socialCategory", "enterpriseType", "dateOfCommencement", "district", "state", "appliedDate", "modifiedDate", "expiryDate", "nic_2Digit", "nic_4Digit", "nic_5Digit", "panStatus", "lastName", "firstName", "fullName", "idHolderTitle", "idLastUpdated", "aadhaarSeedingStatus", "addresses", "allClassOfVehicle", "drivingLicenseNumber", "dateOfBirth", "endorseDate", "endorseNumber", "fatherOrHusbandName", "validFrom", "validTo", "epicNo", "nameInVernacular", "gender", "age", "relativeName", "relativeNameInVernacular", "relativeRelationType", "houseNumber", "partOrLocationInConstituency", "partNumberOrLocationNumberInConstituency", "parliamentaryConstituency", "assemblyConstituency", "sectionOfConstituencyPart", "cardSerialNumberInPollingList", "lastUpdateDate", "pollingBoothDetails", "emailId", "mobileNumber", "stateCode", "pollingBoothCoordinates", "pollingBoothAddress", "pollingBoothNumber", "id", "blacklistStatus", "registrationDate", "registrationLocation", "class", "maker", "ownerName", "chassisNumber", "registrationNumber", "engineNumber", "fuelType", "fitUpto", "insuranceUpto", "taxUpto", "insuranceDetails", "insuranceValidity", "permitType", "permitValidUpto", "pollutionControlValidity", "pollutionNorms", "licenseAddress", "registrationAddress", "ownerFatherName", "ownerPresentAddress", "bodyType", "category", "color", "engineCubicCapacity", "numberCylinders", "unladenWeight", "grossWeight", "wheelbase", "manufacturedMonthYear", "makerDescription", "nocDetails", "normsDescription", "financier", "permitIssueDate", "permitNumber", "permitValidFrom", "seatingCapacity", "sleepingCapacity", "standingCapacity", "statusAsOn", "primaryBusinessContact", "stateJurisdiction", "stateJurisdictionCode", "taxpayerType", "constitutionOfBusiness", "gstnStatus", "tradeName", "gstin", "additionalPlacesOfBusinessInState", "legalName", "natureOfBusiness", "centralJurisdiction", "centralJurisdictionCode", "pan", "authorizedSignatories", "complianceRating", "cxdt", "businessDetails", "annualAggregateTurnover", "mandatoryEInvoicing", "grossTotalIncome", "grossTotalIncomeFinancialYear", "isFieldVisitConducted", "filingStatus", "directors", "companyMasterData", "charges", "llpData", "companyData", "directorData", "llpMasterData", "foreignCompanyMasterData", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, ],
                    idNumber: typing.Union[MetaOapg.properties.idNumber, str, schemas.Unset] = schemas.unset,
                    idStatus: typing.Union[MetaOapg.properties.idStatus, str, schemas.Unset] = schemas.unset,
                    name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
                    licenseType: typing.Union[MetaOapg.properties.licenseType, str, schemas.Unset] = schemas.unset,
                    entityName: typing.Union[MetaOapg.properties.entityName, str, schemas.Unset] = schemas.unset,
                    status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
                    premissesAddress: typing.Union[MetaOapg.properties.premissesAddress, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    products: typing.Union[MetaOapg.properties.products, list, tuple, schemas.Unset] = schemas.unset,
                    address: typing.Union[MetaOapg.properties.address, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    uamNumber: typing.Union[MetaOapg.properties.uamNumber, str, schemas.Unset] = schemas.unset,
                    enterpriseName: typing.Union[MetaOapg.properties.enterpriseName, str, schemas.Unset] = schemas.unset,
                    majorActivity: typing.Union[MetaOapg.properties.majorActivity, str, schemas.Unset] = schemas.unset,
                    socialCategory: typing.Union[MetaOapg.properties.socialCategory, str, schemas.Unset] = schemas.unset,
                    enterpriseType: typing.Union[MetaOapg.properties.enterpriseType, str, schemas.Unset] = schemas.unset,
                    dateOfCommencement: typing.Union[MetaOapg.properties.dateOfCommencement, str, schemas.Unset] = schemas.unset,
                    district: typing.Union[MetaOapg.properties.district, str, schemas.Unset] = schemas.unset,
                    state: typing.Union[MetaOapg.properties.state, str, schemas.Unset] = schemas.unset,
                    appliedDate: typing.Union[MetaOapg.properties.appliedDate, str, schemas.Unset] = schemas.unset,
                    modifiedDate: typing.Union[MetaOapg.properties.modifiedDate, str, schemas.Unset] = schemas.unset,
                    expiryDate: typing.Union[MetaOapg.properties.expiryDate, str, schemas.Unset] = schemas.unset,
                    nic_2Digit: typing.Union[MetaOapg.properties.nic_2Digit, str, schemas.Unset] = schemas.unset,
                    nic_4Digit: typing.Union[MetaOapg.properties.nic_4Digit, str, schemas.Unset] = schemas.unset,
                    nic_5Digit: typing.Union[MetaOapg.properties.nic_5Digit, str, schemas.Unset] = schemas.unset,
                    panStatus: typing.Union[MetaOapg.properties.panStatus, str, schemas.Unset] = schemas.unset,
                    lastName: typing.Union[MetaOapg.properties.lastName, str, schemas.Unset] = schemas.unset,
                    firstName: typing.Union[MetaOapg.properties.firstName, str, schemas.Unset] = schemas.unset,
                    fullName: typing.Union[MetaOapg.properties.fullName, str, schemas.Unset] = schemas.unset,
                    idHolderTitle: typing.Union[MetaOapg.properties.idHolderTitle, str, schemas.Unset] = schemas.unset,
                    idLastUpdated: typing.Union[MetaOapg.properties.idLastUpdated, str, schemas.Unset] = schemas.unset,
                    aadhaarSeedingStatus: typing.Union[MetaOapg.properties.aadhaarSeedingStatus, str, schemas.Unset] = schemas.unset,
                    addresses: typing.Union[MetaOapg.properties.addresses, list, tuple, schemas.Unset] = schemas.unset,
                    allClassOfVehicle: typing.Union[MetaOapg.properties.allClassOfVehicle, list, tuple, schemas.Unset] = schemas.unset,
                    drivingLicenseNumber: typing.Union[MetaOapg.properties.drivingLicenseNumber, str, schemas.Unset] = schemas.unset,
                    dateOfBirth: typing.Union[MetaOapg.properties.dateOfBirth, str, schemas.Unset] = schemas.unset,
                    endorseDate: typing.Union[MetaOapg.properties.endorseDate, str, schemas.Unset] = schemas.unset,
                    endorseNumber: typing.Union[MetaOapg.properties.endorseNumber, str, schemas.Unset] = schemas.unset,
                    fatherOrHusbandName: typing.Union[MetaOapg.properties.fatherOrHusbandName, str, schemas.Unset] = schemas.unset,
                    validFrom: typing.Union[MetaOapg.properties.validFrom, str, schemas.Unset] = schemas.unset,
                    validTo: typing.Union[MetaOapg.properties.validTo, str, schemas.Unset] = schemas.unset,
                    epicNo: typing.Union[MetaOapg.properties.epicNo, str, schemas.Unset] = schemas.unset,
                    nameInVernacular: typing.Union[MetaOapg.properties.nameInVernacular, str, schemas.Unset] = schemas.unset,
                    gender: typing.Union[MetaOapg.properties.gender, str, schemas.Unset] = schemas.unset,
                    age: typing.Union[MetaOapg.properties.age, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                    relativeName: typing.Union[MetaOapg.properties.relativeName, str, schemas.Unset] = schemas.unset,
                    relativeNameInVernacular: typing.Union[MetaOapg.properties.relativeNameInVernacular, str, schemas.Unset] = schemas.unset,
                    relativeRelationType: typing.Union[MetaOapg.properties.relativeRelationType, str, schemas.Unset] = schemas.unset,
                    houseNumber: typing.Union[MetaOapg.properties.houseNumber, str, schemas.Unset] = schemas.unset,
                    partOrLocationInConstituency: typing.Union[MetaOapg.properties.partOrLocationInConstituency, str, schemas.Unset] = schemas.unset,
                    partNumberOrLocationNumberInConstituency: typing.Union[MetaOapg.properties.partNumberOrLocationNumberInConstituency, str, schemas.Unset] = schemas.unset,
                    parliamentaryConstituency: typing.Union[MetaOapg.properties.parliamentaryConstituency, str, schemas.Unset] = schemas.unset,
                    assemblyConstituency: typing.Union[MetaOapg.properties.assemblyConstituency, str, schemas.Unset] = schemas.unset,
                    sectionOfConstituencyPart: typing.Union[MetaOapg.properties.sectionOfConstituencyPart, str, schemas.Unset] = schemas.unset,
                    cardSerialNumberInPollingList: typing.Union[MetaOapg.properties.cardSerialNumberInPollingList, str, schemas.Unset] = schemas.unset,
                    lastUpdateDate: typing.Union[MetaOapg.properties.lastUpdateDate, str, schemas.Unset] = schemas.unset,
                    pollingBoothDetails: typing.Union[MetaOapg.properties.pollingBoothDetails, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    emailId: typing.Union[MetaOapg.properties.emailId, str, schemas.Unset] = schemas.unset,
                    mobileNumber: typing.Union[MetaOapg.properties.mobileNumber, str, schemas.Unset] = schemas.unset,
                    stateCode: typing.Union[MetaOapg.properties.stateCode, str, schemas.Unset] = schemas.unset,
                    pollingBoothCoordinates: typing.Union[MetaOapg.properties.pollingBoothCoordinates, str, schemas.Unset] = schemas.unset,
                    pollingBoothAddress: typing.Union[MetaOapg.properties.pollingBoothAddress, str, schemas.Unset] = schemas.unset,
                    pollingBoothNumber: typing.Union[MetaOapg.properties.pollingBoothNumber, str, schemas.Unset] = schemas.unset,
                    id: typing.Union[MetaOapg.properties.id, str, schemas.Unset] = schemas.unset,
                    blacklistStatus: typing.Union[MetaOapg.properties.blacklistStatus, str, schemas.Unset] = schemas.unset,
                    registrationDate: typing.Union[MetaOapg.properties.registrationDate, str, schemas.Unset] = schemas.unset,
                    registrationLocation: typing.Union[MetaOapg.properties.registrationLocation, str, schemas.Unset] = schemas.unset,
                    maker: typing.Union[MetaOapg.properties.maker, str, schemas.Unset] = schemas.unset,
                    ownerName: typing.Union[MetaOapg.properties.ownerName, str, schemas.Unset] = schemas.unset,
                    chassisNumber: typing.Union[MetaOapg.properties.chassisNumber, str, schemas.Unset] = schemas.unset,
                    registrationNumber: typing.Union[MetaOapg.properties.registrationNumber, str, schemas.Unset] = schemas.unset,
                    engineNumber: typing.Union[MetaOapg.properties.engineNumber, str, schemas.Unset] = schemas.unset,
                    fuelType: typing.Union[MetaOapg.properties.fuelType, str, schemas.Unset] = schemas.unset,
                    fitUpto: typing.Union[MetaOapg.properties.fitUpto, str, schemas.Unset] = schemas.unset,
                    insuranceUpto: typing.Union[MetaOapg.properties.insuranceUpto, str, schemas.Unset] = schemas.unset,
                    taxUpto: typing.Union[MetaOapg.properties.taxUpto, str, schemas.Unset] = schemas.unset,
                    insuranceDetails: typing.Union[MetaOapg.properties.insuranceDetails, str, schemas.Unset] = schemas.unset,
                    insuranceValidity: typing.Union[MetaOapg.properties.insuranceValidity, str, schemas.Unset] = schemas.unset,
                    permitType: typing.Union[MetaOapg.properties.permitType, str, schemas.Unset] = schemas.unset,
                    permitValidUpto: typing.Union[MetaOapg.properties.permitValidUpto, str, schemas.Unset] = schemas.unset,
                    pollutionControlValidity: typing.Union[MetaOapg.properties.pollutionControlValidity, str, schemas.Unset] = schemas.unset,
                    pollutionNorms: typing.Union[MetaOapg.properties.pollutionNorms, str, schemas.Unset] = schemas.unset,
                    licenseAddress: typing.Union[MetaOapg.properties.licenseAddress, str, schemas.Unset] = schemas.unset,
                    registrationAddress: typing.Union[MetaOapg.properties.registrationAddress, str, schemas.Unset] = schemas.unset,
                    ownerFatherName: typing.Union[MetaOapg.properties.ownerFatherName, str, schemas.Unset] = schemas.unset,
                    ownerPresentAddress: typing.Union[MetaOapg.properties.ownerPresentAddress, str, schemas.Unset] = schemas.unset,
                    bodyType: typing.Union[MetaOapg.properties.bodyType, str, schemas.Unset] = schemas.unset,
                    category: typing.Union[MetaOapg.properties.category, str, schemas.Unset] = schemas.unset,
                    color: typing.Union[MetaOapg.properties.color, str, schemas.Unset] = schemas.unset,
                    engineCubicCapacity: typing.Union[MetaOapg.properties.engineCubicCapacity, str, schemas.Unset] = schemas.unset,
                    numberCylinders: typing.Union[MetaOapg.properties.numberCylinders, str, schemas.Unset] = schemas.unset,
                    unladenWeight: typing.Union[MetaOapg.properties.unladenWeight, str, schemas.Unset] = schemas.unset,
                    grossWeight: typing.Union[MetaOapg.properties.grossWeight, str, schemas.Unset] = schemas.unset,
                    wheelbase: typing.Union[MetaOapg.properties.wheelbase, str, schemas.Unset] = schemas.unset,
                    manufacturedMonthYear: typing.Union[MetaOapg.properties.manufacturedMonthYear, str, schemas.Unset] = schemas.unset,
                    makerDescription: typing.Union[MetaOapg.properties.makerDescription, str, schemas.Unset] = schemas.unset,
                    nocDetails: typing.Union[MetaOapg.properties.nocDetails, str, schemas.Unset] = schemas.unset,
                    normsDescription: typing.Union[MetaOapg.properties.normsDescription, str, schemas.Unset] = schemas.unset,
                    financier: typing.Union[MetaOapg.properties.financier, str, schemas.Unset] = schemas.unset,
                    permitIssueDate: typing.Union[MetaOapg.properties.permitIssueDate, str, schemas.Unset] = schemas.unset,
                    permitNumber: typing.Union[MetaOapg.properties.permitNumber, str, schemas.Unset] = schemas.unset,
                    permitValidFrom: typing.Union[MetaOapg.properties.permitValidFrom, str, schemas.Unset] = schemas.unset,
                    seatingCapacity: typing.Union[MetaOapg.properties.seatingCapacity, str, schemas.Unset] = schemas.unset,
                    sleepingCapacity: typing.Union[MetaOapg.properties.sleepingCapacity, str, schemas.Unset] = schemas.unset,
                    standingCapacity: typing.Union[MetaOapg.properties.standingCapacity, str, schemas.Unset] = schemas.unset,
                    statusAsOn: typing.Union[MetaOapg.properties.statusAsOn, str, schemas.Unset] = schemas.unset,
                    primaryBusinessContact: typing.Union[MetaOapg.properties.primaryBusinessContact, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    stateJurisdiction: typing.Union[MetaOapg.properties.stateJurisdiction, str, schemas.Unset] = schemas.unset,
                    stateJurisdictionCode: typing.Union[MetaOapg.properties.stateJurisdictionCode, str, schemas.Unset] = schemas.unset,
                    taxpayerType: typing.Union[MetaOapg.properties.taxpayerType, str, schemas.Unset] = schemas.unset,
                    constitutionOfBusiness: typing.Union[MetaOapg.properties.constitutionOfBusiness, str, schemas.Unset] = schemas.unset,
                    gstnStatus: typing.Union[MetaOapg.properties.gstnStatus, str, schemas.Unset] = schemas.unset,
                    tradeName: typing.Union[MetaOapg.properties.tradeName, str, schemas.Unset] = schemas.unset,
                    gstin: typing.Union[MetaOapg.properties.gstin, str, schemas.Unset] = schemas.unset,
                    additionalPlacesOfBusinessInState: typing.Union[MetaOapg.properties.additionalPlacesOfBusinessInState, list, tuple, schemas.Unset] = schemas.unset,
                    legalName: typing.Union[MetaOapg.properties.legalName, str, schemas.Unset] = schemas.unset,
                    natureOfBusiness: typing.Union[MetaOapg.properties.natureOfBusiness, list, tuple, schemas.Unset] = schemas.unset,
                    centralJurisdiction: typing.Union[MetaOapg.properties.centralJurisdiction, str, schemas.Unset] = schemas.unset,
                    centralJurisdictionCode: typing.Union[MetaOapg.properties.centralJurisdictionCode, str, schemas.Unset] = schemas.unset,
                    pan: typing.Union[MetaOapg.properties.pan, str, schemas.Unset] = schemas.unset,
                    authorizedSignatories: typing.Union[MetaOapg.properties.authorizedSignatories, str, schemas.Unset] = schemas.unset,
                    complianceRating: typing.Union[MetaOapg.properties.complianceRating, str, schemas.Unset] = schemas.unset,
                    cxdt: typing.Union[MetaOapg.properties.cxdt, str, schemas.Unset] = schemas.unset,
                    businessDetails: typing.Union[MetaOapg.properties.businessDetails, list, tuple, schemas.Unset] = schemas.unset,
                    annualAggregateTurnover: typing.Union[MetaOapg.properties.annualAggregateTurnover, str, schemas.Unset] = schemas.unset,
                    mandatoryEInvoicing: typing.Union[MetaOapg.properties.mandatoryEInvoicing, str, schemas.Unset] = schemas.unset,
                    grossTotalIncome: typing.Union[MetaOapg.properties.grossTotalIncome, str, schemas.Unset] = schemas.unset,
                    grossTotalIncomeFinancialYear: typing.Union[MetaOapg.properties.grossTotalIncomeFinancialYear, str, schemas.Unset] = schemas.unset,
                    isFieldVisitConducted: typing.Union[MetaOapg.properties.isFieldVisitConducted, str, schemas.Unset] = schemas.unset,
                    filingStatus: typing.Union[MetaOapg.properties.filingStatus, list, tuple, schemas.Unset] = schemas.unset,
                    directors: typing.Union[MetaOapg.properties.directors, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
                    companyMasterData: typing.Union[MetaOapg.properties.companyMasterData, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    charges: typing.Union[MetaOapg.properties.charges, list, tuple, schemas.Unset] = schemas.unset,
                    llpData: typing.Union[MetaOapg.properties.llpData, list, tuple, schemas.Unset] = schemas.unset,
                    companyData: typing.Union[MetaOapg.properties.companyData, list, tuple, schemas.Unset] = schemas.unset,
                    directorData: typing.Union[MetaOapg.properties.directorData, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    llpMasterData: typing.Union[MetaOapg.properties.llpMasterData, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    foreignCompanyMasterData: typing.Union[MetaOapg.properties.foreignCompanyMasterData, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'kycResult':
                    return super().__new__(
                        cls,
                        *args,
                        idNumber=idNumber,
                        idStatus=idStatus,
                        name=name,
                        licenseType=licenseType,
                        entityName=entityName,
                        status=status,
                        premissesAddress=premissesAddress,
                        products=products,
                        address=address,
                        uamNumber=uamNumber,
                        enterpriseName=enterpriseName,
                        majorActivity=majorActivity,
                        socialCategory=socialCategory,
                        enterpriseType=enterpriseType,
                        dateOfCommencement=dateOfCommencement,
                        district=district,
                        state=state,
                        appliedDate=appliedDate,
                        modifiedDate=modifiedDate,
                        expiryDate=expiryDate,
                        nic_2Digit=nic_2Digit,
                        nic_4Digit=nic_4Digit,
                        nic_5Digit=nic_5Digit,
                        panStatus=panStatus,
                        lastName=lastName,
                        firstName=firstName,
                        fullName=fullName,
                        idHolderTitle=idHolderTitle,
                        idLastUpdated=idLastUpdated,
                        aadhaarSeedingStatus=aadhaarSeedingStatus,
                        addresses=addresses,
                        allClassOfVehicle=allClassOfVehicle,
                        drivingLicenseNumber=drivingLicenseNumber,
                        dateOfBirth=dateOfBirth,
                        endorseDate=endorseDate,
                        endorseNumber=endorseNumber,
                        fatherOrHusbandName=fatherOrHusbandName,
                        validFrom=validFrom,
                        validTo=validTo,
                        epicNo=epicNo,
                        nameInVernacular=nameInVernacular,
                        gender=gender,
                        age=age,
                        relativeName=relativeName,
                        relativeNameInVernacular=relativeNameInVernacular,
                        relativeRelationType=relativeRelationType,
                        houseNumber=houseNumber,
                        partOrLocationInConstituency=partOrLocationInConstituency,
                        partNumberOrLocationNumberInConstituency=partNumberOrLocationNumberInConstituency,
                        parliamentaryConstituency=parliamentaryConstituency,
                        assemblyConstituency=assemblyConstituency,
                        sectionOfConstituencyPart=sectionOfConstituencyPart,
                        cardSerialNumberInPollingList=cardSerialNumberInPollingList,
                        lastUpdateDate=lastUpdateDate,
                        pollingBoothDetails=pollingBoothDetails,
                        emailId=emailId,
                        mobileNumber=mobileNumber,
                        stateCode=stateCode,
                        pollingBoothCoordinates=pollingBoothCoordinates,
                        pollingBoothAddress=pollingBoothAddress,
                        pollingBoothNumber=pollingBoothNumber,
                        id=id,
                        blacklistStatus=blacklistStatus,
                        registrationDate=registrationDate,
                        registrationLocation=registrationLocation,
                        maker=maker,
                        ownerName=ownerName,
                        chassisNumber=chassisNumber,
                        registrationNumber=registrationNumber,
                        engineNumber=engineNumber,
                        fuelType=fuelType,
                        fitUpto=fitUpto,
                        insuranceUpto=insuranceUpto,
                        taxUpto=taxUpto,
                        insuranceDetails=insuranceDetails,
                        insuranceValidity=insuranceValidity,
                        permitType=permitType,
                        permitValidUpto=permitValidUpto,
                        pollutionControlValidity=pollutionControlValidity,
                        pollutionNorms=pollutionNorms,
                        licenseAddress=licenseAddress,
                        registrationAddress=registrationAddress,
                        ownerFatherName=ownerFatherName,
                        ownerPresentAddress=ownerPresentAddress,
                        bodyType=bodyType,
                        category=category,
                        color=color,
                        engineCubicCapacity=engineCubicCapacity,
                        numberCylinders=numberCylinders,
                        unladenWeight=unladenWeight,
                        grossWeight=grossWeight,
                        wheelbase=wheelbase,
                        manufacturedMonthYear=manufacturedMonthYear,
                        makerDescription=makerDescription,
                        nocDetails=nocDetails,
                        normsDescription=normsDescription,
                        financier=financier,
                        permitIssueDate=permitIssueDate,
                        permitNumber=permitNumber,
                        permitValidFrom=permitValidFrom,
                        seatingCapacity=seatingCapacity,
                        sleepingCapacity=sleepingCapacity,
                        standingCapacity=standingCapacity,
                        statusAsOn=statusAsOn,
                        primaryBusinessContact=primaryBusinessContact,
                        stateJurisdiction=stateJurisdiction,
                        stateJurisdictionCode=stateJurisdictionCode,
                        taxpayerType=taxpayerType,
                        constitutionOfBusiness=constitutionOfBusiness,
                        gstnStatus=gstnStatus,
                        tradeName=tradeName,
                        gstin=gstin,
                        additionalPlacesOfBusinessInState=additionalPlacesOfBusinessInState,
                        legalName=legalName,
                        natureOfBusiness=natureOfBusiness,
                        centralJurisdiction=centralJurisdiction,
                        centralJurisdictionCode=centralJurisdictionCode,
                        pan=pan,
                        authorizedSignatories=authorizedSignatories,
                        complianceRating=complianceRating,
                        cxdt=cxdt,
                        businessDetails=businessDetails,
                        annualAggregateTurnover=annualAggregateTurnover,
                        mandatoryEInvoicing=mandatoryEInvoicing,
                        grossTotalIncome=grossTotalIncome,
                        grossTotalIncomeFinancialYear=grossTotalIncomeFinancialYear,
                        isFieldVisitConducted=isFieldVisitConducted,
                        filingStatus=filingStatus,
                        directors=directors,
                        companyMasterData=companyMasterData,
                        charges=charges,
                        llpData=llpData,
                        companyData=companyData,
                        directorData=directorData,
                        llpMasterData=llpMasterData,
                        foreignCompanyMasterData=foreignCompanyMasterData,
                        _configuration=_configuration,
                        **kwargs,
                    )
            responseCode = schemas.StrSchema
            requestTimestamp = schemas.StrSchema
            responseTimestamp = schemas.StrSchema
            decentroTxnId = schemas.StrSchema
            
            
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
            __annotations__ = {
                "kycStatus": kycStatus,
                "status": status,
                "message": message,
                "kycResult": kycResult,
                "responseCode": responseCode,
                "requestTimestamp": requestTimestamp,
                "responseTimestamp": responseTimestamp,
                "decentroTxnId": decentroTxnId,
                "error": error,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["kycStatus"]) -> MetaOapg.properties.kycStatus: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["kycResult"]) -> MetaOapg.properties.kycResult: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseCode"]) -> MetaOapg.properties.responseCode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["requestTimestamp"]) -> MetaOapg.properties.requestTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responseTimestamp"]) -> MetaOapg.properties.responseTimestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["decentroTxnId"]) -> MetaOapg.properties.decentroTxnId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["error"]) -> MetaOapg.properties.error: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["kycStatus", "status", "message", "kycResult", "responseCode", "requestTimestamp", "responseTimestamp", "decentroTxnId", "error", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["kycStatus"]) -> typing.Union[MetaOapg.properties.kycStatus, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["message"]) -> typing.Union[MetaOapg.properties.message, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["kycResult"]) -> typing.Union[MetaOapg.properties.kycResult, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseCode"]) -> typing.Union[MetaOapg.properties.responseCode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["requestTimestamp"]) -> typing.Union[MetaOapg.properties.requestTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responseTimestamp"]) -> typing.Union[MetaOapg.properties.responseTimestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["decentroTxnId"]) -> typing.Union[MetaOapg.properties.decentroTxnId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["error"]) -> typing.Union[MetaOapg.properties.error, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["kycStatus", "status", "message", "kycResult", "responseCode", "requestTimestamp", "responseTimestamp", "decentroTxnId", "error", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        kycStatus: typing.Union[MetaOapg.properties.kycStatus, str, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        message: typing.Union[MetaOapg.properties.message, str, schemas.Unset] = schemas.unset,
        kycResult: typing.Union[MetaOapg.properties.kycResult, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        responseCode: typing.Union[MetaOapg.properties.responseCode, str, schemas.Unset] = schemas.unset,
        requestTimestamp: typing.Union[MetaOapg.properties.requestTimestamp, str, schemas.Unset] = schemas.unset,
        responseTimestamp: typing.Union[MetaOapg.properties.responseTimestamp, str, schemas.Unset] = schemas.unset,
        decentroTxnId: typing.Union[MetaOapg.properties.decentroTxnId, str, schemas.Unset] = schemas.unset,
        error: typing.Union[MetaOapg.properties.error, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ValidateResponse':
        return super().__new__(
            cls,
            *args,
            kycStatus=kycStatus,
            status=status,
            message=message,
            kycResult=kycResult,
            responseCode=responseCode,
            requestTimestamp=requestTimestamp,
            responseTimestamp=responseTimestamp,
            decentroTxnId=decentroTxnId,
            error=error,
            _configuration=_configuration,
            **kwargs,
        )
