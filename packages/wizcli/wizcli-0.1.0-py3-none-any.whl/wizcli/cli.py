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
    host: str = typer.Option(None, "--host", "-h", envvar="WIZ_HOST"),
    port: int = 38899,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    if not host:
        raise typer.Abort("Missing host.")

    if verbose:
        typer.echo(f"WiZ {host=} {port=}")

    ctx.obj = State(
        wiz=Wiz(host, port),
        verbose=verbose
    )


@run.command()
def on(ctx: typer.Context):
    ctx.obj.wiz.on()


@run.command()
def off(ctx: typer.Context):
    ctx.obj.wiz.off()


@run.command()
def dim(
    ctx: typer.Context,
    value: int = typer.Argument(50, min=0, max=100),
):
    ctx.obj.wiz.set_brightness(value)


@run.command()
def temp(
    ctx: typer.Context,
    value: int = typer.Argument(None, min=0, max=100),
):
    kelvin = value * (6500 - 2200) // 100 + 2200
    print(kelvin)
    ctx.obj.wiz.set_temp(kelvin)


@run.command()
def hot(ctx: typer.Context):
    ctx.obj.wiz.set_temp(2200)


@run.command()
def cold(ctx: typer.Context):
    ctx.obj.wiz.set_temp(6500)


@run.command()
def rgb(
    ctx: typer.Context,
    r: int = typer.Argument(None, min=0, max=255),
    g: int = typer.Argument(None, min=0, max=255),
    b: int = typer.Argument(None, min=0, max=255),
):
    ctx.obj.wiz.set_color((r, g, b))


if __name__ == "__main__":
    run()
