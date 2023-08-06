import typing_extensions

from taurus_datajob_api.apis.tags import TagValues
from taurus_datajob_api.apis.tags.data_jobs_api import DataJobsApi
from taurus_datajob_api.apis.tags.data_jobs_deployment_api import DataJobsDeploymentApi
from taurus_datajob_api.apis.tags.data_jobs_execution_api import DataJobsExecutionApi
from taurus_datajob_api.apis.tags.data_jobs_properties_api import DataJobsPropertiesApi
from taurus_datajob_api.apis.tags.data_jobs_service_api import DataJobsServiceApi
from taurus_datajob_api.apis.tags.data_jobs_sources_api import DataJobsSourcesApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.DATA_JOBS: DataJobsApi,
        TagValues.DATA_JOBS_DEPLOYMENT: DataJobsDeploymentApi,
        TagValues.DATA_JOBS_EXECUTION: DataJobsExecutionApi,
        TagValues.DATA_JOBS_PROPERTIES: DataJobsPropertiesApi,
        TagValues.DATA_JOBS_SERVICE: DataJobsServiceApi,
        TagValues.DATA_JOBS_SOURCES: DataJobsSourcesApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.DATA_JOBS: DataJobsApi,
        TagValues.DATA_JOBS_DEPLOYMENT: DataJobsDeploymentApi,
        TagValues.DATA_JOBS_EXECUTION: DataJobsExecutionApi,
        TagValues.DATA_JOBS_PROPERTIES: DataJobsPropertiesApi,
        TagValues.DATA_JOBS_SERVICE: DataJobsServiceApi,
        TagValues.DATA_JOBS_SOURCES: DataJobsSourcesApi,
    }
)
