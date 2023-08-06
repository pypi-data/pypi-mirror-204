from loguru import logger
import requests

from api_to_case.common.tools import get_target_value, get_file_path, dump_yaml, dump_json
from requests.auth import HTTPBasicAuth


class SwaggerParser(object):
    s = requests

    def __init__(self, url, username=None, password=None):
        self.api_doc_json = self.get_entry_json(url, username, password)

    def get_entry_json(self, url, username, password):
        '''
        获取api接口文档
        :param url: Swgger API接口地址
        :param username: 鉴权用户名
        :param password: 鉴权密码
        :return: json格式的API文档接口response
        '''
        if username is None:
            response = self.s.get(url)
            if 'You do not have permission to access this resource' in response.text:
                logger.warning('swagger需要用户名及密码登录')
                exit(0)
            else:
                return response.json()
        else:
            response = self.s.get(url, auth=(HTTPBasicAuth(username, password))).json()

        if response is not None:
            dump_json(response, r'./response.json')
            return response

    @staticmethod
    def _make_request_url(test_step_dict, path):
        '''
        根据json,构造api地址
        :param test_step_dict:
        :param path:
        :return:
        '''
        test_step_dict["url"] = path

    @staticmethod
    def _make_request_method(test_step_dict, entry_json):
        '''
        解析json,构造请求方法
        :param test_step_dict:
        :param entry_json:
        :return:
        '''
        test_step_dict["method"] = [x for x in entry_json.keys()][0].upper()

    @staticmethod
    def _make_request_headers(test_step_dict, entry_json):
        '''
        解析json,构造请求头信息
        :param test_step_dict:
        :param entry_json:
        :return:
        '''
        test_step_headers = {}
        for method, params in entry_json.items():
            if 'consumes' in params:
                test_step_headers["content-type"] = params['consumes'][0] + '; charset=utf-8'
            test_step_headers["Authorization"] = " "

        if test_step_headers:
            test_step_dict["headers"] = test_step_headers

    @staticmethod
    def _make_request_params(test_step_dict, entry_json):
        '''
        解析json,构造请求参数
        :param test_step_dict:
        :param entry_json:
        :return:
        '''
        for method, params in entry_json.items():
            query_dict = {}
            for param in params.get("parameters"):
                if param.get("in") == "query" or ('in' not in param.keys()):
                    test_step_dict["in"] = "query"
                    query_string = param.get("name")
                    if 'description' in param:
                        if 'example' in param:
                            query_dict[query_string] = str(param['example']) + ' # ' + param['description']
                        elif 'x-example' in param:
                            query_dict[query_string] = str(param['x-example']) + ' # ' + param['description']
                        else:
                            query_dict[query_string] = ' # ' + param['description']
                    else:
                        query_dict[query_string] = '$' + query_string
                    test_step_dict["params"] = query_dict

    def _make_request_data(self, test_step_dict, entry_json):
        '''
        解析json,构造请求体
        :param test_step_dict:
        :param entry_json:
        :return:
        '''
        for method, params in entry_json.items():
            request_data_key = "params"
            if method.upper() in ["POST", "PUT", "PATCH", 'DELETE']:
                for param in params.get("parameters"):
                    if param.get("in") == "body":
                        test_step_dict['in'] = "body"
                        schema_obj = param.get("name")
                        if schema_obj.upper() in str(get_target_value("originalRef", param['schema'])).upper():
                            for obj, properties in self.api_doc_json.get("definitions").items():
                                data_dict = {}
                                if obj.upper() in schema_obj.upper():
                                    for k, v in properties.get("properties").items():
                                        if 'description' in v:
                                            if 'example' in v:
                                                data_dict[k] = str(v['example']) + ' # ' + v['description']
                                            else:
                                                data_dict[k] = ' # ' + v['description']
                                        else:
                                            data_dict[k] = f"${k}"
                                        test_step_dict[request_data_key] = data_dict
                        else:
                            schema_obj = get_target_value("originalRef", param['schema'])
                            for obj, properties in self.api_doc_json.get("definitions").items():
                                data_dict = {}
                                if obj.upper() in str(schema_obj).upper():
                                    for k, v in properties.get("properties").items():
                                        if 'description' in v:
                                            if 'example' in v:
                                                data_dict[k] = str(v['example']) + ' # ' + v['description']
                                            else:
                                                data_dict[k] = ' # ' + v['description']
                                        else:
                                            data_dict[k] = f"${k}"
                                        test_step_dict[request_data_key] = data_dict

    # TODO: respone提取
    @staticmethod
    def _make_validate(test_step_dict):
        test_step_dict["validate"] = {"equals": {'status_code': 1000},
                                      "contains": '操作成功'}

    def _prepare_test_step(self, path, entry_json):
        '''
        拼装用例
        :param path:
        :param entry_json:
        :return:
        '''
        test_step_dict = {
            "url": "",
            "method": '',
            "headers": {},
            "params": {},
            "validate": {}
        }
        self._make_request_url(test_step_dict, path)
        self._make_request_method(test_step_dict, entry_json)
        self._make_request_headers(test_step_dict, entry_json)
        self._make_request_params(test_step_dict, entry_json)
        self._make_request_data(test_step_dict, entry_json)
        self._make_validate(test_step_dict)
        return test_step_dict

    @staticmethod
    def _prepare_config(entry_json):
        for summary in entry_json.items():
            name = summary[1].get("summary")
        return name

    def _make_testcase(self, path, entry_json):
        '''
        提取json信息
        :param path:
        :param entry_json:
        :return:
        '''
        logger.debug("提取信息并准备测试用例")

        config = self._prepare_config(entry_json)
        test_steps = self._prepare_test_step(path, entry_json)
        return [{'name': config,
                 'requests': test_steps}]

    def gen_testcase(self, path=None, file_type="yml"):
        '''
        转换用例主函数
        :param path: API接口路径
        :param file_type:
        :return:
        '''
        if path is not None:
            for test_mapping in get_target_value(path, self.api_doc_json.get("paths")):
                logger.info(f"开始生成测试用例: {path}")
                test_case = self._make_testcase(path, test_mapping)

                file = get_file_path(path, test_mapping) + "." + file_type
                dump_yaml(test_case, file) if file_type == "yml" else dump_json(test_case, file)
                logger.debug("用例准备完成: {}".format(test_case))

        else:
            for path, test_mapping in self.api_doc_json.get("paths").items():
                logger.info(f"开始生成测试用例: {path}")
                test_case = self._make_testcase(path, test_mapping)

                file = get_file_path(path, test_mapping) + "." + file_type
                logger.debug(f"生成文件 : {file}")
                dump_yaml(test_case, file) if file_type == "yml" else dump_json(test_case, file)
                logger.debug(f"用例生成完成: {test_case}")


