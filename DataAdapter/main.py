import sys
import DataAdapter.converter
import math
import DataAdapter.utils
import DataAdapter.schemes.cli_params as cli_params
import numpy
from stl import mesh
from colored import fore, style
import time

TEMP_PATH = "models/temp/fixed_model.stl"

def parseFlags(argv):
    args = cli_params.parser.parse_args()
    config = vars(args)
    return config

def printClientParams(config):
    for k in config:
        print("--- " + k + ": " + getColoredText(fore.YELLOW, str(config[k])))
    print()

def getColoredText(color, text):
    return color + str(text) + style.RESET

# TODO: add axis correction in future
def correctModelPositionAngleByAxis(model):
    model.rotate([0.5, 0, 0], math.radians(0))
    model.rotate([0, 0.5, 0], math.radians(0))
    model.rotate([0, 0, 0.5], math.radians(0))

def correctModelPositionCoords(model):
    minx1, maxx1, miny1, maxy1, minz1, maxz1 = DataAdapter.utils.find_mins_maxs(model)
    model.translate(numpy.array([0-minx1, 0-miny1, 0-minz1]))

def main(argv):
    print("====== Running Data Adapter ======")
    timeStart = time.time()

    print("- Client params: parsed and validated, status: " + getColoredText(fore.GREEN, "OK"))
    config = parseFlags(argv)
    print("-- Client Params are:")
    printClientParams(config)

    # DataAdapter.utils.recreateDir("models/output/")
    # DataAdapter.utils.recreateDir("models/temp/")

    src_model = mesh.Mesh.from_file(config["src"])

    print("\n- Model '" + getColoredText(fore.YELLOW, config["src"]) +
        "' loaded. ", "Status: " + getColoredText(fore.GREEN, "OK"))
    print("-- Model STL type: " + getColoredText(fore.YELLOW,
        DataAdapter.utils.checkFileType(src_model)))

    if DataAdapter.utils.checkFileType(src_model) == "Binary":
        print('--- Converting binary STL model to ASCII STL model')
        DataAdapter.converter.convert_from_binary_to_stl(
            config["src"], "models/temp/converted_to_ascii_model.stl")
        src_model = mesh.Mesh.from_file("models/temp/converted_to_ascii_model.stl")
        print('-- Binary STL converted to ASCII STL, status: ', getColoredText(fore.GREEN, "OK"))

    correctModelPositionAngleByAxis(src_model)
    correctModelPositionCoords(src_model)
    print("- Model axis position corrected, status: ",
        getColoredText(fore.GREEN, "OK"))
    src_model.save(TEMP_PATH)
    print("- New model saved as: '" + getColoredText(fore.YELLOW, TEMP_PATH) + "', status: " + getColoredText(fore.GREEN, "OK"))

    config["src"] = TEMP_PATH

    print("- Config source path changed to: '" + getColoredText(fore.YELLOW,
                                                    TEMP_PATH) + "', status: " + getColoredText(fore.GREEN, "OK"))

    print("\nElapsed Time: " + getColoredText(fore.YELLOW,
        time.time() - timeStart) + "s")
    print("====== Data Adapter finished working ======")

    return config

if __name__ == "__main__":
    main(sys.argv[1:])
