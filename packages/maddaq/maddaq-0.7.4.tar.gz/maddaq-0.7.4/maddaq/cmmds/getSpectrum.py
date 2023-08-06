#!/usr/bin/env python3
"""Open data file and get spectrum."""
import os
import sys
from argparse import Action
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import numpy as np
from maddaq.cmmds.fit_utils import draw_best_fit, fit_gaussian, fit_two_peaks
from maddaq import MadDAQData
from maddaq import ShowProgress


def draw_hist_and_projection(axh, axp, data, title=None, axis_title=None, x_label=None, y_label=None):
    """Plots a bar histogram and the Y projection.

    Args:
    ----
        axh: axis for the histogram
        axp: axis for the projection
        data: The monitor data
        title: the histogram title
        axis_title: title for the histogram axis
        x_label: label for the histgram X axis
        y_label: label for the Y axis

    Returns
    -------
        mean. std: a tuple with the Y maverage and std

    """
    # Draw the histogram
    y = data
    x = np.linspace(0, len(data)+1, len(data))

    axh.step(x, y)
    if axis_title:
        axh.set_title(axis_title)

    if x_label:
        axh.set_xlabel(x_label)

    if y_label:
        axh.set_ylabel(y_label)

    mean = np.mean(y)
    std = np.std(y)

    # Now the projection
    axp.hist(y, orientation="horizontal")

    return mean, std


def show_pedestals(md):
    """Show module pedestals.

    Args:
    ----
        md: Module object.

    """
    # Get the data and plot
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(ncols=2, nrows=2, width_ratios=(2, 1))

    # pedestals
    ax = fig.add_subplot(gs[0, 0])
    mped, stped = draw_hist_and_projection(
        ax, fig.add_subplot(gs[0, 1], sharey=ax),
        md.pedestal,
        axis_title="Pedestals",
        x_label="Channel"
    )
    print("Pedestal mean {:.1f} std {:.1f}".format(mped, stped))

    # noise
    ax = fig.add_subplot(gs[1, 0])
    mnoise, stnoise = draw_hist_and_projection(
        ax, fig.add_subplot(gs[1, 1], sharey=ax),
        md.noise,
        axis_title="Noise",
        x_label="Channel"
    )
    print("Noise mean {:.1f} std {:.1f}".format(mnoise, stnoise))


def do_getSpectrum(fnam, options):
    """Main entry."""
    # Check that the file exists
    if not os.path.exists(fnam):
        print("Input file", fnam, "does not exist")
        return

    # We open here the file with MadDAQData
    maddaq = MadDAQData(fnam)
    maddaq.show_info(True)

    # Find the module
    keys = list(maddaq.modules.keys())
    if options.mid in keys:
        mid = options.mid
    else:
        mid = keys[0]

    print("\n## Looking at data from module {}.".format(mid))
    md = maddaq.modules[mid]

    # Show pedeswtals and noise
    show_pedestals(md)

    # Create the iterator
    if options.scan_point is not None:
        maddaq_iter = maddaq.create_iterator_at_scanpoint(options.scan_point, [mid])
    elif options.start_time is not None:
        maddaq_iter = maddaq.create_iterator_at_time(options.start_time, [mid])
    elif options.start_evt is not None:
        maddaq_iter = maddaq.create_iterator_at_event(options.start_evt, [mid])
    else:
        maddaq_iter = maddaq.create_module_iterator(md)

    amplitude = []
    prg = ShowProgress(maddaq.nevts, width=24)
    prg.start()

    for evt in maddaq_iter:
        data = md.process_event(evt)
        if data is not None:
            for C, E in data:
                if E > options.thrs:
                    amplitude.append(E)

        prg.increase(show=True)

    prg.stop()
    print("")
    # Draw the signal
    fig, ax = plt.subplots(1, 1)
    n, bins, *_ = ax.hist(amplitude, bins=options.nbin)
    mean = np.mean(amplitude)
    std = np.std(amplitude)
    if options.fit:
        if options.two_peaks:
            result, out, legend = fit_two_peaks(mean, std, std, n, bins)

        else:
            result, out, legend = fit_gaussian(n, bins, mean, width=std)

        draw_best_fit(ax, result, bins)
        ax.legend([legend], loc=1)

    ax.set_title("Signel Channel signal")
    ax.set_xlabel("Charge (ADC)")
    if options.logY:
        ax.set_yscale("log")

    plt.show()


class CommaSeparatedListAction(Action):
    """Create a list from the comma sepparated numbers at imput."""

    def __call__(self, parser, namespace, values, option_string=None):
        """The actual action."""
        setattr(namespace, self.dest, list(map(int, values.split(','))))


def getSpectrum():
    """Main entry."""

    parser = ArgumentParser()
    parser.add_argument('files', nargs='+', help="Input files")
    parser.add_argument("--start-time", dest="start_time", default=None, type=float,
                        help="Event time to start")
    parser.add_argument("--start-evt", dest="start_evt", default=None,
                        action=CommaSeparatedListAction,
                        help="Event number to start showing")
    parser.add_argument("--scan-point", dest="scan_point", type=int, default=None,
                        help="Scan point number to visit")
    parser.add_argument("--nbin", default=50, help="Number of bins in histogram.")
    parser.add_argument("--logY", default=False, action="store_true", help="Log axis")
    parser.add_argument("--thrs", default=0.0, type=float, help="Min E to show in histogram")
    parser.add_argument("--two_peaks", default=False, action="store_true", help="Min E to show in histogram")
    parser.add_argument("--no-fit", dest="fit", default=True, action="store_false")
    parser.add_argument("--mid", dest="mid", default=-1,
                        type=int, help="The module ID")

    options = parser.parse_args()

    if len(options.files) == 0:
        print("I need an input file")
        sys.exit()

    do_getSpectrum(options.files[0], options)


if __name__ == "__main__":
    getSpectrum()
