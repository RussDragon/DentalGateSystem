import sys
import numpy
import stl
from stl import mesh
from bezier import bezier
from DataProcessor.Util import utils
from colored import fore, style
import matplotlib.pyplot as plt
import time
import seaborn
seaborn.set()

def getColoredText(color, text):
    return color + str(text) + style.RESET

def simple_generation_mode(config):
    print("====== Running Data Processor ======")
    timeStart = time.time()

    src_model = mesh.Mesh.from_file(config["src"])
    print("- Model '" + getColoredText(fore.YELLOW, config["src"]) +
        "' loaded. " + "Status: " + getColoredText(fore.GREEN, "OK"))

    minsrcx, maxsrcx, minsrcy, maxsrcy, minsrcz, maxsrcz = utils.find_mins_maxs(
        src_model)
    srcw, srcl, srch = utils.fiind_side_sizes(src_model)

    pipe_models = []
    for i in range(config["tamount"]):
        loaded_model = mesh.Mesh.from_file("models/pipe.stl")

        utils.translateToZero(loaded_model)

        pipe_models.append(loaded_model)
        print("- Upper gate model " + str(i+1) + " loaded." + " Status: " + getColoredText(fore.GREEN, "OK"))

    pipew, pipel, pipeh = utils.fiind_side_sizes(pipe_models[0]) # pipe dimensions


    print('\n- Connecting upper gates, status: ' + getColoredText(fore.YELLOW, "working..."))
    # Connect upper gates to model
    for i in range(len(pipe_models)):
        minpipex, maxpipex, minpipey, maxpipey, minpipez, maxpipez = utils.find_mins_maxs(pipe_models[i])
        teeth_lenght = srcw / config["tamount"]

        # some magic coefficients for correcting upper gates
        # only for simple model
        x_calculated = minsrcx - minpipex + (teeth_lenght * i + pipew/2)
        y_calculated = minsrcy - maxpipey + 0.2 * srcl
        z_calculated = maxsrcz - maxpipez - 0.3 * srch

        pipe_models[i].translate(numpy.array([x_calculated, y_calculated, z_calculated]))
        print("-- Upper gate " + str(i+1) + " connected. Status: " + getColoredText(fore.GREEN, "OK"))
    print("- Upper gates connected, status: " + getColoredText(fore.GREEN, "OK"))

    middle_pipe_model = mesh.Mesh.from_file("models/middle_pipe.stl") # should be generated automatically
    print("\n- Middle Pipe Model loaded. " + "Status: " + getColoredText(fore.GREEN, "OK"))

    utils.translateToZero(middle_pipe_model)
    minmx, maxmx, minmy, maxmy, minmz, maxmz = utils.find_mins_maxs(
        middle_pipe_model)

    print('\n- Connecting middle gate, status: ' +
            getColoredText(fore.YELLOW, "working..."))
    x_calculated = minsrcx - minmx
    y_calculated = minmy - pipel
    z_calculated = maxsrcz - maxpipez - 0.3 * srch

    middle_pipe_model.translate(numpy.array([x_calculated, y_calculated, z_calculated]))
    minmx, maxmx, minmy, maxmy, minmz, maxmz = utils.find_mins_maxs(
        middle_pipe_model)
    print("- Middle gate connected, status: " +
            getColoredText(fore.GREEN, "OK") + "\n")

    base_pipes = []
    for i in range(2):
        loaded_model = mesh.Mesh.from_file("models/pipe.stl")

        utils.translateToZero(loaded_model)

        base_pipes.append(loaded_model)
        print("- Base pipe Model " + str(i+1) + " loaded." +
                " Status: " + getColoredText(fore.GREEN, "OK"))

    print('\n- Connecting base gates, status: ' +
            getColoredText(fore.YELLOW, "working..."))
    for i in range(len(base_pipes)):
        minpipex, maxpipex, minpipey, maxpipey, minpipez, maxpipez = utils.find_mins_maxs(
            base_pipes[i])

        # some magic coefficients for correcting upper gates
        # only for simple model

        x_calculated = minmx - minpipex + (((maxmx - minmx) / 3) * (i + 1)) - pipew / 2
        y_calculated = minmy - maxpipey + 0.2 * srcl
        z_calculated = maxsrcz - maxpipez - 0.3 * srch

        base_pipes[i].translate(numpy.array(
            [x_calculated, y_calculated, z_calculated]))
        print("-- Base gate " + str(i+1) + " connected. Status: " +
                getColoredText(fore.GREEN, "OK"))
    print("- Base gates connected, status: " +
            getColoredText(fore.GREEN, "OK"))

    combined = mesh.Mesh(numpy.concatenate(
        [src_model.data, middle_pipe_model.data]))
    combined.save('models/output/first-stage-combined.stl', mode=stl.Mode.ASCII)  # save as ASCII
    for model in pipe_models:
        combined = mesh.Mesh(numpy.concatenate([combined.data, model.data]))
    combined.save('models/output/second-stage-combined.stl', mode=stl.Mode.ASCII)  # save as ASCII
    for model in base_pipes:
        combined = mesh.Mesh(numpy.concatenate([combined.data, model.data]))

    print("\nSaving combined model as 'models/output/combined.stl', status: " + getColoredText(fore.GREEN, "OK"))
    combined.save('models/output/combined.stl', mode=stl.Mode.ASCII)  # save as ASCII

    print("\nElapsed Time: " + getColoredText(fore.YELLOW,
        time.time() - timeStart) + "s")
    print("====== Data Processor finished working ======")

def complex_generation_mode(config):
    print("====== Running Data Processor ======")
    timeStart = time.time()

    src_model = mesh.Mesh.from_file(config["src"])
    print("- Model '" + getColoredText(fore.YELLOW, config["src"]) +
        "' loaded. " + "Status: " + getColoredText(fore.GREEN, "OK"))

    minsrcx, maxsrcx, minsrcy, maxsrcy, minsrcz, maxsrcz = utils.find_mins_maxs(
        src_model)
    srcw, srcl, srch = utils.fiind_side_sizes(src_model)

    x0, y0 = minsrcx, maxsrcz - (srch / 2)
    x2, y2 = maxsrcx, maxsrcz - (srch / 2)
    # x0, y0 = minsrcx, minsrcz - (srch / 2) * 0
    # x2, y2 = maxsrcx, minsrcz - (srch / 2) * 0
    cx, cy = maxsrcx - srcw/2, maxsrcz

    x1 = 2 * cx - x0 / 2 - x2 / 2
    y1 = 2 * cy - y0 / 2 - y2 / 2
    print(x1, y1)

    nodes1 = numpy.asfortranarray([
        [x0, x1, x2],
        [y0, y1, y2],
    ])
    curve1 = bezier.Curve.from_nodes(nodes1)

    ax = curve1.plot(num_pts=256)
    _ = ax.axis("scaled")
    _ = ax.set_xlim(minsrcx-10, maxsrcx+10)
    _ = ax.set_ylim(minsrcz-10, maxsrcz+10)
    _ = ax.plot([x0], [y0], marker="o", markersize=10,
                markeredgecolor="red", markerfacecolor="green")
    _ = ax.plot([cx], [cy], marker="o", markersize=10,
                markeredgecolor="red", markerfacecolor="green")
    _ = ax.plot([x2], [y2], marker="o", markersize=10,
                markeredgecolor="red", markerfacecolor="green")
    plt.show()
    # plt.savefig('demo.png', transparent=True)





def main(argv):
    pass

if __name__ == "__main__":
    main(sys.argv[1:])
