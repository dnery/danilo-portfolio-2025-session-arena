from app.celery_main import celery_app


@celery_app.task
def process_event(event: dict):
    # FIXME send posthog event here
    # do asyncio.run something if database interaction needed
    return {"ok": True, "event": event}
