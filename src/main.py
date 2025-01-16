import logging
from time import sleep
from typing import Annotated

import typer
from pytapo import Tapo


def get_logger(log_level: str) -> logging.Logger:
    level = getattr(logging, log_level.upper(), None)
    if not isinstance(level, int):
        raise TypeError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


app = typer.Typer()


@app.command()
def calibrate(
    username: Annotated[str, typer.Argument(envvar="CAM_USERNAME")],
    password: Annotated[str, typer.Argument(envvar="CAM_PASSWORD")],
    host: Annotated[str, typer.Argument(envvar="CAM_HOST")],
    log_level: Annotated[str, typer.Option(autocompletion=lambda: logging._levelToName.values())] = "INFO",
):
    logger = get_logger(log_level)

    logger.info("Calibrating camera")
    logger.debug(f"Connecting to {host}")
    tapo = Tapo(host, username, password)

    tapo.calibrateMotor()
    logger.debug("Calibration command sent")

    logger.debug("Waiting for calibration to complete")
    sleep(30)

    tapo.setPreset(1)
    logger.debug("Preset 1 command sent")

    logger.info("Calibration complete")


if __name__ == "__main__":
    app()
