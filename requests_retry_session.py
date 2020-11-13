# This Python file uses the following encoding: utf-8
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def requests_retry_session(
    retries=3,
    backoff_factor=0.2,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# if__name__ == "__main__":
#     pass
