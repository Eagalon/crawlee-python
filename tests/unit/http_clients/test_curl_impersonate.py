from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from crawlee import Request
from crawlee.errors import ProxyError
from crawlee.http_clients import CurlImpersonateHttpClient
from crawlee.statistics import Statistics

if TYPE_CHECKING:
    from yarl import URL

    from crawlee.proxy_configuration import ProxyInfo


@pytest.fixture
def http_client() -> CurlImpersonateHttpClient:
    return CurlImpersonateHttpClient()


# TODO: improve this flaky test and remove the skip
# https://github.com/apify/crawlee-python/issues/743
@pytest.mark.skip
async def test_crawl_with_proxy(
    http_client: CurlImpersonateHttpClient,
    proxy: ProxyInfo,
    httpbin: URL,
) -> None:
    url = str(httpbin / 'status/222')
    request = Request.from_url(url)

    async with Statistics.with_default_state() as statistics:
        result = await http_client.crawl(request, proxy_info=proxy, statistics=statistics)

    assert result.http_response.status_code == 222  # 222 - authentication successful


@pytest.mark.skipif(os.name == 'nt', reason='Skipped on Windows')
async def test_crawl_with_proxy_disabled(
    http_client: CurlImpersonateHttpClient,
    disabled_proxy: ProxyInfo,
    httpbin: URL,
) -> None:
    url = str(httpbin / 'status/222')
    request = Request.from_url(url)

    with pytest.raises(ProxyError):
        async with Statistics.with_default_state() as statistics:
            await http_client.crawl(request, proxy_info=disabled_proxy, statistics=statistics)


@pytest.mark.skipif(os.name == 'nt', reason='Skipped on Windows')
async def test_send_request_with_proxy(
    http_client: CurlImpersonateHttpClient,
    proxy: ProxyInfo,
    httpbin: URL,
) -> None:
    url = str(httpbin / 'status/222')

    response = await http_client.send_request(url, proxy_info=proxy)
    assert response.status_code == 222  # 222 - authentication successful


@pytest.mark.skipif(os.name == 'nt', reason='Skipped on Windows')
async def test_send_request_with_proxy_disabled(
    http_client: CurlImpersonateHttpClient,
    disabled_proxy: ProxyInfo,
    httpbin: URL,
) -> None:
    url = str(httpbin / 'status/222')

    with pytest.raises(ProxyError):
        await http_client.send_request(url, proxy_info=disabled_proxy)
