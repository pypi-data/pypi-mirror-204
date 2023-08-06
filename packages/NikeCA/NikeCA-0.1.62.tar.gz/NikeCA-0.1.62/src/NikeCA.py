
from NikeSF import Snowflake
from NikeQA import QA
from Dashboards._Dashboards import Dashboards
from Dashboards.InclusionExclusion._InclusionExclusion import InclusionExclusion
from Dashboards.Telemetry._Telemetry import Telemetry


class NikeCA(
    Snowflake
    , QA
    , Dashboards
    , Telemetry
    , InclusionExclusion
):
    pass
