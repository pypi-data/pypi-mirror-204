"""Fondat Salesforce sObject module."""

from datetime import date, datetime
from fondat.codec import JSONCodec
from fondat.data import datacls, make_datacls
from fondat.error import NotFoundError
from fondat.resource import operation, query, resource
from fondat.salesforce.client import Client
from fondat.validation import MaxLen
from typing import Annotated, Any, Literal


@datacls
class PicklistEntry:
    active: bool
    label: str | None
    value: str


@datacls
class Location:
    latitude: float | None
    longitude: float | None


@datacls
class Address(Location):
    accuracy: str | None
    city: str | None
    country: str | None
    countryCode: str | None
    postalCode: str | None
    state: str | None
    stateCode: str | None
    street: str | None


_type_mappings = {
    "address": Address,
    "anyType": Any,
    "base64": bytes,
    "boolean": bool,
    "combobox": str,
    "complexvalue": Any,
    "currency": float,
    "date": date,
    "datetime": datetime,
    "double": float,
    "email": str,
    "encryptedstring": str,
    "id": str,
    "int": int,
    "json": Any,
    "location": Location,
    "long": int,
    "multipicklist": str,
    "percent": float,
    "phone": str,
    "picklist": str,
    "reference": str,
    "time": str,
    "string": str,
    "textarea": str,
    "url": str,
}


FieldType = Literal[tuple(_type_mappings.keys())]


@datacls
class Field:
    aggregatable: bool
    aiPredictionField: bool
    autoNumber: bool
    byteLength: int
    calculated: bool
    cascadeDelete: bool
    caseSensitive: bool
    createable: bool
    custom: bool
    defaultedOnCreate: bool
    dependentPicklist: bool
    deprecatedAndHidden: bool
    digits: int
    displayLocationInDecimal: bool
    encrypted: bool
    externalId: bool
    filterable: bool
    formulaTreatNullNumberAsZero: bool
    groupable: bool
    highScaleNumber: bool
    htmlFormatted: bool
    idLookup: bool
    label: str
    length: int
    name: str
    nameField: bool
    namePointing: bool
    nillable: bool
    permissionable: bool
    picklistValues: list[PicklistEntry]
    polymorphicForeignKey: bool
    precision: int
    queryByDistance: bool
    restrictedDelete: bool
    restrictedPicklist: bool
    scale: int
    searchPrefilterable: bool
    soapType: str
    sortable: bool
    type: FieldType
    unique: bool
    updateable: bool
    writeRequiresMasterRead: bool


@datacls
class ChildRelationship:
    cacadeDelete: bool
    childSObject: str
    deprecatedAndHidden: bool
    field: str
    junctionIdListNames: list[str]
    junctionReferenceTo: list[str]
    relationshipName: str
    restrictedDelete: bool


@datacls
class URLs:
    approvalLayouts: str | None
    compactLayouts: str | None
    describe: str | None
    layouts: str | None
    listviews: str | None
    quickActions: str | None
    rowTemplate: str | None
    sobject: str | None
    uiDetailTemplate: str | None
    uiEditTemplate: str | None
    uiNewRecord: str | None


@datacls
class SObjectBasic:
    activateable: bool
    createable: bool
    custom: bool
    customSetting: bool
    deepCloneable: bool
    deletable: bool
    deprecatedAndHidden: bool
    feedEnabled: bool
    hasSubtypes: bool
    isInterface: bool
    isSubtype: bool
    label: str
    labelPlural: str
    layoutable: bool
    mergeable: bool
    mruEnabled: bool
    name: str
    queryable: bool
    replicateable: bool
    retrieveable: bool
    searchable: bool
    triggerable: bool
    undeletable: bool
    updateable: bool
    urls: URLs


@datacls
class SObject:
    activateable: bool
    compactLayoutable: bool
    createable: bool
    custom: bool
    customSetting: bool
    deepCloneable: bool
    deletable: bool
    deprecatedAndHidden: bool
    feedEnabled: bool
    fields: list[Field]
    hasSubtypes: bool
    isInterface: bool
    isSubtype: bool
    keyPrefix: str | None
    label: str
    labelPlural: str
    layoutable: bool
    mergeable: bool
    mruEnabled: bool
    name: str
    queryable: bool
    replicateable: bool
    retrieveable: bool
    searchLayoutable: bool
    searchable: bool
    sobjectDescribeOption: str
    triggerable: bool
    undeletable: bool
    updateable: bool
    urls: URLs


@datacls
class SObjects:
    encoding: str
    maxBatchSize: int
    sobjects: list[SObjectBasic]


def sobject_field_type(field: Field) -> Any:
    """Return the Python type associated with an SObject field."""

    try:
        result = _type_mappings[field.type]
    except KeyError:
        raise TypeError(f"unsupported field type: {field.type}")
    if field.length != 0:
        result = Annotated[result, MaxLen(field.length)]
    return result | None


def sobjects_metadata_resource(client: Client):
    """Return resource representing SObject metadata."""

    path = f"{client.resources['sobjects']}"

    @resource
    class SObjectMetadataResource:
        """..."""

        def __init__(self, name):
            self.name = name

        @query
        async def describe(self) -> SObject:
            """Get SObject metadata."""
            async with client.request(
                method="GET", path=f"{path}/{self.name}/describe"
            ) as response:
                metadata = JSONCodec.get(SObject).decode(await response.json())
            if metadata.name != self.name:
                raise NotFoundError
            return metadata

    @resource
    class SObjectsMetadataResource:
        """..."""

        @operation
        async def get(self) -> SObjects:
            """Get a list of objects."""
            async with client.request(method="GET", path=f"{path}/") as response:
                return JSONCodec.get(SObjects).decode(await response.json())

        def __getitem__(self, name: str) -> SObjectMetadataResource:
            return SObjectMetadataResource(name)

    return SObjectsMetadataResource()


async def sobject_data_resource(client: Client, name: str):
    """Return resource representing SObject data."""

    try:
        metadata = await sobjects_metadata_resource(client)[name].describe()
    except NotFoundError as nfe:
        raise TypeError(f"sobject not found: {name}") from nfe

    datacls = make_datacls(
        metadata.name,
        [(field.name, sobject_field_type(field)) for field in metadata.fields],
    )

    codec = JSONCodec.get(datacls)

    @resource
    class SObjectRecordResource:
        """..."""

        def __init__(self, id: str):
            self.id = id

        @operation
        async def get(self) -> datacls:
            path = metadata.urls.rowTemplate.format(ID=self.id)
            async with client.request(method="GET", path=path) as response:
                return codec.decode(await response.json())

    @resource
    class SObjectResource:
        """..."""

        @query
        async def describe(self) -> SObject:
            return metadata

        def __getitem__(self, id) -> SObjectRecordResource:
            """Return an sobject record resource."""
            return SObjectRecordResource(id)

    return SObjectResource()
