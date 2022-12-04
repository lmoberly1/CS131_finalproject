## Beatboard

1. Applies adaptive thresholding to locate a grid of squares (each grid square corresponds to a musical intonation (vertical) and a beat in a standard 4-beat measure (horizontal))
2. Applies 4-point transformation to obtain top-down unskewed view of image.
3. Uses contour detection to isolate each individual square in grid.
4. Applies thresholding to determine if there is shape in square.
5. If there is a shape in a square, approximates the polynomial (number of edges)

## Trombone [Old]

Uses hand detection to calculate distance between hands.
Similar to a trombone, will play notes depending on this distance.
Keep hands open to play, close into a fist to cut off sound.
