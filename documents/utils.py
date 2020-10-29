import os
from google.cloud import vision
from google.cloud import storage
import re
import json
from google.cloud import language_v1
from dumbo.settings import BASE_DIR


def from_document(source_uri: str, destination_uri: str):
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
    operation.result(timeout=360)
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    blob_names = [blob.name for blob in blob_list]

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
    return text_response, blob_names


def extract_text(from_: str = 'remote', dtype: str = 'image', location: str = None, destination_uri: str = None):
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
        return from_document(location, destination_uri)


# For document text retrieval
# src = 'gs://dumbo-document-storage/documents/Group44_ML_Assignment2_report.pdf'
# des = 'gs://dumbo-document-storage/tags/ReportTags'

# text = from_document('gs://dumbo-document-storage/documents/Group44_ML_Assignment2_report.pdf',
#                      'gs://dumbo-document-storage/tags/ReportTags')
#
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credential.json"


def classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={'document': document})
    categories = response.categories

    categories_list = []

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        # result[category.name] = category.confidence
        categories_list.append(category.name)

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response1 = language_client.analyze_entities(request={'document': document, 'encoding_type': encoding_type})

    # Loop through entities returned from the API
    entities_list = []
    for entity in response1.entities:
        if entity.salience > 0.05:
            entities_list.append(entity.name)
        else:
            break

    return categories_list, entities_list


def split_labels(categories):
    category_list = []
    for name in categories:
        labels = [label for label in name.split("/") if label]
        for label in labels:
            category_list.append(label)

    return category_list


def get_tags(source_uri: str, dest_uri: str, dtype: str):
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(BASE_DIR, 'credential.json')
    if dtype == 'image':
        ret_text = extract_text('remote', dtype, source_uri, dest_uri)
    else:
        # Text is a list of string, blob-names are returned
        ret_text, blob_names = extract_text('remote', 'document', source_uri, dest_uri)
        ret_text = '\n'.join(ret_text)
        storage_client = storage.Client()
        for blob_name in blob_names:
            bucket = storage_client.bucket('dumbo-document-storage')
            blob = bucket.blob(blob_name)
            blob.delete()
    categories, entities = classify(ret_text)
    categories = list(set(split_labels(categories)))
    tags = categories + entities
    return ', '.join(tags)


src = 'gs://dumbo-document-storage/documents/Group44_ML_Assignment2_report.pdf'
dst = 'gs://dumbo-document-storage/tags/ReportTags'

print(get_tags(src, dst, 'pdf'))