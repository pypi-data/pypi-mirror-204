import typing_extensions

from humanloop.apis.tags import TagValues
from humanloop.apis.tags.projects_api import ProjectsApi
from humanloop.apis.tags.experiments_api import ExperimentsApi
from humanloop.apis.tags.generate_api import GenerateApi
from humanloop.apis.tags.model_configs_api import ModelConfigsApi
from humanloop.apis.tags.logs_api import LogsApi
from humanloop.apis.tags.feedback_api import FeedbackApi
from humanloop.apis.tags.authentication_api import AuthenticationApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.PROJECTS: ProjectsApi,
        TagValues.EXPERIMENTS: ExperimentsApi,
        TagValues.GENERATE: GenerateApi,
        TagValues.MODEL_CONFIGS: ModelConfigsApi,
        TagValues.LOGS: LogsApi,
        TagValues.FEEDBACK: FeedbackApi,
        TagValues.AUTHENTICATION: AuthenticationApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.PROJECTS: ProjectsApi,
        TagValues.EXPERIMENTS: ExperimentsApi,
        TagValues.GENERATE: GenerateApi,
        TagValues.MODEL_CONFIGS: ModelConfigsApi,
        TagValues.LOGS: LogsApi,
        TagValues.FEEDBACK: FeedbackApi,
        TagValues.AUTHENTICATION: AuthenticationApi,
    }
)
