# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from taurus_datajob_api.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    DATA_JOBS = "Data Jobs"
    DATA_JOBS_DEPLOYMENT = "Data Jobs Deployment"
    DATA_JOBS_EXECUTION = "Data Jobs Execution"
    DATA_JOBS_PROPERTIES = "Data Jobs Properties"
    DATA_JOBS_SERVICE = "Data Jobs Service"
    DATA_JOBS_SOURCES = "Data Jobs Sources"
