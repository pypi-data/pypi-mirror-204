import configparser
import dataclasses
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

import pydantic
from pydantic import BaseModel


class FieldDataType(pydantic.BaseModel):
    meta: Dict[str, str]
    type: str  # noqa: A003


class FieldDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    primary: bool
    optional: bool
    data_type: FieldDataType


class IcebergTableProperties(pydantic.BaseModel):
    format: Optional[str] = None  # noqa: A003
    partitioning: Optional[List[str]] = None
    location: Optional[str] = None
    format_version: Optional[int] = None


class StreamingSchemaBase(pydantic.BaseModel):
    type: Literal["streaming"]  # noqa: A003
    fields: Optional[List[FieldDefinition]]
    iceberg_table_properties: Optional[IcebergTableProperties] = None


class StoredSchemaBase(pydantic.BaseModel):
    type: Literal["stored"]  # noqa: A003
    fields: Optional[List[FieldDefinition]]


class SubsetSchema(BaseModel):
    type: Literal["subset"]  # noqa: A003
    parent_product: str
    columns: List[str]


class CreateStreamingSchema(StreamingSchemaBase):
    flow_type: str


class CreateSubsetDataProduct(BaseModel):
    name: str
    description: str
    details: SubsetSchema


class CreateStreamingDataProduct(pydantic.BaseModel):
    name: str
    description: str
    details: CreateStreamingSchema


class CreateStoredDataProduct(pydantic.BaseModel):
    name: str
    description: str
    details: StoredSchemaBase


class Info(pydantic.BaseModel):
    label: str
    owner: Union[str, None]
    contact_ids: List[str]
    links: List[str]
    notes: Union[str, None]


class CreateDataProduct(pydantic.BaseModel):
    name: str
    description: str
    info: Info
    details: Union[StoredSchemaBase, CreateStreamingSchema, SubsetSchema] = pydantic.Field(..., discriminator="type")


class StreamingDataProductSchema(StreamingSchemaBase):
    fields: List[FieldDefinition]


class StoredDataProductSchema(StoredSchemaBase):
    fields: List[FieldDefinition]


class UpdateDataProductSchema(pydantic.BaseModel):
    details: Union[StreamingDataProductSchema, StoredDataProductSchema] = pydantic.Field(..., discriminator="type")


class UpdateDataProductInfo(pydantic.BaseModel):
    info: Info


class ExpectationItem(pydantic.BaseModel):
    expectation_type: str
    kwargs: dict
    meta: dict


class ExpectationWeights(pydantic.BaseModel):
    accuracy: float
    completeness: float
    consistency: float
    uniqueness: float
    validity: float


class ExpectationColumnThresholds(BaseModel):
    accuracy: Union[float, None]
    completeness: Union[float, None]
    consistency: Union[float, None]
    uniqueness: Union[float, None]
    validity: Union[float, None]


class ExpectationThresholds(BaseModel):
    table: float
    columns: Dict[str, ExpectationColumnThresholds]


class UpdateQualityExpectations(pydantic.BaseModel):
    custom_details: List[ExpectationItem]
    weights: Union[ExpectationWeights, None]
    thresholds: Union[ExpectationThresholds, None]


class RegisterCore(BaseModel):
    partition: str
    name: str


class RemoveCore(BaseModel):
    urn: str


class CreateSource(pydantic.BaseModel):
    name: str
    description: Union[str, None] = None
    info: Info


class UpdateSource(pydantic.BaseModel):
    name: str
    description: Union[str, None] = None


class UpdateSourceInfo(pydantic.BaseModel):
    info: Info


class ExternalDatabaseConnectionDetails(pydantic.BaseModel):
    type: Literal["external_database"]  # noqa: A003
    engine: str
    schema_: str = pydantic.Field(..., alias="schema")
    host: str
    port: int
    database: str
    user_env: str
    password_env: str


class FileConnectionDetails(pydantic.BaseModel):
    type: Literal["file"]  # noqa: A003
    url: str
    access_key_env: Optional[str]
    access_secret_env: Optional[str]


class CreateConnection(pydantic.BaseModel):
    name: str
    details: Union[
        ExternalDatabaseConnectionDetails,
        FileConnectionDetails,
    ]


class TableConnectionParams(pydantic.BaseModel):
    type: Literal["table"]  # noqa: A003
    table: str


class QueryConnectionParams(pydantic.BaseModel):
    type: Literal["query"]  # noqa: A003
    query: str


class CSVConnectionParams(pydantic.BaseModel):
    type: Literal["csv"]  # noqa: A003
    path: Union[str, List[str]]
    has_header: Optional[bool]
    delimiter: Optional[str]
    quote_char: Optional[str]
    escape_char: Optional[str]


class CreateSourceConnection(pydantic.BaseModel):
    details: Union[
        TableConnectionParams,
        QueryConnectionParams,
        CSVConnectionParams,
    ]


class Auth(BaseModel):
    access_token: str = ""
    expires_in: Optional[int] = None
    refresh_token: str = ""
    refresh_expires_in: Optional[int] = None


class OptionalProfile(BaseModel):
    gateway_api_url: str = ""
    registry_api_url: str = ""
    iam_api_url: str = ""
    storage_api_url: str = ""
    user: str = ""
    access_token: str = ""
    refresh_token: str = ""
    ignore_tls: bool = False


class Profile(OptionalProfile):
    gateway_api_url: str
    registry_api_url: str
    iam_api_url: str
    storage_api_url: str
    user: str
    access_token: str
    refresh_token: str
    ignore_tls: bool


class EffectEnum(Enum):
    allow = "allow"
    deny = "deny"


class Statement(BaseModel):
    sid: str
    principal: List[str]
    action: List[str]
    resource: List[str]
    condition: Optional[List[str]] = None
    effect: EffectEnum = EffectEnum.allow

    class Config:
        """Pydantic configuration object."""

        use_enum_values = True


class Statements(BaseModel):
    statements: List[Statement]


class Policy(BaseModel):
    version: str = "2022-10-01"
    statements: List[Statement]


class UserPolicy(BaseModel):
    user: str
    policy: Policy


@dataclasses.dataclass
class Common:
    gateway_api_url: str
    registry_api_url: str
    iam_api_url: str
    storage_api_url: str
    profile_name: str
    config: configparser.ConfigParser
    profile: Optional[Union[Profile, OptionalProfile]]

    def get_gateway_api_url(self) -> str:
        """Return gateway api url.

        If a user profile is provided and defines a gateway url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.gateway_api_url:
            return self.profile.gateway_api_url
        return self.gateway_api_url

    def get_registry_api_url(self) -> str:
        """Return registry api url.

        If a user profile is provided and defines a registry url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.registry_api_url:
            return self.profile.registry_api_url
        return self.registry_api_url

    def get_iam_api_url(self) -> str:
        """Return iam api url.

        If a user profile is provided and defines a iam url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.iam_api_url:
            return self.profile.iam_api_url
        return self.iam_api_url

    def get_storage_api_url(self) -> str:
        """Return storage api url.

        If a user profile is provided and defines a storage url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.profile and self.profile.storage_api_url:
            return self.profile.storage_api_url
        return self.storage_api_url
