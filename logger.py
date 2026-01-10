import logging 

def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s ||| %(levelname)s ||| %(name)s : %(message)s"
    )

    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
