"""Fondat Salesforce bulk module."""

import asyncio

from collections import deque, namedtuple
from collections.abc import Iterable
from contextlib import suppress
from fondat.csv import TypedDictCodec
from fondat.salesforce.client import Client
from fondat.salesforce.jobs import queries_resource
from fondat.salesforce.sobjects import SObject, sobject_field_type
from time import time
from typing import Any, TypedDict


_exclude_types = {"address", "location"}


class SObjectQuery:
    """
    Performs an asynchronous bulk data query.

    Parameters:
    • client: client object through which to perform queries
    • sobject: Salesforce object metadata
    • columns: columns to select  [all fields]
    • where: query conditon expression
    • order_by: order of query results
    • limit: maximum number of rows in query results
    • page_size: number of rows to retrieve per page
    • timeout: seconds to wait for query job to complete
    """

    Column = namedtuple("Column", "name, expression, type")

    def __init__(
        self,
        client: Client,
        sobject: SObject,
        *,
        columns: Iterable[Column | str] | None = None,
        where: str | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        page_size: int | None = None,
        timeout: int | None = None,
    ):
        self.client = client
        self.page_size = page_size
        columns = (
            [f.name for f in sobject.fields if f.type not in _exclude_types]
            if columns is None
            else list(columns)
        )
        if len(columns) == 0:
            raise ValueError("must select at least one column")
        fields = {field.name: field for field in sobject.fields}
        for n, column in enumerate(columns):
            if isinstance(column, SObjectQuery.Column):
                continue
            field = fields.get(column)
            if not field:
                raise ValueError(f"unknown field: {column}")
            if field.type in _exclude_types:
                raise ValueError(f"cannot query {field.type} type field: {column}")
            columns[n] = SObjectQuery.Column(column, None, sobject_field_type(field))
        self.td = TypedDict("QueryDict", {column.name: column.type for column in columns})
        self.stmt = "SELECT "
        self.stmt += ", ".join(
            ((c.expression or c.name) + (f" {c.name}" if c.expression else "")) for c in columns
        )
        self.stmt += f" FROM {sobject.name}"
        if where:
            self.stmt += f" WHERE {where}"
        if order_by:
            self.stmt += f" ORDER BY {order_by}"
        if limit:
            self.stmt += f" LIMIT {limit}"
        self.timeout = timeout
        self.query = None
        self.results = None
        self.header = None
        self.cursor = None

    async def info(self):
        return await self.query.get()

    async def _await_complete(self):
        """Wait for job to be complete."""
        start = time()
        sleep = 1
        while (state := (await self.info()).state) in {"UploadComplete", "InProgress"}:
            if self.timeout and time() - start >= self.timeout:
                raise asyncio.exceptions.TimeoutError
            await asyncio.sleep(sleep)
            sleep = min(sleep * 2, 60)
        if state != "JobComplete":
            raise RuntimeError(f"unexpected job state: {state}")

    async def __aenter__(self):
        if self.query is not None:
            raise RuntimeError("context is not reentrant")
        queries = queries_resource(self.client)
        info = await queries.post(operation="query", query=self.stmt)
        self.query = queries[info.id]
        return self

    async def __aexit__(self, *args):
        if self.results is None:
            with suppress(asyncio.exceptions.TimeoutError):
                await self._await_complete()
        with suppress(Exception):
            await self.query.delete()

    def __aiter__(self):
        if self.query is None:
            raise RuntimeError("must iterate within async context")
        return self

    async def _next_page(self):
        page = await self.query.results(limit=self.page_size or 1000, cursor=self.cursor)
        self.results = deque(page.items)
        self.cursor = page.cursor
        self.codec = TypedDictCodec(self.td, self.results.popleft())

    async def __anext__(self) -> dict[str, Any]:
        if self.results is None:
            await self._await_complete()
        if self.results is None or (not self.results and self.cursor):
            await self._next_page()
        if not self.results and not self.cursor:
            raise StopAsyncIteration
        return self.codec.decode(self.results.popleft())
