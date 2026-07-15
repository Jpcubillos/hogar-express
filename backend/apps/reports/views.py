from apps.core.api import domain_viewset_for
from apps.reports.models import OperationalAlert, ReportDefinition, ReportRun

ReportDefinitionViewSet = domain_viewset_for(ReportDefinition, ("is_active",))
ReportRunViewSet = domain_viewset_for(ReportRun, ("report_definition", "requested_by", "status", "output_format"))
OperationalAlertViewSet = domain_viewset_for(OperationalAlert, ("alert_type", "severity", "status", "due_at"))
