import math, argparse, sys
from svgpathtools import Line, Path, wsvg

"""

Archimedean spiral generator for embroidered speaker coils.
You need svgpathtools to run this script. Install it via pip using this command:
pip install svgpathtools

Usage:
./spiral_generator.py [-h] -o <float> -i <float> -t <int> [-r] [-smin <float>] [-smax <float>] [-s]

Example:
./spiral_generator.py -t 78 -o 50 -i 11 -smin 2 -smax 4 -r -s


Optional arguments:
  -h, --help  show help message
  -o          outer diameter <float>
  -i          inner diameter <float>
  -t          number of turns <int>
  -smin       min stitch length, default = 2 <float>
  -smax       max stitch length, default = 2 <float>
  -r          reverse path direction from outward to inward
  -s          save to svg

Improvement suggestions:
thomas.preindl(at)fh-hagenberg.at

More:
http://mi-lab.org/sonoflex-embroidered-speakers/

"""

def spiral(OD, ID, turns, stitch_min, stitch_max, reverse = False):
  radius = OD/2 # spiral radius
  dist = ID/2 # current distance from center
  spacing = (radius - dist) / turns # radius increase per full revolution
  print("outer diameter:\t", OD, "mm")
  print("inner diameter:\t", ID, "mm")
  print("turns:\t\t", turns)
  print("turn spacing:\t", round(spacing,4), "mm")
  print("min stitch length:\t", stitch_min, "mm")
  print("max stitch length:\t", stitch_max, "mm")
  theta = 0 # current spiral angle theta

  if stitch_min > ID:
    raise ValueError('Minimal stitch length is bigger than inner diameter.')

  stitchlength = stitch_min

  coords=[]

  r = 0
  while r < radius:
    cord=[]
    cord.append(dist*math.cos(theta))
    cord.append(dist*math.sin(theta))
    coords.append(cord)
    r = math.hypot(*cord)

    # map stitch length
    if stitch_min != stitch_max:
      stitchlength = mapval(r*2, ID, OD, stitch_min, stitch_max)

    # approximate increment angle alpha for wanted segment length s with circle equation
    alpha = 2 * math.asin(stitchlength/(2*r))

    theta += alpha
    dist += spacing * ( alpha / (2*math.pi) )

  # pack points into continuous path
  p = Path(*[Line(complex(*coords[i-1]),complex(*coords[i])) for i in range(1, len(coords))])

  if reverse:
    p = p.reversed()

  # clackson scroll formula for estimating yarn length
  # print("estimated path length: ", round(math.pi * spacing * turns * turns), "mm")
  print("path length:\t", round(p.length()), "mm")
  print("points:\t\t", len(coords))

  return p

def mapval(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main(argv):
  parser = argparse.ArgumentParser(description='Tool for generating stitching paths for embroidered coils.')
  parser.add_argument('-o', help='outer diameter <float>', type=float, required=True, dest="od")
  parser.add_argument('-i', help='inner diameter <float>', type=float, required=True, dest="id")
  parser.add_argument('-t', help='number of turns <int>', type=int, required=True, dest="turns")
  parser.add_argument('-r', help='reverse path direction from outward to inward', action="store_true", dest="reverse")
  parser.add_argument('-a', help='adapt stitch length', action="store_true", dest="adaptive")
  parser.add_argument('-smin', help='minimal stitch length <float>, default = %(default)s', type=float, default=2, dest="smin")
  parser.add_argument('-smax', help='maximal stitch length <float>, default = %(default)s', type=float, default=2, dest="smax")
  parser.add_argument('-s', help='save to svg', action="store_true", dest="save")
  args = parser.parse_args()

  print("generating path ...")
  s = spiral(args.od, args.id, args.turns, args.smin, args.smax, args.reverse)

  if args.save:
    print("saving path ...")
    name = "coil_{}t_{}od_{}id_{}smin_{}smax".format(args.turns, round(args.od), round(args.id), round(args.smin*10), round(args.smax*10))
    if args.reverse:
      name += "_r"
    name += ".svg"
    d = "{}mm".format(args.od*1.2)
    wsvg(s, dimensions=(d,d), margin_size=0.1, filename=name)
    print(name)

if __name__ == "__main__":
  main(sys.argv[1:])

