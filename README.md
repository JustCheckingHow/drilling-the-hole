# drilling-the-hole
Solution for Bosch's "WE MOVE. YOU WIN" contest on HackYeah 2019.

### Setup
Camera feed is uglily read from the screen. You need a live stream opened in another window, for example a web camera interface or a config program.
Edit the `zero.py` and `angle.py` (lines 39, 40) with new stream coordinates. (We've decided on this way, because the camera
we had access to was difficult to work with via python).

Now you should be able to run `color_picker.py`. Use it to select the color of the tracker - click on the tracker in the screen with distorted colors.
It will save the color of the tracker into config.

The only thing left is to calibrate the algorithm to prevent interference from inertia and camera delay.
You will have to adjust variables `clockwise_inertia` and `ctr_clockwise_inertia` in the file `solver.py`, lines 27 and 28.
In our test environment the values ranged from 0.1 and 0.4.

### Usage
`python zero.py` will set the engine in 'zero' position. \
`python angle.py <angle>` will rotate the engine by `<angle>` degrees counterclockwise.
