import os
import unittest
import uuid
from pprint import pprint
from humanloop import Humanloop


class TestSimple(unittest.TestCase):
    """AccountHoldings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSimple(self):
        humanloop = Humanloop(
            api_key=os.environ['HUMANLOOP_API_KEY'],
            host="http://127.0.0.1:4010"
        )

        list_response = humanloop.projects.list(
            query_params = {
                'page': 0,
                'size': 10,
                'organization_id': "string_example",
                'filter': "string_example",
                'user_filter': "string_example",
                'sort_by': "name",
                'order': "asc",
            },
        )

        assert list_response is not None, "Response is none"
        generate_response = humanloop.generate(
            body = {
                "project": "project_example",
                "inputs": {
                    "Hello": "World"
                },
                "num_samples": 1,
                "stream": False,
                "model_config": {
                    "model": "model_example",
                    "temperature": 1,
                    "max_tokens": 16,
                    "top_p": 1,
                    "presence_penalty": 0,
                    "frequency_penalty": 0,
                },
            },
        )
        assert generate_response is not None, "Response is none"

        chat_response = humanloop.chat(
            body = {
                "project": "project_example",
                "messages": [
                    {
                        "role": "user",
                        "content": "content_example",
                    }
                ],
                "provider_api_keys": {
                },
                "num_samples": 1,
                "stream": False,
                "model_config": {
                    "model": "model_example",
                    "temperature": 1,
                    "max_tokens": 16,
                    "top_p": 1,
                    "presence_penalty": 0,
                    "frequency_penalty": 0,
                },
            },
        )
        assert chat_response is not None, "Response is none"



if __name__ == '__main__':
    unittest.main()