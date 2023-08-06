# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from taurus_datajob_api.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    DATAJOBS_FORTEAM_TEAM_NAME_INFO = "/data-jobs/for-team/{team_name}/info"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS = "/data-jobs/for-team/{team_name}/jobs"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME = "/data-jobs/for-team/{team_name}/jobs/{job_name}"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_KEYTAB = "/data-jobs/for-team/{team_name}/jobs/{job_name}/keytab"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_TEAM_NEW_TEAM = "/data-jobs/for-team/{team_name}/jobs/{job_name}/team/{new_team}"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_DEPLOYMENTS = "/data-jobs/for-team/{team_name}/jobs/{job_name}/deployments"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_DEPLOYMENTS_DEPLOYMENT_ID = "/data-jobs/for-team/{team_name}/jobs/{job_name}/deployments/{deployment_id}"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_EXECUTIONS = "/data-jobs/for-team/{team_name}/jobs/{job_name}/executions"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_DEPLOYMENTS_DEPLOYMENT_ID_EXECUTIONS = "/data-jobs/for-team/{team_name}/jobs/{job_name}/deployments/{deployment_id}/executions"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_EXECUTIONS_EXECUTION_ID = "/data-jobs/for-team/{team_name}/jobs/{job_name}/executions/{execution_id}"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_EXECUTIONS_EXECUTION_ID_LOGS = "/data-jobs/for-team/{team_name}/jobs/{job_name}/executions/{execution_id}/logs"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_DEPLOYMENTS_DEPLOYMENT_ID_PROPERTIES = "/data-jobs/for-team/{team_name}/jobs/{job_name}/deployments/{deployment_id}/properties"
    DATAJOBS_FORTEAM_TEAM_NAME_JOBS_JOB_NAME_SOURCES = "/data-jobs/for-team/{team_name}/jobs/{job_name}/sources"
