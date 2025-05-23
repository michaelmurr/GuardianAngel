from logging import Logger
from app.repositories.valkey import get_valkey
from app.types.tracking import TrackingTaskMessage


def get_tracking_tasks_key() -> str:
  return "tracking_task"

def publish_tracking_task(message: TrackingTaskMessage) -> None:
   
  key = get_tracking_tasks_key()
  get_valkey().publish(key, message.model_dump_json())

