import argparse

parser = argparse.ArgumentParser(description="CLI params for dental support system generator",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--size_of_top_gate",
                    action="store", type=int, help="Size of top gate in mm", default=30)
parser.add_argument("--size_of_mid_gate",
                    action="store", type=int, help="Size of middle gate in mm", default=50)
parser.add_argument("--size_of_low_gate",
                    action="store", type=int, help="Size of lower gate in mm", default=40)
parser.add_argument("-v", "--verbose",
                    action="store", help="increase verbosity")
parser.add_argument("--u_dist", action="store_true",
                    help="Even distribution of gates", default=True)
parser.add_argument("--volume_check", action="store_true",
                    help="Whether volume check is needed", default=True)
parser.add_argument("--curve_check", action="store_true",
                    help="Whether curve check is needed", default=True)
parser.add_argument("--top_dist", action="store", type=int,
                    help="Height of the top gate")
parser.add_argument("--mid_dist", action="store", type=int,
                    help="Height of the middle gate")
parser.add_argument("--low_dist", action="store", type=int,
                    help="Height of the lower gate")
parser.add_argument("--tamount", action="store", type=int,
                    help="Amount of teeths", default=3)
parser.add_argument("-src", action="store", type=str, help="Source location", default="models/curved_teeth.stl")
parser.add_argument("-dest", action="store", type=str, help="Destination location", default="models/output/test.stl")
