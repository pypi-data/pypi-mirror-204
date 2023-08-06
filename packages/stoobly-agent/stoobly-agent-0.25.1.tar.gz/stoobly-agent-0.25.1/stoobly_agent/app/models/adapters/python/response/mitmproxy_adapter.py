import pdb
import requests

from mitmproxy.http import Headers, Response as MitmproxyResponse
from time import time

from stoobly_agent.app.models.adapters.raw_http_request_adapter import DEFAULT_HTTP_VERSION

class MitmproxyResponseAdapter():

  def __init__(self, response: requests.Response):
    self.__timestamp_start = time()

    if hasattr(response, 'raw'):
      self.__http_version = f"HTTP/{response.raw.version / 10.0}"
    else:
      self.__http_version = DEFAULT_HTTP_VERSION

    self.__latency = 0 # Seconds
    self.__response = response
 
  def with_latency(self, latency: int):
    self.__latency = latency
    return self

  @property
  def status_code(self) -> int:
    status_code = self.__response.status_code

    if isinstance(status_code, str):
      return int(status_code)

    if isinstance(status_code, bytes):
      return int(status_code.decode())

    return status_code

  @property
  def headers(self):
    return Headers(**self.__decode_dict(self.__response.headers))

  @property
  def reason(self):
    return self.__response.reason or ''

  @property
  def timestamp_end(self):
    return self.__timestamp_start + self.__latency

  def adapt(self):
    body = b''
    
    if self.__response._content_consumed or not hasattr(self.__response, 'raw'):
      body = self.__response.content
    else:
      body = self.__response.raw.data

    return MitmproxyResponse(
      self.__http_version,
      self.status_code,
      self.reason,
      self.headers,
      body,
      Headers(), # Trailers
      self.__timestamp_start,
      self.timestamp_end
    )

  def __decode_dict(self, d):
    new_d = {}
    for k, v in d.items():
      new_d[k.decode() if isinstance(k, bytes) else k] = v.decode() if isinstance(k, bytes) else v
    return new_d