import json 
from pathlib import Path 

from report_engine import analyse_events, validate_events

def generate_report():
    
    # find the project folder
    base_dir = Path(__file__).resolve().parent

    # load the event data
    data_path = base_dir / "data" / "sample_events.json"

    with data_path.open("r", encoding="utf-8") as f:
            events = json.load(f)

    # 3. Validate the dataset
    if not validate_events(events):
            raise ValueError("Dataset validation failed")

    # 4. Discover the services automatically
    services = sorted({event["service"] for event in events})

    # 5. Generate the report
    report = {
            "overall": analyse_events(events),
            "services": {}
        }

    for service in services:
            service_events = [
                event for event in events
                if event["service"] == service
            ]

    report["services"][service] = analyse_events(service_events)

    # 6. Create the reports folder
    reports_folder = base_dir / "reports"
    reports_folder.mkdir(exist_ok=True)

    # 7. Save the report
    report_path = reports_folder / "saas_performance_report.json"

    with report_path.open("w", encoding="utf-8") as f:
     json.dump(report, f, indent=4)

    # 8. Return the saved file location
    return report_path