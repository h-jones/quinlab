"""Optical Absorption

This module is a Python environment script for optical power
measurements. It collects the data and then combines the data into a
single file with analysis completed.

Developed by Hayden Jones for usage with the optical calibration
experiment in QuIN Lab.

"""

__authors__ = "Hayden Jones"
__copyright__ = "Copyright 2016, QuIN Lab"
__credits__ = ["Hayden Jones", "Mats Powlowski"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Hayden Jones"
__email__ = "h4jones@uwaterloo.ca"
__status__ = "Production"

import csv
import newport_1830c as newportlib
import numpy as np
import scipy.constants as sciconst
import time


def measurement(name, side):
    """Measure and save optical power data over a small time period.

    Records 20 measurements and saves them to a csv file titled
    "`name`_input_side.csv" or "`name`_output_side.csv" depending on the
    `side` of the optical device which was being tested.

    Parameters
    ----------
    name : str
        The name of the device which is being tested. This name is used
        to sort the data files, and must be kept the same in order to
        properly combine the input and output optical power data.
    side : str
        The side of the device which is being tested.
        "input" for the input side, "output" for the output side.

    """
    power_meter = newportlib.Newport_1830C(4)
    if side == "input":
        filename = name + "_input_side.csv"
        values = [name + " input readings"]
    else:
        filename = name + "_output_side.csv"
        values = [name + " output readings"]
    for i in range(0, 20, 1):
        time.sleep(0.01)
        values.append(float(power_meter.get_power()))
    values.append("")  # Empty space, for backwards compatibility
    values.append(sum(values[1:-1]) / len(values[1:-1]))  # Mean
    values.append("")  # Empty space, for backwards compatibility
    with open(filename, "w", newline='') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(values)


def combine(name):
    """Combines and analyses the results from the input and output test.

    Combines the results from both the input and output side csv files,
    then outputs a new file titled "`name`_%Y_%m_%d_%H-%M-%S", where
    %Y is year, %m is month, %d is day, %H is hour, %M is minute, %S is
    second, and this time corresponds to the time when the combine
    function was called.

    In this output file, the raw data is saved in the first 5 rows, then
    after a blank row, a table of the analysed data is saved.

    Parameters
    ----------
    name : str
        The name of the device which is being tested. This name must be
        the same as the input and output files which correspond to the
        device which is being tested, in order to properly combine and
        analyse the data which is recorded.

    """
    infile = name + "_input_side.csv"
    outfile = name + "_output_side.csv"
    combined_file = name + time.strftime("_%Y_%m_%d_%H-%M-%S") + ".csv"
    with open(infile, 'r') as f:
        reader = csv.reader(f)
        in_vals = list(reader)[0]
    with open(outfile, 'r') as f:
        reader = csv.reader(f)
        out_vals = list(reader)[0]
    abs_delta_vals = [name + " absolute delta values"]
    rel_delta_vals = [name + " relative delta values"]
    photon_loss_vals = [name + " photon loss"]
    for i in range(1, 21, 1):
        abs_delta = float(in_vals[i]) - float(out_vals[i])
        abs_delta_vals.append(abs_delta)
        rel_delta = (abs_delta / float(in_vals[i])) * 100
        rel_delta_vals.append(rel_delta)
        photon_loss = (abs_delta * 780 * 10**(-9)) / (sciconst.c * sciconst.h)
        photon_loss_vals.append(photon_loss)
    output_table = [["Device:", name],
                    ["Average Input Power (W):", in_vals[-2]],
                    ["Average Output Power (W):", out_vals[-2]],
                    ["Average Power Delta (W):", np.mean(abs_delta_vals[1:]),
                     "Standard Deviation (W):", np.std(abs_delta_vals[1:])],
                    ["Average Photon Loss (photons/s):", np.mean(photon_loss_vals[1:]),
                     "Standard Deviation (photons/s):", np.std(photon_loss_vals[1:])],
                    ["Average Power/Photon Loss (%):", np.mean(rel_delta_vals[1:]),
                     "Standard Deviation (%):", np.std(rel_delta_vals[1:])]]
    output_table.append(["SNR:", output_table[-1][1] / output_table[-1][-1]])
    with open(combined_file, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(in_vals)
        writer.writerow(out_vals)
        writer.writerow(abs_delta_vals)
        writer.writerow(rel_delta_vals)
        writer.writerow(photon_loss_vals)
        writer.writerow([])
        writer.writerows(output_table)


def zero_meter():
    """Zeroes the optical power meter."""
    power_meter = newportlib.Newport_1830c()
    try:
        power_meter.zero_on()
    except Exception:
        pass
