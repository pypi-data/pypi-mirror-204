from typing import Dict, Optional
import logging

from requests import Response, Session

from zapit.exceptions import RequestException

logger = logging.getLogger(__name__)
TIMEOUT = 10


class Requestor:
    def __init__(
        self,
        api_key: str,
        session: Optional[Session] = None,
        timeout: float = TIMEOUT,
    ) -> None:
        self.timeout = timeout
        self.base_url = "https://api.zerotier.com/api/v1"
        self._http = session or Session()
        self.api_key = api_key

    def request(
        self,
        method: str,
        path: str,
        data,
        headers: Dict = {},
        timeout: Optional[float] = TIMEOUT,
        *args,
        **kwargs,
    ) -> Response:
        url = f"{self.base_url}{path}"
        auth_headers = {"Authorization": f"Bearer {self.api_key}"}
        auth_headers.update(headers)
        return self._make_request(
            method,
            url,
            auth_headers,
            data,
            timeout=timeout,
        )

    def _make_request(
        self,
        method,
        url,
        headers,
        data,
        *args,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Response:
        try:
            logger.info(f"Url: {url}")
            logger.info(f"data: {data}")
            logger.info(f"headers: {headers}")
            return self._http.request(
                method,
                url,
                headers=headers,
                data=data,
                timeout=timeout or self.timeout,
            )
        except Exception as exc:
            raise RequestException(exc, args, kwargs)
