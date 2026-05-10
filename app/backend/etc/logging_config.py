import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ],
    )
    
    # прибираємо спам від watchfiles
    logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
