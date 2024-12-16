import logging
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import azure.functions as func

# Définir l'application Azure Function
app = func.FunctionApp()

@app.function_name(name="BlobToQueueFunction")
@app.blob_trigger(arg_name="blob", path="images/{name}", connection="AzureWebJobsStorage")
def BlobToQueueFunction(blob: func.InputStream):
    # Lecture du nom et de la taille du fichier
    name = blob.name
    size = len(blob.read())
    logging.info(f"Blob Triggered: {name}, Size: {size} bytes")

    # Connexion à Azure Service Bus
    connection_string = os.environ["SERVICE_BUS_CONNECTION_STRING"]
    queue_name = os.environ["SERVICE_BUS_QUEUE_NAME"]

    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_queue_sender(queue_name) as sender:
            message = ServiceBusMessage(name)
            sender.send_messages(message)
            logging.info(f"Sent file name '{name}' to queue {queue_name}")
