# hldlib

A Python package for working with Hyper Light Drifter files.

## TODO list
- way better documentation
- make **dependencies** their own class; something like
```py
class Dependencies:
    depends_on: list[int]
    depends_type: "flag" | "enemy"
    actor: HLDType | -999999
    delay: int

    @classmethod
    def from_string(cls, string: str): ...

    def to_string(self) -> str: ...
```
- make **room_settings** their own class and add level pngs; something like
```py
class RoomSettings:
    w: int # width
    h: int # height
    bg: str | Path # or PIL.Image idk
    ...

    @classmethod
    def from_string(cls, string: str): ...

    def to_string(self) -> str: ...    
```

## Examples
[Here.](https://github.com/sakhezech/hldlib/tree/master/examples)