## What?

Archimedean spiral generator for embroidered coils.

<img src="http://mi-lab.org/wp-content/uploads/2020/06/embroidered_spiral_small.jpg" width="800" height="266">

## How?

### Prerequisites

Clone or download [this repo](https://github.com/mitmedialab/spiral).

You need svgpathtools to run this script. Install it via pip using this command:

    pip install svgpathtools


### Usage

    spiral_generator.py [-h] -o <float> -i <float> -t <int> [-r] [-smin <float>] [-smax <float>] [-s]


### Example:

Generate an SVG file:

    spiral_generator.py -t 78 -o 50 -i 11 -smin 2 -smax 4 -r -s


### Optional arguments:

    -h, --help  show help message
    -o          outer diameter <float>
    -i          inner diameter <float>
    -t          number of turns <int>
    -smin       min stitch length, default = 2 <float>
    -smax       max stitch length, default = 2 <float>
    -r          reverse path direction from outward to inward
    -s          save to svg


## Contact

thomas.preindl(at)fh-hagenberg.at


## More:
[mi-lab.org/sonoflex-embroidered-speakers](http://mi-lab.org/sonoflex-embroidered-speakers/)

