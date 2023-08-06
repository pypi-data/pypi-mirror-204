# lpdraw

This is a simple drawing package that contains Line and Circle Drawing Algorithms.
This package can display the output on terminal as well as visually appealing grayscale image.

## Usage

**Example:**
```python
from lpdraw import Line, Circle, Clear, DisplayTerminal
from lptypes import i32, Const

from numpy import empty, int32

def main():
    Width: Const[i32] = 100 # x-axis limits [0, 99]
    Height: Const[i32] = 40 # y-axis limits [0, 39]
    Screen: i32[Height, Width] = empty((Height, Width), dtype=int32)

    Clear(Height, Width, Screen)
    Line(Height, Width, Screen, 2, 4, 99, 11)
    Line(Height, Width, Screen, 0, 39, 49, 0)
    Circle(Height, Width, Screen, 52, 20, 6.0)
    DisplayTerminal(Height, Width, Screen)

main()
```
**Output:**
```bash
$ python main.py
+----------------------------------------------------------------------------------------------------+
|.                                                                                                   |
| .                                                                                                  |
|  ..                                                                                                |
|    .                                                                                               |
|     .                                                                                              |
|      .                                                                                             |
|       ..                                                                                           |
|         .                                                                                          |
|          .                                                                                         |
|           .                                                                                        |
|            ..                                                                                      |
|              .                                                                                     |
|               .                                                                                    |
|                .                                   .                                               |
|                 ..                               .. ..                                             |
|                   .                             .     .                                            |
|                    .                           .       .                                           |
|                     .                         .         .                                          |
|                      ..                       .         .                                          |
|                        .                     .           .                                         |
|                         .                     .         .                                          |
|                          ..                   .         .                                          |
|                            .                   .       .                                           |
|                             .                   .     .                                            |
|                              .                   .. ..                                             |
|                               ..                   .                                               |
|                                 .                                                                  |
|                                  .                                                                 |
|                                   .                                                         .......|
|                                    ..                                         ..............       |
|                                      .                          ..............                     |
|                                       .           ..............                                   |
|                                     ..............                                                 |
|                       ..............    ..                                                         |
|         ..............                    .                                                        |
|  .......                                   .                                                       |
|                                             .                                                      |
|                                              ..                                                    |
|                                                .                                                   |
|                                                 .                                                  |
+----------------------------------------------------------------------------------------------------+
```

You can also use the `Display()` provided in this package to generate a grascale `.pgm` image. You need to save the output produced on execution to a `.pgm` file. For example,

```bash
python main.py > img.pgm
```
