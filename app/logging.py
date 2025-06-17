import logging

def init():
    log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    # Reduce the noise:
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    # logging.getLogger("uvicorn.access").setLevel(logging.ERROR)

    root_logger = logging.getLogger()
    root_logger.info(f"Logging initialized with level: {logging.getLevelName(root_logger.level)}    ")