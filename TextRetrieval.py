import os
from google.cloud import vision
from google.cloud import storage
import re
import json


def from_document(source_uri: str, destination_uri: str):
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credential.json'
    mime_type = 'application/pdf'  # Supported mime_types are: 'application/pdf' and 'image/tiff'
    batch_size = 2  # How many pages should be grouped into each json output file.

    client = vision.ImageAnnotatorClient()
    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION  # The feature we are going to use
    )
    gcs_source = vision.GcsSource(uri=source_uri)  # The source of the files
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)  # Configuring the operation
    gcs_destination = vision.GcsDestination(uri=destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)
    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)
    operation = client.async_batch_annotate_files(
        requests=[async_request])
    print('Waiting for the operation to finish.')
    operation.result(timeout=420)
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    text_response = []
    for output in blob_list:
        json_string = output.download_as_string()
        response = json.loads(json_string)

        # The actual response for the first page of the input file.
        first_page_response = response['responses'][0]
        annotation = first_page_response['fullTextAnnotation']

        text_response.append(annotation['text'])
    return text_response


def extract_text(from_: str = 'remote', dtype: str = 'image', location: str = None, destination_uri: str = None):
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credential.json'
    client = vision.ImageAnnotatorClient()  # Initialize a vision client
    if dtype == 'image':
        # We perform `TEXT_DETECTION`
        if from_ == 'local':
            with open(location, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

        elif from_ == 'remote':  # If from GCloud, location is of format : gs://{bucket-name}/{file-path}
            image = vision.Image()  # Instantiate an image object
            image.source.image_uri = location  # Supply the image URL

        response = client.text_detection(image=image)  # The response object
        parent_object = response.text_annotations  # `parent_object` has additional details such as bounding boxes etc
        text = parent_object[0].description  # Grab all the text in a single place
        return text
    elif dtype == 'document' or dtype == 'pdf':
        # Document doesn't mean pdf, if dtype = 'document'
        # Even if the input is an image(TIFF), we perform `DOCUMENT_TEXT_DETECTION`
        from_document(location, destination_uri)


# For document text retrieval
# src = 'gs://dumbo-document-storage/documents/Group44_ML_Assignment2_report.pdf'
# des = 'gs://dumbo-document-storage/tags/ReportTags'

print(from_document('gs://dumbo-document-storage/documents/Group44_ML_Assignment2_report.pdf', 'gs://dumbo-document-storage/tags/ReportTags'))