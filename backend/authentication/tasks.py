from celery import shared_task, Task
from backend.celery import app
from celery.utils.log import get_task_logger
from .models import NonceSignRequest, UserData
from .serializers import NonceSignRequestSerializer
from lib.utils import get_address_from_signature

logger = get_task_logger(__name__)


@app.task
def generate_nonce(address, user_pk=0):
    data = {
        'address': address,
    }
    if user_pk:
        data['user_pk'] = user_pk
    serializer = NonceSignRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

@app.task
def check_nonce(nonce, address, signature):
    try:
        nonce_request = NonceSignRequest.objects.get(
            nonce=nonce,
            address=address,
            )
    except:
        return False
    verified_address = get_address_from_signature(nonce, signature)
    logger.info(f'address: {verified_address}')
    logger.info(f'nonce: {nonce} signature: {signature}')
    # nonce_request.delete() # ??
    return verified_address == address