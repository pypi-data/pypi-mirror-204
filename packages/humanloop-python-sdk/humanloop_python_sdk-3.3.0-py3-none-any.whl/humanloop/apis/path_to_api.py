import typing_extensions

from humanloop.paths import PathValues
from humanloop.apis.paths.projects import Projects
from humanloop.apis.paths.projects_id import ProjectsId
from humanloop.apis.paths.projects_id_model_configs import ProjectsIdModelConfigs
from humanloop.apis.paths.projects_id_model_config import ProjectsIdModelConfig
from humanloop.apis.paths.projects_id_active_model_config import ProjectsIdActiveModelConfig
from humanloop.apis.paths.projects_id_active_experiment import ProjectsIdActiveExperiment
from humanloop.apis.paths.projects_id_feedback_types import ProjectsIdFeedbackTypes
from humanloop.apis.paths.projects_id_export import ProjectsIdExport
from humanloop.apis.paths.generate import Generate
from humanloop.apis.paths.chat import Chat
from humanloop.apis.paths.logs import Logs
from humanloop.apis.paths.feedback import Feedback
from humanloop.apis.paths.model_configs import ModelConfigs
from humanloop.apis.paths.model_configs_id import ModelConfigsId
from humanloop.apis.paths.projects_project_id_experiments import ProjectsProjectIdExperiments
from humanloop.apis.paths.experiments_experiment_id import ExperimentsExperimentId
from humanloop.apis.paths.experiments_experiment_id_model_config import ExperimentsExperimentIdModelConfig

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.PROJECTS: Projects,
        PathValues.PROJECTS_ID: ProjectsId,
        PathValues.PROJECTS_ID_MODELCONFIGS: ProjectsIdModelConfigs,
        PathValues.PROJECTS_ID_MODELCONFIG: ProjectsIdModelConfig,
        PathValues.PROJECTS_ID_ACTIVEMODELCONFIG: ProjectsIdActiveModelConfig,
        PathValues.PROJECTS_ID_ACTIVEEXPERIMENT: ProjectsIdActiveExperiment,
        PathValues.PROJECTS_ID_FEEDBACKTYPES: ProjectsIdFeedbackTypes,
        PathValues.PROJECTS_ID_EXPORT: ProjectsIdExport,
        PathValues.GENERATE: Generate,
        PathValues.CHAT: Chat,
        PathValues.LOGS: Logs,
        PathValues.FEEDBACK: Feedback,
        PathValues.MODELCONFIGS: ModelConfigs,
        PathValues.MODELCONFIGS_ID: ModelConfigsId,
        PathValues.PROJECTS_PROJECT_ID_EXPERIMENTS: ProjectsProjectIdExperiments,
        PathValues.EXPERIMENTS_EXPERIMENT_ID: ExperimentsExperimentId,
        PathValues.EXPERIMENTS_EXPERIMENT_ID_MODELCONFIG: ExperimentsExperimentIdModelConfig,
    }
)

path_to_api = PathToApi(
    {
        PathValues.PROJECTS: Projects,
        PathValues.PROJECTS_ID: ProjectsId,
        PathValues.PROJECTS_ID_MODELCONFIGS: ProjectsIdModelConfigs,
        PathValues.PROJECTS_ID_MODELCONFIG: ProjectsIdModelConfig,
        PathValues.PROJECTS_ID_ACTIVEMODELCONFIG: ProjectsIdActiveModelConfig,
        PathValues.PROJECTS_ID_ACTIVEEXPERIMENT: ProjectsIdActiveExperiment,
        PathValues.PROJECTS_ID_FEEDBACKTYPES: ProjectsIdFeedbackTypes,
        PathValues.PROJECTS_ID_EXPORT: ProjectsIdExport,
        PathValues.GENERATE: Generate,
        PathValues.CHAT: Chat,
        PathValues.LOGS: Logs,
        PathValues.FEEDBACK: Feedback,
        PathValues.MODELCONFIGS: ModelConfigs,
        PathValues.MODELCONFIGS_ID: ModelConfigsId,
        PathValues.PROJECTS_PROJECT_ID_EXPERIMENTS: ProjectsProjectIdExperiments,
        PathValues.EXPERIMENTS_EXPERIMENT_ID: ExperimentsExperimentId,
        PathValues.EXPERIMENTS_EXPERIMENT_ID_MODELCONFIG: ExperimentsExperimentIdModelConfig,
    }
)
