from typing import Dict, Any, List
import requests

class TgglResponse:
    def __init__(self, flags: Dict[str, Any] = {}):
        self.__flags = flags

    def is_active(self, slug: str):
        return slug in self.__flags

    def get(self, slug: str, default_value=None):
        return self.__flags.get(slug, default_value)

class TgglClient(TgglResponse):
    def __init__(self, api_key: str, url: str = 'https://api.tggl.io/flags', initial_active_flags: Dict[str, Any] = {}):
        super().__init__(initial_active_flags)
        self.__api_key = api_key
        self.__url = url

    def eval_context(self, context: Dict[str, Any]):
        responses = self.eval_contexts([context])
        return responses[0]

    def eval_contexts(self, contexts: List[Dict[str, Any]]):
        try:
            if not isinstance(contexts, List):
                raise ValueError('Invalid Tggl contexts, contexts must be a List')

            for context in contexts:
                if not isinstance(context, dict):
                    raise ValueError('Invalid Tggl context, context must be a dict')

            response = requests.post(
                url=self.__url,
                json=contexts,
                headers={
                    'x-tggl-api-key': self.__api_key
                }
            )

            return response.json()

        except Exception as e:
            print(e)
            return [TgglResponse() for _ in range(len(contexts))]
