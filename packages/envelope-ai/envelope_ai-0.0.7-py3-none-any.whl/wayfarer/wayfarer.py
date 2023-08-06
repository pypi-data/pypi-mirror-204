import logging
from typing import Dict, List, Optional
from uuid import UUID

import requests
import validators

LOGGER = logging.getLogger(__name__)

DOCUMENTS_PATH = "/api/v1/documents"
QUERY_PATH = "/api/v1/query"
API_HEADER_KEY = "x-envelope-key"

READER_URL = "https://reader.envelope.ai"
COMPOSER_URL = "https://composer.envelope.ai"


def _build_header(api_key: str, additional_headers: Dict):
    header = {API_HEADER_KEY: api_key}
    # TODO: Check if there'll be header collision
    header.update(additional_headers)
    return header


def _set_and_validate_host(host: str):
    if not host:
        raise ValueError(f"No host value provided. A host must be provided.")
    elif not validators.url(host):
        raise ValueError(f"Provided host {host} is not a valid url format.")

    # Make sure we don't have dangling backslashes in the url during url composition later
    trimmed_hostname = host.rstrip("/")

    # TODO: Validate host is valid and healthy
    return trimmed_hostname


def _check_collection_identifier_collision(collection_id: Optional[UUID], collection_name: Optional[str]):
    if collection_id is None and collection_name is None:
        raise ValueError(
            "Please provide at least one value for either collection_id or collection_name."
        )
    elif collection_id and collection_name:
        raise ValueError(
            "Please only provide either collection_id or collection_name in your request."
        )


class Composer(object):
    """docstring for Composer"""

    def __init__(self, api_key: UUID, host: Optional[str] = None):
        if host is None:
            host = COMPOSER_URL

        self.host = _set_and_validate_host(host)
        self.api_key = api_key

    def delete(
        self,
        documents: List[UUID],
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
    ) -> Dict:
        _check_collection_identifier_collision(collection_id, collection_name)
        # TODO: Be safe and make sure the item passed through that doesn't hold a value is a None

        # TODO: filter through documents to make sure values are what we expect them to be
        """
        dict(
            collection_id="collection_id_example",
            collection_name="collection_name_example",
            documents=["uuid-uuid-uuid"]
            ],
        )
        """

        request_data = dict(
            collection_id=collection_id,
            collection_name=collection_name,
            documents=documents,
        )
        response = requests.delete(
            url=f"{self.host}{DOCUMENTS_PATH}",
            json=request_data,
            headers=_build_header(
                api_key=self.api_key,
                additional_headers={"Content-Type": "application/json"},
            ),
        )

        if not response.ok:
            LOGGER.error(
                f"Request failed with status code {response.status_code} "
                f"and the following message:\n{response.text}"
            )
            return {}
        return response.json()

    def insert(
        self,
        documents: List[Dict],
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
    ) -> Dict:
        _check_collection_identifier_collision(collection_id, collection_name)
        # TODO: Be safe and make sure the item passed through that doesn't hold a value is a None

        # TODO: filter through documents to make sure values are what we expect them to be
        """
        dict(
            collection_id="collection_id_example",
            collection_name="collection_name_example",
            documents=[
                dict(
                    embedding=[3.14],
                    metadata=dict(),
                )
            ],
        )
        """

        request_data = dict(
            collection_id=collection_id,
            collection_name=collection_name,
            documents=documents,
        )
        response = requests.post(
            url=f"{self.host}{DOCUMENTS_PATH}",
            json=request_data,
            headers=_build_header(
                api_key=self.api_key,
                additional_headers={"Content-Type": "application/json"},
            ),
        )

        if not response.ok:
            LOGGER.error(
                f"Request failed with status code {response.status_code} "
                f"and the following message:\n{response.text}"
            )
            return {}
        return response.json()

    def update(
        self,
        documents: List[Dict],
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
    ) -> Dict:
        _check_collection_identifier_collision(collection_id, collection_name)
        # TODO: Be safe and make sure the item passed through that doesn't hold a value is a None

        # TODO: filter through documents to make sure values are what we expect them to be
        """
        dict(
            collection_id="collection_id_example",
            collection_name="collection_name_example",
            documents=[
                dict(
                    id:"UUID-UUID-UUID",
                    metadata={},
                )
            ],
        )
        """

        request_data = dict(
            collection_id=collection_id,
            collection_name=collection_name,
            documents=documents,
        )
        response = requests.patch(
            url=f"{self.host}{DOCUMENTS_PATH}",
            json=request_data,
            headers=_build_header(
                api_key=self.api_key,
                additional_headers={"Content-Type": "application/json"},
            ),
        )

        if not response.ok:
            LOGGER.error(
                f"Request failed with status code {response.status_code} "
                f"and the following message:\n{response.text}"
            )
            return {}
        return response.json()


class Reader(object):
    """docstring for Reader"""

    def __init__(self, api_key: UUID, host: Optional[str] = None):
        if host is None:
            host = READER_URL

        self.host = _set_and_validate_host(host)
        self.api_key = api_key

    def query(
        self,
        sql: str,
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
        query_embedding: Optional[List[float]] = None,
    ) -> Dict:
        _check_collection_identifier_collision(collection_id, collection_name)
        # TODO: Be safe and make sure the item passed through that doesn't hold a value is a None

        # TODO: filter through query_embedding to make sure values are what we expect
        """
        dict(
            collection_id="collection_id_example",
            collection_name="collection_name_example",
            query_embedding=None,
            sql="sql_example",
        )
        """

        request_data = dict(
            collection_id=collection_id,
            collection_name=collection_name,
            query_embedding=query_embedding,
            sql=sql,
        )
        response = requests.post(
            url=f"{self.host}{QUERY_PATH}",
            json=request_data,
            headers=_build_header(
                api_key=self.api_key,
                additional_headers={"Content-Type": "application/json"},
            ),
        )

        if not response.ok:
            LOGGER.error(
                f"Request failed with status code {response.status_code} "
                f"and the following message:\n{response.text}"
            )
            return {}
        return response.json()


class Wayfarer(object):
    """docstring for Wayfarer"""

    def __init__(
        self,
        api_key: str,
        reader_host: Optional[str] = None,
        composer_host: Optional[str] = None,
    ):
        self.composer = Composer(api_key=api_key, host=composer_host)
        self.reader = Reader(api_key=api_key, host=reader_host)

    def delete(
        self,
        documents: List[Dict],
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
    ) -> Dict:
        return self.composer.delete(
            documents=documents,
            collection_id=collection_id,
            collection_name=collection_name,
        )

    def insert(
        self,
        documents: List[Dict],
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
    ) -> Dict:
        return self.composer.insert(
            documents=documents,
            collection_id=collection_id,
            collection_name=collection_name,
        )

    def query(
        self,
        sql: str,
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
        query_embedding: Optional[List[float]] = None,
    ) -> Dict:
        return self.reader.query(
            sql=sql,
            collection_id=collection_id,
            collection_name=collection_name,
            query_embedding=query_embedding,
        )

    def update(
        self,
        documents: List[Dict],
        collection_id: Optional[UUID] = None,
        collection_name: Optional[str] = None,
    ) -> Dict:
        return self.composer.update(
            documents=documents,
            collection_id=collection_id,
            collection_name=collection_name,
        )
