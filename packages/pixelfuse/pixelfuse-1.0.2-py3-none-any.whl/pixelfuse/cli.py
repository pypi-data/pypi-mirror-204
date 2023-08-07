from ffmpegio import FFmpegError
import typer
from typing import Optional
from rich import print

from pixelfuse.src.f2v import ToVideo
from pixelfuse.src.v2f import ToFile

app = typer.Typer()

@app.command(name="videoToFile")
def convertToFile(path: str, verbose: Optional[int]=2, show_log: Optional[bool]=False):
    try:
        c = ToFile(path, verbose, show_log)
        c.convert()
    except FFmpegError as e:
        print("[red bold]FFmgeg error:")
        print(str(e).replace("show_log=True", "--show_log"))
    except UnicodeDecodeError as e:
        print(f"[red bold]Cannot decode frames:[/red bold] {e}")
    except Exception as e:
        print(f"[red bold]Unknown error:")
        print(e)

@app.command(name="fileToVideo")
def convertToVideo(
    path: str,
    fps: Optional[float]=1.,
    width: Optional[int]=480,
    height: Optional[int]=640,
    fourcc: Optional[str]="HFYU",
    output: Optional[str]="output.avi",
    verbose: Optional[int]=2,
):
    try:
        c = ToVideo(path, fps, width, height, fourcc, output, verbose)
        c.convert()
    except FileNotFoundError:
        print(f"[red bold]File {path} doesn't exist")
    except Exception as e:
        print("[red bold]Unknown error:")
        print(e)