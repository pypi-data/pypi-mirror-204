# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from taurus_datajob_api.paths.data_jobs_for_team_team_name_info import Api

from taurus_datajob_api.paths import PathValues

path = PathValues.DATAJOBS_FORTEAM_TEAM_NAME_INFO