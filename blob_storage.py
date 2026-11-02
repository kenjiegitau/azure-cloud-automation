import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from pathlib import Path

def upload_report(report_path):
   # 1. Check that the report file exists
    report_path = Path(report_path)

    if not report_path.is_file():
        raise FileNotFoundError(f"Report not found: {report_path}")

    # retrieve azurite connection string (using an environment variable)
    connection_string = os.getenv("AzureWebJobsStorage")

    if not connection_string:
       error_msg = "AzureWebJobsStorage is not configured"
       logging.error(error_msg)
       raise ValueError(error_msg)


    # connect to Azurite
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string,
        api_version="2023-11-03"
    )
    # select the storage container
    container_client = blob_service_client.get_container_client("saas-performance-report")
    logging.info("BlobServiceClient initialised successfully")

    # create the container, handling the possibility that it already exists
    try:
        container_client.create_container()
        logging.info("Container created successfully.")

    except ResourceExistsError:
        logging.info("Container already exists. Safe to proceed.")

    # use the correct file name
    blob_name = report_path.name
    blob_client = container_client.get_blob_client(blob_name)

    # upload the json report
    with open(report_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    # verify the upload
    if not blob_client.exists():
        raise RuntimeError("Blob upload verification failed")
    # retrieve uploaded file properties
    properties = blob_client.get_blob_properties()

    logging.info(
        "Upload verified: %s (%s bytes)",
        blob_name,
        properties.size
    )

    return blob_name
