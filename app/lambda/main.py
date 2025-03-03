import logging
import smtplib
import os
from email.mime.text import MIMEText
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response # type: ignore
from ask_sdk_model.services.list_management import ListManagementServiceClient
import boto3
from botocore.exceptions import ClientError
from jinja2 import Template
from ask_sdk_model.services.ups import UpsServiceClient

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to your shopping list skill. You can ask me to send your shopping list via email.  Local A1"
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

class SendShoppingListIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SendItIntent")(handler_input)

    def handle(self, handler_input):
        # Ensure environment variables are set
        from_email = os.getenv("FROM_EMAIL")
        aws_region = os.getenv("AWS_REGION")

        if not from_email or not aws_region:
            logger.error("Environment variables FROM_EMAIL and AWS_REGION must be set.")
            speech_text = "There is a configuration error. Please check the environment variables. Local B1"
            return handler_input.response_builder.speak(speech_text).response

        # Get the shopping list from Alexa
        shopping_list = self.get_shopping_list(handler_input)

        # Get the user's email address from their Alexa profile
        ups_service_client = handler_input.service_client_factory.get_ups_service()
        user_email = ups_service_client.get_profile_email()

        if not user_email:
            speech_text = "I couldn't find your email address in your Alexa profile. Please check your settings."
            return handler_input.response_builder.speak(speech_text).response

        # Send email
        self.send_email(user_email, shopping_list)

        speech_text = "I have sent your shopping list to your email."
        return handler_input.response_builder.speak(speech_text).response

    def get_shopping_list(self, handler_input):
        service_client_factory = handler_input.service_client_factory
        list_client = service_client_factory.get_list_management_service()
        lists_metadata = list_client.get_lists_metadata()
        shopping_list_id = None

        for list_metadata in lists_metadata.lists:
            if list_metadata.name == "Alexa shopping list":
                shopping_list_id = list_metadata.list_id
                break

        if not shopping_list_id:
            return []

        list_items = list_client.get_list(shopping_list_id, "active").items
        return [item.value for item in list_items]

    def send_email(self, to_email, shopping_list):
        from_email = os.getenv("FROM_EMAIL")  # Get from email from environment variable
        aws_region = os.getenv("AWS_REGION")  # Get AWS region from environment variable

        subject = "Your Shopping List"

        # Load and render the HTML template
        try:
            with open("/home/rob/Projects/alexa_sendlist/alexa-skill-project/alexa-skill/src/email_template.html") as file:
                template = Template(file.read())
            body = template.render(shopping_list=shopping_list)
        except Exception as e:
            logger.error(f"Error loading email template: {e}")
            return

        client = boto3.client('ses', region_name=aws_region)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [to_email],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': "UTF-8",
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=from_email,
            )
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
        else:
            logger.info("Email sent! Message ID:"),
            logger.info(response['MessageId'])

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SendShoppingListIntentHandler())

handler = sb.lambda_handler()
