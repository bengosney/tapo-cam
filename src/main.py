from time import sleep
from typing import Annotated

import typer
from pytapo import Tapo

app = typer.Typer()


@app.command()
def calibrate(
    username: Annotated[str, typer.Argument(envvar="CAM_USERNAME")],
    password: Annotated[str, typer.Argument(envvar="CAM_PASSWORD")],
    host: Annotated[str, typer.Argument(envvar="CAM_HOST")],
):
    print(f"Calibrating camera at {host}")
    tapo = Tapo(host, username, password)
    tapo.calibrateMotor()
    sleep(30)
    tapo.setPreset(1)
    print("Calibration complete")


if __name__ == "__main__":
    app()
