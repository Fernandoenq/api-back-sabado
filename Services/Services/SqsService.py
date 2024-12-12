import boto3
import json
from typing import List
from Application.Configuration import Configuration
from Services.Services.AuthenticationService import AuthenticationService
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from io import BytesIO


class SqsService:
    @staticmethod
    def send_message_to_sqs(cursor, phone: str, person_name: str, image_ids: List[str], authentication_id: int) -> bool:
        """
        sqs_client = boto3.client(
            "sqs",
            aws_access_key_id=Configuration.aws_access_key_id,
            aws_secret_access_key=Configuration.aws_secret_access_key,
            region_name=Configuration.region_name
        )

        message_sqs = {
            "origin": 2,
            "phone": phone,
            "message": "Aqui estão suas fotos",
            "imageIds": image_ids
        }

        response = sqs_client.send_message(
            QueueUrl=Configuration.sqs_queue_url,
            MessageBody=json.dumps(message_sqs)
        )

        if response.get('MessageId'):
            print(f"Mensagem enviada com sucesso para {person_name} / {phone}."
                  f"ID da mensagem: {response['MessageId']}")

            AuthenticationService().set_authentication_sent(cursor, authentication_id)

            return True
        else:
            print(f"Falha ao enviar mensagem para {person_name} / {phone}.")
            return False
        """
        return AuthenticationService().set_authentication_sent(cursor, authentication_id)

    @staticmethod
    def download_image(image_id: str):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=Configuration.aws_access_key_id,
            aws_secret_access_key=Configuration.aws_secret_access_key,
            region_name=Configuration.region_name
        )
        bucket_name = Configuration.bucket_name

        try:
            s3_client.head_object(Bucket=bucket_name, Key=image_id)
        except ClientError as e:
            return None

        file_object = BytesIO()
        s3_client.download_fileobj(bucket_name, image_id, file_object)
        file_object.seek(0)
        return file_object
