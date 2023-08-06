
from NikeSF import Snowflake
from NikeQA import QA
from Dashboards.Dashboards import Dashboards
from Dashboards.InclusionExclusion.InclusionExclusion import InclusionExclusion
from Dashboards.Telemetry.Telemetry import Telemetry
from Dashboards.Telemetry.ProductUsage import ProductUsage

class NikeCA(
    Snowflake
    , QA
    , Dashboards
    , Telemetry
    , InclusionExclusion
    , ProductUsage
):
    pass
