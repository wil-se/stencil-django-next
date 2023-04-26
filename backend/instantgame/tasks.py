from backend.celery import app
from lib.utils import *
from celery.utils.log import get_task_logger
from .models import CoinFlip

logger = get_task_logger(__name__)

