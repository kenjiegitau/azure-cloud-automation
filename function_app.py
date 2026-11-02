import azure.functions as func
import logging
from report_workflow import generate_report
from blob_storage import upload_report

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
@app.route(route="http_trigger") # http trigger
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get("HealthCheck")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('HealthCheck')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
# time trigger
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False,
  )

def heartbeat(timer: func.TimerRequest):
    logging.info("Heartbeat excecuted successfully")
    
# call the function and store returned path file
    report_path = generate_report()
    blob_name = upload_report(report_path)

# display the returned path in the azure functions terminal
    logging.info(f"Report generated: {report_path}")
    logging.info(f"Report uploaded to Blob Storage: {blob_name}")
    