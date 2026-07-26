import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.catalogs.models import RepairCategory, PropertyType, Country, Department, City, Neighborhood
from apps.properties.models import Property
from apps.repairs.models import RepairIncident, RepairOrder, RepairPriority, RepairSeverity, RepairType
from apps.repairs.state_machine import RepairStateMachine
from apps.repairs.services import RepairService


@pytest.fixture
def test_property(db):
    country, _ = Country.objects.get_or_create(code="CO", defaults={"name": "Colombia"})
    department, _ = Department.objects.get_or_create(code="CO-VAC", country=country, defaults={"name": "Valle del Cauca"})
    city, _ = City.objects.get_or_create(code="CO-VAC-CALI", department=department, defaults={"name": "Cali"})
    neighborhood, _ = Neighborhood.objects.get_or_create(code="TEQUENDAMA", city=city, defaults={"name": "Tequendama"})
    property_type, _ = PropertyType.objects.get_or_create(code="APARTMENT", defaults={"name": "Apartamento"})
    
    return Property.objects.create(
        internal_code="INM-TEST-001",
        property_type=property_type,
        address_line="Calle 5 #38-21",
        country=country,
        department=department,
        city=city,
        neighborhood=neighborhood,
        stratum=5
    )


@pytest.fixture
def test_category(db):
    category, _ = RepairCategory.objects.get_or_create(code="PLUMBING", defaults={"name": "Plomería"})
    return category


@pytest.mark.django_db
def test_create_repair_order_and_sla(test_property, test_category):
    incident = RepairIncident.objects.create(
        property=test_property,
        title="Filtración de agua en baño",
        description="Fuga de agua constante en lavamanos",
        category=test_category,
        priority=RepairPriority.CRITICAL,
        severity=RepairSeverity.HIGH,
        repair_type=RepairType.CORRECTIVE
    )

    order = RepairOrder.objects.create(
        incident=incident,
        property=test_property,
        order_number="OT-2026-0001",
        title="Reparación tubería de baño",
        description="Cambio de empaque y tubo flexible",
        category=test_category,
        priority=RepairPriority.CRITICAL,
        severity=RepairSeverity.HIGH,
        repair_type=RepairType.CORRECTIVE
    )

    assert order.status == "REPORTED"
    assert order.sla_deadline is not None
    assert order.is_overdue is False
    delta = order.sla_deadline - order.created_at
    assert abs(delta.total_seconds() - 86400) < 60


@pytest.mark.django_db
def test_state_machine_invalid_transition(test_property, test_category):
    order = RepairOrder.objects.create(
        property=test_property,
        order_number="OT-2026-0002",
        title="Mantenimiento preventivo",
        description="Revisión de contadores",
        category=test_category
    )

    with pytest.raises(ValidationError):
        RepairStateMachine.validate_transition(order, "COMPLETED")


@pytest.mark.django_db
def test_state_machine_cancellation_reason_required(test_property, test_category):
    order = RepairOrder.objects.create(
        property=test_property,
        order_number="OT-2026-0003",
        title="Mantenimiento cerrajería",
        description="Cambio de guarda",
        category=test_category
    )

    with pytest.raises(ValidationError):
        RepairStateMachine.validate_transition(order, "CANCELLED", reason="")

    assert RepairStateMachine.validate_transition(order, "CANCELLED", reason="Solicitado por propietario")


@pytest.mark.django_db
def test_integration_contract_property_summary(test_property, test_category):
    order = RepairOrder.objects.create(
        property=test_property,
        order_number="OT-2026-0004",
        title="Reparación fuga de gas",
        description="Revisión de válvula",
        category=test_category,
        priority=RepairPriority.HIGH
    )

    summary = RepairService.get_property_repairs_summary(test_property.id)
    assert summary["property_id"] == str(test_property.id)
    assert summary["total_repairs"] == 1
    assert summary["active_repairs_count"] == 1


@pytest.mark.django_db
def test_integration_contract_dashboard_widgets(test_property, test_category):
    RepairOrder.objects.create(
        property=test_property,
        order_number="OT-2026-0005",
        title="Cambio de pintura en portal",
        description="Pintura de puerta principal",
        category=test_category
    )

    widgets = RepairService.get_dashboard_widgets_data()
    assert "by_status" in widgets
    assert "by_priority" in widgets
    assert "sla_compliance_rate" in widgets
