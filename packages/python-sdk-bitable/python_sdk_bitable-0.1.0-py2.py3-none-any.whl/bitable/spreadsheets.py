import requests
import posixpath
import time
from collections import OrderedDict
from params import BitableParams
from auth import FeiShuAuth
import pprint


class SpreadSheet(object):
    VERSION = "v2"
    API_BASE_URL = "https://open.feishu.cn/open-apis/sheets/"
    API_LIMIT = 1.0 / 5  # 5 per second
    API_URL = posixpath.join(API_BASE_URL, VERSION, "spreadsheets")
    MAX_RECORDS_PER_REQUEST = 100

    def __init__(self, spreadsheet_token: str, app_id: str, app_secret: str, timeout: int = None):
        """
        Instantiate a new SpreadSheet instance

        >>> sheet = SpreadSheet('spreadsheet_token','app_id', 'app_secret')

        Args:
            spreadsheet_token: str (``str``): SpreadSheet  identifier
            app_id (``str``): API key
            app_secret (``str``): API secret key

        Keyword Args:
            timeout (``int``, ``Tuple[int, int]``, optional): Optional timeout
                parameters to be used in request. `See requests timeout docs.
                <https://requests.readthedocs.io/en/master/user/advanced/#timeouts>`_
        """
        session = requests.Session()
        session.auth = FeiShuAuth(app_id=app_id, app_secret=app_secret)
        self.session = session
        self.spreadsheet_token = spreadsheet_token
        self.spreadsheet_url = posixpath.join(self.API_URL, self.spreadsheet_token)
        self.timeout = timeout
        self._metadata = self.get_metadata()
        self.sheets = [{'sheetId': i.get('sheetId'),
                        'title': i.get('title'),
                        'rowCount': i.get('rowCount')
                        } for i in self._metadata.get('data').get('sheets')]
        # self.sheets = [{'id': "a", "name": "b"} for i in self.metadata]

    def _process_params(self, params):
        """
        Process params names or values as needed using filters
        """
        new_params = OrderedDict()
        for param_name, param_value in sorted(params.items()):
            param_value = params[param_name]
            ParamClass = BitableParams._get(param_name)
            new_params.update(ParamClass(param_value).to_param_dict())
        return new_params

    def _chunk(self, iterable, chunk_size):
        """Break iterable into chunks."""
        for i in range(0, len(iterable), chunk_size):
            yield iterable[i: i + chunk_size]

    def _build_batch_record_objects(self, records):
        return [{"fields": record} for record in records]

    def _process_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            err_msg = str(exc)

            # Attempt to get Error message from response, Issue #16
            try:
                error_dict = response.json()
            except ValueError:
                pass
            else:
                if "error" in error_dict:
                    err_msg += " [Error: {}]".format(error_dict["error"])
            exc.args = (*exc.args, err_msg)
            raise exc
        else:
            return response.json()

    def sheet_url(self, sheet_id):
        """ Builds URL with record id """
        return posixpath.join(self.spreadsheet_url, "records", sheet_id)

    def _request(self, method, url, params=None, json_data=None):
        response = self.session.request(
            method, url, params=params, json=json_data, timeout=self.timeout
        )
        return self._process_response(response)

    def _get(self, url, **params):
        processed_params = self._process_params(params)
        return self._request("get", url, params=processed_params)

    def _post(self, url, json_data):
        return self._request("post", url, json_data=json_data)

    def _put(self, url, json_data):
        return self._request("put", url, json_data=json_data)

    def _patch(self, url, json_data):
        return self._request("patch", url, json_data=json_data)

    def _delete(self, url):
        return self._request("delete", url)

    def get_metadata(self):
        return self._get(
            self.spreadsheet_url + "/metainfo")

    def get_data_by_range(self, shift_id: str, start, end):
        return self._get(
            posixpath.join(self.spreadsheet_url, "values",
                           shift_id + "!" + start + ":" + end + "?valueRenderOption=ToString&dateTimeRenderOption=FormattedString"))

    def get_data_by_id(self, shift_id: str):
        return self._get(
            posixpath.join(self.spreadsheet_url, "values",
                           shift_id + "?valueRenderOption=ToString&dateTimeRenderOption=FormattedString"))


def main():
    a = SpreadSheet(spreadsheet_token='shtcn3J74Ru2oa8G38cAuDtqs9c', app_id='cli_a2456e28678dd00b',
                    app_secret='eGlSyaVaJ1LtsfOKaiML9elNOnmpARgj')
    print(a.sheets)
    print(a._metadata)
    # result = a.get_data_by_range('912e7f', 'A1', 'N16')
    # result = a.get_data_by_id('912e7f').get('data').get('valueRange').get('values')
    # import pandas as pd
    # df = pd.DataFrame(result[1:], columns=[result[3]])
    # df = df.fillna(method='ffill').dropna()
    # print(df)


if __name__ == "__main__":
    main()
