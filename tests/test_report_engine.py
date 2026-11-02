import pytest
from report_engine import validate_event
from report_engine import validate_events
from report_engine import analyse_events
import json 
from pathlib import Path 
from report_workflow import generate_report

# test function whose name begins with test_
def test_validate_event_with_valid_synthetic_data():
    
    # synthetic event dictionary with all five required fields
    # every field has a valid value (realistic HTTP status, non-negative response time, UTC timestamp)
    synthetic_event = {
        "event_id": "evt_987654321",
        "service": "saas-performance-report",
        "status_code": 200,
        "response_ms": 142,
        "timestamp": "2026-10-31T12:58:00Z"
    }
    
    # call validate_event() using dictionary
    result = validate_event(synthetic_event)
    
    # use assert to check that the result is True
    assert result is True

# begin negative testing
def test_required_field_missing_data():
    # synthetic event dictionary 
    synthetic_event = {
        "event_id": "evt_987654321",
        "service": "saas-performance-report",
        "response_ms": 160,
        "timestamp": "2026-10-31T13:06:35Z"
    }
     
    # call validate_event() using negative dictionary
    result = validate_event(synthetic_event)

    # use assert to check that the result is false
    assert result is False
    
def test_negative_response_time():
        # synthetic event dictionary 
        synthetic_event = {
                "event_id": "evt_987654321",
                "service": "saas-performance-report",
                "status_code": 200,
                "response_ms": -60,
                "timestamp": "2026-10-31T13:06:35Z"
            }
        # call validate_event() using negative dictionary
        result = validate_event(synthetic_event)
        # use assert to check that the result is false
        assert result is False
    
def test_invalid_timestamp():
        # synthetic event dictionary 
        synthetic_event = {
                        "event_id": "evt_987654321",
                        "service": "saas-performance-report",
                        "status_code": 200,
                        "response_ms": 156,
                        "timestamp": "not-a-date"
        }
        # call validate_event() using negative dictionary
        result = validate_event(synthetic_event)
        # use assert to check that the result is false
        assert result is False
        
def test_duplicate_event_ids():
    # Two events share an ID, so the collection should be rejected.
    synthetic_events = [
        {
            "event_id": "EVT-001",
            "service": "customer-api",
            "status_code": 200,
            "response_ms": 120,
            "timestamp": "2026-10-31T14:32:02Z",
        },
        {
            "event_id": "EVT-001",
            "service": "billing-api",
            "status_code": 200,
            "response_ms": 143,
            "timestamp": "2026-10-31T15:01:22Z",
        },
    ]

    result = validate_events(synthetic_events)
    assert result is False
    
def test_analyse_events():

    synthetic_events = [
        {
            "event_id": "EVT-001",
            "service": "customer-api",
            "status_code": 200,
            "response_ms": 100,
            "timestamp": "2026-10-31T14:32:02Z",
        },
        {
            "event_id": "EVT-002",
            "service": "billing-api",
            "status_code": 500,
            "response_ms": 300,
            "timestamp": "2026-10-31T15:01:22Z",
        },
    ]

    result = analyse_events(synthetic_events)
    assert result ["total_requests"] == 2
    assert result ["successful_requests"] == 1
    assert result ["success_percentage"] == 50.0
    assert result ["average_response_time"] == 200.0
    
def test_generate_report():
    # call generate_report() and store its returned file path
    report_path = generate_report()
    # confirm the report exists
    report_path = Path(report_path)
    assert report_path.is_file()
    # read the report using json.load()
    with report_path.open("r", encoding="utf-8") as f:
        report_data = json.load(f)
        
    # check required sections
    assert "overall" in report_data
    assert "services" in report_data

    # check that the overall request count equals 12
    total_count = report_data["overall"].get("total_requests")
    assert total_count == 12