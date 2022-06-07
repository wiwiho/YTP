# Puzcopan

A puzzle solver.

## Usage

First, set `tempFilePath` as you want in Config.py.

Open Python shell and type:

```
from Puzcopan import *
```

then you can use the following functions:

- `image(path)`: Read an image. The image with piece borders is saved 
    at `$tempFilePath/image`, and pieces in this image is saved at `$tempFilePath/piece`. 
    The four edges of a piece is colored in four colors: blue, green, red and purple, ordered by their indices.
- `component(pieceId)`: Show the connected component in which the given piece is located. 
    Numbers in blue circles is the indices of the pieces in the same component.
    Numbers in red circles means the indecies of slots.
- `solve(slotId)`: Specify a slot to solve.
- `next()`: Show the next recommended solution to the slot which is specified by you.
- `now()`: Show the previous shown solution.
- `last()`: Opposite of `next()`.
- `ok()`: Confirm the recommended solution which is shown previously.
    After that, the recommended piece is put in the slot, and the result will be shown.
    If you are not satisfied with a lot of recommended solutions, 
    you can use `ok(slotId, pieceId, edgeId)` to specify a piece and direction by yourself.
    The `edgeId` means the index of the edge at the upside.
