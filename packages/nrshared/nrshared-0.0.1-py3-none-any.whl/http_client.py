import urllib,http.client
import asyncio,aiohttp

class HttpClient:
    """ Http class for client request and response """
    def https_request(self, resorce_url, headers, param_values, function_url, function_key):
        """ returns a http response"""
        params = urllib.parse.urlencode(param_values)
        conn = http.client.HTTPSConnection(function_url)
        conn.request("GET", f"{resorce_url}?code={function_key}&%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        return (response.status,data)

    async def async_http_call(self,urls,headers):
        async with aiohttp.ClientSession(headers=headers) as session:
            ret = await asyncio.gather(*[self.get(url, session) for url in urls])
            return ret

    async def get(self,url, session):
        async with session.get(url=url) as response:
            resp = await response.read()
            return resp.decode("utf-8"),response.status
