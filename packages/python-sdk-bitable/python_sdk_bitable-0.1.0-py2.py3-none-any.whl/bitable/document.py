import requests
import posixpath
import time
from collections import OrderedDict
from params import BitableParams
from auth import FeiShuAuth


class Document:
    VERSION = "v1"
    API_BASE_URL = "https://open.feishu.cn/open-apis/docx/"
    API_LIMIT = 1.0 / 5  # 5 per second
    API_URL = posixpath.join(API_BASE_URL, VERSION)
    MAX_RECORDS_PER_REQUEST = 100
    block_type_dict = {
        1: 'page',

        3: 'heading1',  # 一级标题
        4: 'heading2',  # 二级标题
        13: 'ordered',  # 有序列表

    }

    def __init__(self, doc_id: str, app_id: str, app_secret: str, timeout: int = None):
        session = requests.Session()
        session.auth = FeiShuAuth(app_id=app_id, app_secret=app_secret)
        self.session = session
        self.doc_id = doc_id
        self.url_doc = posixpath.join(self.API_URL, "documents", doc_id)
        self.timeout = timeout

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

    def _request(self, method, url, params=None, json_data=None):
        response = self.session.request(
            method, url, params=params, json=json_data, timeout=self.timeout
        )
        return self._process_response(response)

    def _get(self, url, **params):
        processed_params = self._process_params(params)
        return self._request("get", url, params=processed_params)

    def get_iter(self, url, **options):
        offset = None
        while True:
            data = self._get(url, page_token=offset, **options)
            # print(data)
            if not data.get('data').get('items'):
                break
            records = data.get("data", {"items": []}).get("items", [])
            time.sleep(self.API_LIMIT)
            yield records
            if data.get("data").get("has_more"):
                pass
            else:
                break
            offset = data.get("data").get("page_token")
            if not offset:
                break

    def get_all(self, **options):
        all_records = []
        url = self.url_doc + '/blocks'
        for records in self.get_iter(url=url, **options):
            all_records.extend(records)
        return all_records


def main():
    doc = Document(app_id='cli_a2456e28678dd00b',
                   app_secret='eGlSyaVaJ1LtsfOKaiML9elNOnmpARgj',
                   doc_id='FygRdiYzboepaQxldKMcyDo2n6b')
    doc_data = doc.get_all()
    print(doc_data)


if __name__ == '__main__':
    main()
