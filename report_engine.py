import statistics
import math
from datetime import datetime
import azure.functions as func
import logging


def analyse_events(events):
    if not events:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "success_percentage": 0.0,
                "average_response_time": 0.0
            }
    total_requests = len(events)
    average_response_time = statistics.mean([item["response_ms"] for item in events])
        
    success = 0
    for item in events:
            if item["status_code"] >= 200 and item["status_code"] < 300:
                success += 1
        
    return {
            "total_requests": total_requests,
            "successful_requests": success,
            "success_percentage": (success / total_requests) * 100 if total_requests > 0 else 0,
            "average_response_time": average_response_time
        }
    
    # call empty list to test the function
empty_result = (analyse_events([]))
    
def validate_event(event):
# Check that the input is a dictionary with all required fields.
      if not isinstance(event, dict):
        return False
    
      required_keys = [
        "event_id",
        "service",
        "status_code",
        "response_ms",
        "timestamp",
      ]
      if any(key not in event for key in required_keys):
        return False
    
      # Validate text fields.
      for field in ["event_id", "service"]:
        if not isinstance(event[field], str) or not event[field].strip():
          return False
    
      # Validate HTTP status code.
      if type(event["status_code"]) is not int:
        return False
      if not 100 <= event["status_code"] <= 599:
        return False
    
      # Validate response time as a finite, non-negative number.
      if type(event["response_ms"]) not in (int, float):
        return False
      if not math.isfinite(event["response_ms"]) or event["response_ms"] < 0:
        return False
    
      # Validate timestamp format and timezone.
      if not isinstance(event["timestamp"], str):
        return False
      try:
        timestamp = datetime.fromisoformat(
          event["timestamp"].replace("Z", "+00:00")
        )
      except ValueError:
        return False
    
      if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
        return False
    
      # All checks passed.
      return True

    
def validate_events(events): 
 #check that the input is a list
  if not isinstance(events, list):
    return False
  
  # store IDs already encounted to check for duplicates 
  seen_ids = set()
  
  # check every event
  for event in events:
    if not validate_event(event): # validate the individual record
      return False
    #check for duplicate event IDs
    if event["event_id"] in seen_ids:
      return False 
    # remember this event ID
    seen_ids.add(event["event_id"])
    #all records passed validation
  return True

