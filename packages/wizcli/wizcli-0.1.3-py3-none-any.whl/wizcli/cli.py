import math
from dataclasses import dataclass

import typer
from .wiz import Wiz

run = typer.Typer()

@dataclass
class State:
    wiz: Wiz
    verbose: bool


@run.callback()
def common(
    ctx: typer.Context,
    host: str = typer.Option(None, "--host", "-h", envvar="WIZ_HOST", help="WiZ bulb host"),
    port: int = typer.Option(38899, "--port", "-p", envvar="WIZ_PORT", help="WiZ bulb port"),
    timeout: int = typer.Option(5, "--timeout", "-t", envvar="WIZ_TIMEOUT", help="Timeout in seconds"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    if not host:
        print("Missing host.")
        raise typer.Abort()

    if verbose:
        typer.echo(f"WiZ {host=} {port=}")

    ctx.obj = State(
        wiz=Wiz(host, port, timeout=timeout),
        verbose=verbose
    )


@run.command()
def on(ctx: typer.Context):
    ctx.obj.wiz.on()


@run.command()
def off(ctx: typer.Context):
    ctx.obj.wiz.off()


@run.command()
def switch(ctx: typer.Context):
    state = ctx.obj.wiz.get_state()
    if state["state"]:
        ctx.obj.wiz.off()
    else:
        ctx.obj.wiz.on()


@run.command()
def dim(
    ctx: typer.Context,
    value: int = typer.Argument(50, min=0, max=100, help="%"),
):
    value = math.floor(value / 100 * 255)
    ctx.obj.wiz.set_brightness(value)


@run.command()
def temp(
    ctx: typer.Context,
    value: int = typer.Argument(50, min=0, max=100, help="%"),
):
    k = math.floor(value * (6500 - 2200) / 100 + 2200)
    ctx.obj.wiz.set_temp(k)


@run.command()
def warm(
    ctx: typer.Context,
    value: int = typer.Argument(100, min=0, max=100, help="%"),
):
    value = math.floor(value / 100 * 255)
    ctx.obj.wiz.set_warm(value)


@run.command()
def cold(
    ctx: typer.Context,
    value: int = typer.Argument(100, min=0, max=100, help="%"),
):
    value = math.floor(value / 100 * 255)
    ctx.obj.wiz.set_cold(value)


@run.command()
def rgb(
    ctx: typer.Context,
    r: int = typer.Argument(0, min=0, max=255),
    g: int = typer.Argument(0, min=0, max=255),
    b: int = typer.Argument(0, min=0, max=255),
):
    ctx.obj.wiz.set_color((r, g, b))


if __name__ == "__main__":
    run()
