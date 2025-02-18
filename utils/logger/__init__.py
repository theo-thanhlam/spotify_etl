from logging import *
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")



basicConfig(
    filename=f"log/{today}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime},{levelname},{message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=NOTSET
)



