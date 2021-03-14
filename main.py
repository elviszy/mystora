import json
import copy
import uuid
from xml.dom.minidom import parse


class SoapUIXML:

    def __init__(self, file_path):
        domTree = parse(file_path)
        # 文档根元素
        self.__root = domTree.documentElement

    def get_project_name(self):
        return self.__root.getAttribute('name')

    def get_testsuite_nodes(self):
        return self.__root.getElementsByTagName('con:testSuite')

    def get_testcase_nodes(self, suite_node):
        return suite_node.getElementsByTagName('con:testCase')

    def get_testcase_name(self, case_node):
        return case_node.getAttribute('name')

    def get_teststep_nodes(self, case_node):
        return case_node.getElementsByTagName('con:testStep')

    def get_teststep_type(self, step_node):
        return step_node.getAttribute('type')

    def get_teststep_name(self, step_node):
        return step_node.getAttribute('name')

    def get_groovy_script(self, step_node):
        return step_node.getElementsByTagName('script')[0].childNodes[0].data

    def get_delay_time(self, step_node):
        return step_node.getElementsByTagName('delay').childNodes[0].data


class MeterSphereBaseJson:

    def __init__(self, file):
        with open(file, encoding='utf-8') as f:
            self.base_json = json.load(f)
        self.__base_json = copy.deepcopy(self.base_json)
        self.__requests_json = self.__base_json['scenarios'][0]['requests']


    def get_base_json(self):
        del self.__base_json['scenarios'][0]['requests'][0]
        self.__base_json['scenarios'][0]['id'] = str(uuid.uuid4())
        return self.__base_json

    def set_scenarios_name(self, name):
        self.__base_json['scenarios'][0]['name'] = name

    def get_requests_json(self):
        return self.__requests_json

    def new_request_json(self):
        return copy.deepcopy(self.base_json['scenarios'][0]['requests'][0])

    def set_requests_json(self, request_json):
        self.__requests_json.append(request_json)
        return self.__requests_json

    def __str__(self):
        return self.__requests_json


if __name__ == '__main__':
    # rootNode = readXML()
    # s = rootNode.getElementsByTagName('con:testSuite')
    # for _testSuite in s:
    #    if _testSuite.getAttribute('name') != 'LoadConfigs':
    #        property = rootNode.getElementsByTagName('con:properties')
    #        for _property in property.getElementsByTagName('con:property'):
    #            print("##"*20+_property.getElementsByTagName('con:name')[0].childNodes[0].data)
    #            print("##" * 20 + _property.getElementsByTagName('con:value')[0].childNodes[0].data)
    #        print('=='*20+_testSuite.getAttribute('name')+'=='*20)
    #        for _testCase in _testSuite.getElementsByTagName('con:testCase'):
    #            print('**'*10+_testCase.getAttribute('name')+'**'*10)
    #            for _testStep in _testCase.getElementsByTagName('con:testStep'):
    #                if _testStep.getAttribute('name') != 'SetUp':
    #                    print( _testStep.getAttribute('name'))
    #                    if _testStep.getAttribute('type') == 'groovy':
    #                        print(_testStep.getAttribute('name'))
    #                        # print(_testStep.getElementsByTagName('script')[0].childNodes[0].data)
    #                    elif _testStep.getAttribute('type') == 'restrequest':
    #                        # restRequest = _testStep.getElementsByTagName('con:restRequest')
    #                        path = _testStep.getElementsByTagName('con:config')[0].getAttribute('resourcePath')
    #                        print(path)

    # project = SoapUIXML('SaveLogic-soapui-project-cwgx.xml')
    # suite_nodes = project.get_testsuite_nodes()
    # for suite_node in suite_nodes:
    #     case_nodes = project.get_testcase_nodes(suite_node)

    result = MeterSphereBaseJson('models.json')
    base_json = result.get_base_json()
    print(base_json)
    requests_json = result.get_requests_json()
    request_json = result.new_request_json()
    request_json['type'] = 'sql'
    request_json1 = result.new_request_json()
    request_json1['type'] = 'tcp'
    result.set_requests_json(request_json)
    last_requests = result.set_requests_json(request_json1)
    print(last_requests)
    base_json['scenarios'][0]['name'] = '财务共享'

    print('last_base_json', json.dumps(base_json))
