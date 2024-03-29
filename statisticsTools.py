import json
import os
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from rvms import idfStudent

INFINITE = 99999999999999

batchMeanTemplate = {
    "interarrival": 0,
    "servers": 0,
    "seed": 0,
    "GLOBAL AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "GLOBAL AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "GLOBAL AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE1 AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE1 AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE1 AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE2 AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE2 AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE2 AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE3 AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE3 AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE3 AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE4 AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE4 AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE4 AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE5 AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE5 AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE5 AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE6 AVG WAIT": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE6 AVG DELAY": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "QUEUE6 AVG NUMBER": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "UTILIZATION1": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "UTILIZATION2": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "UTILIZATION3": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "UTILIZATION4": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "UTILIZATION5": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "UTILIZATION6": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "MEAN CONDITIONAL SLOWDOWN (1.24)": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "MEAN CONDITIONAL SLOWDOWN (2.65)": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "MEAN CONDITIONAL SLOWDOWN (4.42)": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},
    "MEAN CONDITIONAL SLOWDOWN (8.26)": {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95},

}

transientTemplate = {
    "interarrival": 0,
    "servers": 0,
    "seed": 0,
    "GLOBAL AVG WAIT": [],
    "GLOBAL AVG DELAY": [],
    "GLOBAL AVG NUMBER": [],
    "QUEUE1 AVG WAIT": [],
    "QUEUE1 AVG DELAY": [],
    "QUEUE1 AVG NUMBER": [],
    "QUEUE2 AVG WAIT": [],
    "QUEUE2 AVG DELAY": [],
    "QUEUE2 AVG NUMBER": [],
    "QUEUE3 AVG WAIT": [],
    "QUEUE3 AVG DELAY": [],
    "QUEUE3 AVG NUMBER": [],
    "QUEUE4 AVG WAIT": [],
    "QUEUE4 AVG DELAY": [],
    "QUEUE4 AVG NUMBER": [],
    "QUEUE5 AVG WAIT": [],
    "QUEUE5 AVG DELAY": [],
    "QUEUE5 AVG NUMBER": [],
    "QUEUE6 AVG WAIT": [],
    "QUEUE6 AVG DELAY": [],
    "QUEUE6 AVG NUMBER": [],
    "UTILIZATION1": [],
    "UTILIZATION2": [],
    "UTILIZATION3": [],
    "UTILIZATION4": [],
    "UTILIZATION5": [],
    "UTILIZATION6": [],
    "JOBS": [],
}


def initialize_transient_organizer(organizer, job_number, transientList):
    for t in organizer.keys():
        for i in range(0, job_number):
            if t not in ['global', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'q1', 'q2', 'q3', 'mean_conditional_slowdown']:
                organizer[t].append([])
            else:
                for t2 in organizer[t].keys():
                    organizer[t][t2].append([])

    for transientStats in transientList:
        for t in transientStats.keys():
            if t in ['seed', 'arrival_stream', 'service_stream', 'observation_period', 'interarrivals', 'k',
                     'batch_size', 'servers', 'acquisition_time', 'index']:
                continue

            if t not in ['global', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'q1', 'q2', 'q3', 'mean_conditional_slowdown']:
                for i in range(0, len(transientStats[t])):
                    try:
                        organizer[t][i].append(transientStats[t][i])
                    except:
                        continue
            else:
                for t2 in organizer[t].keys():
                    for i in range(0, len(transientStats[t][t2])):
                        try:
                            organizer[t][t2][i].append(transientStats[t][t2][i])
                        except:
                            continue

    return organizer


def analyticalResults(interarrivals, model):
    if model == 1:
        # MG1_ABS_NETWORK
        LAMBDA = 1 / interarrivals

        utilization = (LAMBDA / 3) * 4.42

        delay = ((LAMBDA / 6) * 32.2791123) / (1 - utilization)

        wait = delay + 4.42

        numberqueue = delay * (LAMBDA / 3)

        number = (numberqueue + utilization) * 3

        return delay, wait, numberqueue, number, utilization
    else:
        LAMBDA = 1 / interarrivals

        p = [0.199991414, 0.4436064477, 0.3564021383]

        utilization = (LAMBDA) * 4.42

        delay = [((LAMBDA / 2) * 32.2791123) / (1 - LAMBDA * 0.245721),
                 ((LAMBDA / 2) * 32.2791123) / ((1 - LAMBDA * 0.245721) * (1 - LAMBDA * 1.42502)),
                 ((LAMBDA / 2) * 32.2791123) / ((1 - LAMBDA * 4.434939) * (1 - LAMBDA * 1.42502))]

        service = [(0.520762 / p[0]) * (0.47185), (0.520762 / p[1]) * (2.26456), (0.520762 / p[2]) * (5.77984)]

        wait = [delay[0] + service[0], delay[1] + service[1], delay[2] + service[2]]

        number = [delay[0] * (LAMBDA * p[0]), delay[1] * (LAMBDA * p[1]), delay[2] * (LAMBDA * p[2])]

        globalwait = p[0] * wait[0] + p[1] * wait[1] + p[2] * wait[2]
        globaldelay = p[0] * delay[0] + p[1] * delay[1] + p[2] * delay[2]
        globalnumber = number[0] + number[1] + number[2] + utilization

        return globalwait, globaldelay, globalnumber, delay, wait, number, utilization


def estimate(valuesArray):
    if len(valuesArray) == 0:
        mean = 0.0
        stdev = 0.0
        w = 0.0
        return mean, stdev, w

    LOC = 0.95  # level of confidence, use 0.95 for 95% confidence
    n = 0  # counts data points
    sum = 0.0
    mean = 0.0

    data = valuesArray[n]

    for i in range(1, len(valuesArray)):  # use Welford's one-pass method
        n += 1  # to calculate the sample mean
        diff = float(data) - mean  # and standard deviation
        sum += diff * diff * (n - 1.0) / n
        mean += diff / n
        data = valuesArray[i]

    stdev = sqrt(sum / n)

    if n > 1:
        u = 1.0 - 0.5 * (1.0 - LOC)  # interval parameter
        t = idfStudent(n - 1, u)  # critical value of t
        w = t * stdev / sqrt(n - 1)  # interval half width

        return mean, stdev, w
    else:
        print("ERROR - insufficient data\n")


def batchMeans(path, batchDictionary, model):
    # -----------------------------------------------------------
    # This technique is used to compute Steady-State statistics 
    # ( "infinite horizon" point and interval estimations ).
    # -----------------------------------------------------------
    global batchMeanTemplate

    SERVERS = int(batchDictionary["servers"])

    B = batchDictionary["batch_size"]

    batchMeanTemplate["interarrival"] = batchDictionary["interarrivals"]
    batchMeanTemplate["seed"] = batchDictionary["seed"]
    batchMeanTemplate["servers"] = batchDictionary["servers"]

    avg_wait_global = batchDictionary["global"]["avg_wait"][1:]
    avg_delay_global = batchDictionary["global"]["avg_delay"][1:]
    avg_number_global = batchDictionary["global"]["avg_number"][1:]

    avg_slowdown_1_24 = batchDictionary["mean_conditional_slowdown"]["(1.24)"][1:]
    avg_slowdown_2_65 = batchDictionary["mean_conditional_slowdown"]["(2.65)"][1:]
    avg_slowdown_4_42 = batchDictionary["mean_conditional_slowdown"]["(4.42)"][1:]
    avg_slowdown_8_26 = batchDictionary["mean_conditional_slowdown"]["(8.26)"][1:]

    avg_utilizations = []

    for j in range(SERVERS):
        avg_utilizations.append(batchDictionary["avg_utilization" + str(j + 1)][1:])

    if model == 0:
        # MSMQ_SB_NETWORK
        avg_wait_queues = [batchDictionary["q1"]["avg_wait"][1:], batchDictionary["q2"]["avg_wait"][1:],
                           batchDictionary["q3"]["avg_wait"][1:]]
        avg_delay_queues = [batchDictionary["q1"]["avg_delay"][1:], batchDictionary["q2"]["avg_delay"][1:],
                            batchDictionary["q3"]["avg_delay"][1:]]
        avg_number_queues = [batchDictionary["q1"]["avg_number"][1:], batchDictionary["q2"]["avg_number"][1:],
                             batchDictionary["q3"]["avg_number"][1:]]

    if model == 1:
        # MG1_ABS_NETWORK
        avg_wait_queues = []
        avg_delay_queues = []
        avg_number_queues = []

        if SERVERS >= 1:
            avg_wait_queues.append(batchDictionary["c1"]["avg_wait"][1:])
            avg_delay_queues.append(batchDictionary["c1"]["avg_delay"][1:])
            avg_number_queues.append(batchDictionary["c1"]["avg_number"][1:])

        if SERVERS >= 2:
            avg_wait_queues.append(batchDictionary["c2"]["avg_wait"][1:])
            avg_delay_queues.append(batchDictionary["c2"]["avg_delay"][1:])
            avg_number_queues.append(batchDictionary["c2"]["avg_number"][1:])

        if SERVERS >= 3:
            avg_wait_queues.append(batchDictionary["c3"]["avg_wait"][1:])
            avg_delay_queues.append(batchDictionary["c3"]["avg_delay"][1:])
            avg_number_queues.append(batchDictionary["c3"]["avg_number"][1:])

        if SERVERS >= 4:
            avg_wait_queues.append(batchDictionary["c4"]["avg_wait"][1:])
            avg_delay_queues.append(batchDictionary["c4"]["avg_delay"][1:])
            avg_number_queues.append(batchDictionary["c4"]["avg_number"][1:])

        if SERVERS >= 5:
            avg_wait_queues.append(batchDictionary["c5"]["avg_wait"][1:])
            avg_delay_queues.append(batchDictionary["c5"]["avg_delay"][1:])
            avg_number_queues.append(batchDictionary["c5"]["avg_number"][1:])

        if SERVERS >= 6:
            avg_wait_queues.append(batchDictionary["c6"]["avg_wait"][1:])
            avg_delay_queues.append(batchDictionary["c6"]["avg_delay"][1:])
            avg_number_queues.append(batchDictionary["c6"]["avg_number"][1:])

    with open(path + "/steadystate.json", "a") as results:

        res = batchMeanTemplate

        res["interarrival"] = batchDictionary["interarrivals"]
        res["seed"] = batchDictionary["seed"]
        res["servers"] = batchDictionary["servers"]

        mean, stdev, half_interval = estimate(avg_wait_global)
        res["GLOBAL AVG WAIT"]["mean"] = mean
        res["GLOBAL AVG WAIT"]["stdev"] = stdev
        res["GLOBAL AVG WAIT"]["half_confidence_interval"] = half_interval

        mean, stdev, half_interval = estimate(avg_delay_global)
        res["GLOBAL AVG DELAY"]["mean"] = mean
        res["GLOBAL AVG DELAY"]["stdev"] = stdev
        res["GLOBAL AVG DELAY"]["half_confidence_interval"] = half_interval

        mean, stdev, half_interval = estimate(avg_number_global)
        res["GLOBAL AVG NUMBER"]["mean"] = mean
        res["GLOBAL AVG NUMBER"]["stdev"] = stdev
        res["GLOBAL AVG NUMBER"]["half_confidence_interval"] = half_interval

        mean, stdev, half_interval = estimate(avg_slowdown_1_24)
        res["MEAN CONDITIONAL SLOWDOWN (1.24)"]["mean"] = mean
        res["MEAN CONDITIONAL SLOWDOWN (1.24)"]["stdev"] = stdev
        res["MEAN CONDITIONAL SLOWDOWN (1.24)"]["half_confidence_interval"] = half_interval

        mean, stdev, half_interval = estimate(avg_slowdown_2_65)
        res["MEAN CONDITIONAL SLOWDOWN (2.65)"]["mean"] = mean
        res["MEAN CONDITIONAL SLOWDOWN (2.65)"]["stdev"] = stdev
        res["MEAN CONDITIONAL SLOWDOWN (2.65)"]["half_confidence_interval"] = half_interval

        mean, stdev, half_interval = estimate(avg_slowdown_4_42)
        res["MEAN CONDITIONAL SLOWDOWN (4.42)"]["mean"] = mean
        res["MEAN CONDITIONAL SLOWDOWN (4.42)"]["stdev"] = stdev
        res["MEAN CONDITIONAL SLOWDOWN (4.42)"]["half_confidence_interval"] = half_interval

        mean, stdev, half_interval = estimate(avg_slowdown_8_26)
        res["MEAN CONDITIONAL SLOWDOWN (8.26)"]["mean"] = mean
        res["MEAN CONDITIONAL SLOWDOWN (8.26)"]["stdev"] = stdev
        res["MEAN CONDITIONAL SLOWDOWN (8.26)"]["half_confidence_interval"] = half_interval

        if model == 0:
            # MSMQ_SB_NETWORK
            for j in range(1, 4):
                mean, stdev, half_interval = estimate(avg_wait_queues[j - 1])
                res["QUEUE" + str(j) + " AVG WAIT"]["mean"] = mean
                res["QUEUE" + str(j) + " AVG WAIT"]["stdev"] = stdev
                res["QUEUE" + str(j) + " AVG WAIT"]["half_confidence_interval"] = half_interval

                mean, stdev, half_interval = estimate(avg_delay_queues[j - 1])
                res["QUEUE" + str(j) + " AVG DELAY"]["mean"] = mean
                res["QUEUE" + str(j) + " AVG DELAY"]["stdev"] = stdev
                res["QUEUE" + str(j) + " AVG DELAY"]["half_confidence_interval"] = half_interval

                mean, stdev, half_interval = estimate(avg_number_queues[j - 1])
                res["QUEUE" + str(j) + " AVG NUMBER"]["mean"] = mean
                res["QUEUE" + str(j) + " AVG NUMBER"]["stdev"] = stdev
                res["QUEUE" + str(j) + " AVG NUMBER"]["half_confidence_interval"] = half_interval

        if model == 1:
            # MG1_ABS_NETWORK
            for j in range(1, SERVERS + 1):
                mean, stdev, half_interval = estimate(avg_wait_queues[j - 1])
                res["QUEUE" + str(j) + " AVG WAIT"]["mean"] = mean
                res["QUEUE" + str(j) + " AVG WAIT"]["stdev"] = stdev
                res["QUEUE" + str(j) + " AVG WAIT"]["half_confidence_interval"] = half_interval

                mean, stdev, half_interval = estimate(avg_delay_queues[j - 1])
                res["QUEUE" + str(j) + " AVG DELAY"]["mean"] = mean
                res["QUEUE" + str(j) + " AVG DELAY"]["stdev"] = stdev
                res["QUEUE" + str(j) + " AVG DELAY"]["half_confidence_interval"] = half_interval

                mean, stdev, half_interval = estimate(avg_number_queues[j - 1])
                res["QUEUE" + str(j) + " AVG NUMBER"]["mean"] = mean
                res["QUEUE" + str(j) + " AVG NUMBER"]["stdev"] = stdev
                res["QUEUE" + str(j) + " AVG NUMBER"]["half_confidence_interval"] = half_interval

        for j in range(1, SERVERS + 1):
            mean, stdev, half_interval = estimate(avg_utilizations[j - 1])
            res["UTILIZATION" + str(j)]["mean"] = mean
            res["UTILIZATION" + str(j)]["stdev"] = stdev
            res["UTILIZATION" + str(j)]["half_confidence_interval"] = half_interval

        json.dump(res, results, indent=4)

    results.close()


def finiteHorizon(finiteHorizonDictionary):
    # -----------------------------------------------------------
    # This technique is used to compute Transient statistics
    # ( "finite horizon" point and interval estimations ).
    # -----------------------------------------------------------
    global transientTemplate

    transientTemplate["interarrival"] = finiteHorizonDictionary["interarrivals"]
    transientTemplate["seed"] = finiteHorizonDictionary["seed"]
    transientTemplate["servers"] = finiteHorizonDictionary["servers"]


def steadyStatePlotter(path, model, validation):
    # Generate plot for steady State
    global batchMeanTemplate

    directories = os.listdir(path)

    for t in batchMeanTemplate.keys():

        if t in ["interarrival", "servers", "seed"]:
            continue

        headerbuilder = 0

        if model == 0:
            # MSMQ_SB_NETWORK
            title = "Size Based MSMQ - " + t
        elif model == 1:
            # MG1_ABS_NETWORK
            title = "SSQ Abstract Network - " + t

        seeds, values, errors = [], [], []
        k, b, interarrival, servers = 0, 0, 0, 0

        for d in directories:
            files = os.listdir(path + "/" + d)

            for f in files:
                if f.startswith("batchMeans"):
                    filepath = path + "/" + d + "/" + f

                    with open(filepath) as jsonHeader:
                        data = json.load(jsonHeader)
                        seeds.append(data["seed"])
                        if headerbuilder == 0:
                            interarrival = data["interarrivals"]
                            servers = data["servers"]
                            b = data["batch_size"]
                            k = data["k"]
                            title += "\n" + str(servers) + " Servers -  Avg Interarrival time: " + str(
                                interarrival) + "min"
                            title += "\n Infinite Horizon Statistics ( Batch Means : b : " + str(b) + "  k : " + str(
                                k) + " )"
                            headerbuilder = 1

                elif f.startswith("steadystate"):
                    filepath = path + "/" + d + "/" + f

                    with open(filepath) as jsonfile:
                        data = json.load(jsonfile)
                        values.append(data[t]["mean"])
                        errors.append(data[t]["half_confidence_interval"])

        x = [i for i in range(len(values))]

        fig, axs = plt.subplots(2, 1)

        if validation == 1:
            if model == 1:
                # MG1_ABS_NETWORK
                delay, wait, numberqueue, number, utilization = analyticalResults(batchMeanTemplate["interarrival"],
                                                                                  model)
                if t.endswith("AVG WAIT"):
                    l = [wait for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(wait)

                elif t.endswith("AVG DELAY"):
                    l = [delay for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(delay)

                elif t.endswith("AVG NUMBER"):
                    if t.startswith("GLOBAL"):
                        l = [number for i in range(len(values))]
                        realvalue = "{0:6.2f}".format(number)
                    else:
                        l = [numberqueue for i in range(len(values))]
                        realvalue = "{0:6.2f}".format(numberqueue)

                elif t.startswith("UTILIZATION"):
                    l = [utilization for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(utilization)

                truevalue = np.array(l)
                axs[0].plot(truevalue)
                axs[0].legend(["Analytical result: " + realvalue])

            else:
                globalwait, globaldelay, globalnumber, delay, wait, number, utilization = analyticalResults(
                    batchMeanTemplate["interarrival"], model)

                if t.startswith("GLOBAL AVG WAIT"):
                    l = [globalwait for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(globalwait)

                elif t.startswith("GLOBAL AVG DELAY"):
                    l = [globaldelay for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(globaldelay)

                elif t.startswith("GLOBAL AVG NUMBER"):
                    l = [globalnumber for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(globalnumber)

                elif t.startswith("QUEUE1 AVG WAIT"):
                    l = [wait[0] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(wait[0])

                elif t.startswith("QUEUE1 AVG DELAY"):
                    l = [delay[0] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(delay[0])

                elif t.startswith("QUEUE1 AVG NUMBER"):
                    l = [number[0] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(number[0])

                elif t.startswith("QUEUE2 AVG WAIT"):
                    l = [wait[1] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(wait[1])

                elif t.startswith("QUEUE2 AVG DELAY"):
                    l = [delay[1] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(delay[1])

                elif t.startswith("QUEUE2 AVG NUMBER"):
                    l = [number[1] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(number[1])

                elif t.startswith("QUEUE3 AVG WAIT"):
                    l = [wait[2] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(wait[2])

                elif t.startswith("QUEUE3 AVG DELAY"):
                    l = [delay[2] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(delay[2])

                elif t.startswith("QUEUE3 AVG NUMBER"):
                    l = [number[2] for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(number[2])

                elif t.startswith("UTILIZATION"):
                    l = [utilization for i in range(len(values))]
                    realvalue = "{0:6.2f}".format(utilization)

                truevalue = np.array(l)
                axs[0].plot(truevalue)
                axs[0].legend(["Analytical result: " + realvalue])

        if t.startswith("UTILIZATION"):
            maxvalue = np.max(values) + np.max(errors)
            minvalue = np.min(values) - np.max(errors)
            plt.ylim(minvalue - 0.05, maxvalue + 0.05)
        elif t.endswith("NUMBER"):
            maxvalue = np.max(values) + np.max(errors)
            minvalue = np.min(values) - np.max(errors)
            plt.ylim(minvalue - 0.1, maxvalue + 0.1)
        else:
            maxvalue = np.max(values) + np.max(errors)
            minvalue = np.min(values) - np.max(errors)
            plt.ylim(minvalue - 0.1, maxvalue + 0.1)

        cellText = []
        for j in range(len(values)):
            # Building cellText to create table
            row = []
            row.append(str(seeds[j]))
            row.append(str(values[j]))
            row.append("±" + str(errors[j]))
            row.append("95%")
            cellText.append(row)

        # Plotting Table and Graph
        rows = [("Replica " + str(j)) for j in range(0, len(values))]
        cols = ("SEED", "MEAN VALUE", "ERROR", "CONFIDENCE LEVEL")
        axs[1].axis('tight')
        axs[1].axis('off')
        axs[1].table(cellText=cellText,
                     rowLabels=rows,
                     cellLoc='center',
                     colLabels=cols,
                     loc='center')
        axs[0].errorbar(x, values, errors, fmt='.')
        axs[0].set_title(title, fontsize=8)
        plt.subplots_adjust(left=0.2, bottom=0.1)
        plt.savefig(path + "/" + t + ".png", dpi=350)
        plt.close()


def transientPlotter(path, model, transientList, realistic):
    # Generate plot for transient simulation
    global transientTemplate

    interarrivals = transientTemplate["interarrival"]
    SERVERS = int(transientTemplate["servers"])
    title = ""

    if model == 1:
        # MG1_ABS_NETWORK
        center_name_1 = "c1"
        center_name_2 = "c2"
        center_name_3 = "c3"
        center_name_4 = "c4"
        center_name_5 = "c5"
        center_name_6 = "c6"
        organizer = {
            "avg_utilization1": [],
            "avg_utilization2": [],
            "avg_utilization3": [],
            "avg_utilization4": [],
            "avg_utilization5": [],
            "avg_utilization6": [],
            "global": {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_1: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_2: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_3: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_4: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_5: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_6: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            "mean_conditional_slowdown": {"(1.24)": [], "(2.65)": [], "(4.42)": [], "(8.26)": []}
        }

    else:
        center_name_1 = "q1"
        center_name_2 = "q2"
        center_name_3 = "q3"
        organizer = {
            "avg_utilization1": [],
            "avg_utilization2": [],
            "avg_utilization3": [],
            "avg_utilization4": [],
            "avg_utilization5": [],
            "avg_utilization6": [],
            "global": {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_1: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_2: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            center_name_3: {"avg_wait": [], "avg_delay": [], "avg_number": []},
            "mean_conditional_slowdown": {"(1.24)": [], "(2.65)": [], "(4.42)": [], "(8.26)": []}
        }

    jobs_acquisition = transientList[0]['index']
    job_number = len(transientList[0]['index'])

    organizer = initialize_transient_organizer(organizer, job_number, transientList)

    avg_wait_global, avg_delay_global, avg_number_global, avg_utilizations, avg_wait_queues, \
    avg_delay_queues, avg_number_queues = [], [], [], [], [], [], []

    for i in range(0, len(organizer["global"]["avg_wait"])):
        avg_wait_global.append(organizer["global"]["avg_wait"][i])
    for i in range(0, len(organizer["global"]["avg_delay"])):
        avg_delay_global.append(organizer["global"]["avg_delay"][i])
    for i in range(0, len(organizer["global"]["avg_number"])):
        avg_number_global.append(organizer["global"]["avg_number"][i])

    if model == 1:
        # MG1_ABS_NETWORK
        for j in range(SERVERS):
            avg_utilizations.append([])
            avg_wait_queues.append([])
            avg_delay_queues.append([])
            avg_number_queues.append([])
    else:
        for j in range(SERVERS):
            avg_utilizations.append([])
        for j in range(3):
            avg_wait_queues.append([])
            avg_delay_queues.append([])
            avg_number_queues.append([])

    for j in range(1, SERVERS + 1):
        for i in range(0, len(organizer["avg_utilization" + str(j)])):
            avg_utilizations[j - 1].append(organizer["avg_utilization" + str(j)][i])

    for i in range(0, len(organizer[center_name_1]["avg_wait"])):
        if SERVERS >= 1: avg_wait_queues[0].append(organizer[center_name_1]["avg_wait"][i])
    for i in range(0, len(organizer[center_name_2]["avg_wait"])):
        if SERVERS >= 2: avg_wait_queues[1].append(organizer[center_name_2]["avg_wait"][i])
    for i in range(0, len(organizer[center_name_3]["avg_wait"])):
        if SERVERS >= 3: avg_wait_queues[2].append(organizer[center_name_3]["avg_wait"][i])

    for i in range(0, len(organizer[center_name_1]["avg_delay"])):
        if SERVERS >= 1: avg_delay_queues[0].append(organizer[center_name_1]["avg_delay"][i])
    for i in range(0, len(organizer[center_name_2]["avg_delay"])):
        if SERVERS >= 2: avg_delay_queues[1].append(organizer[center_name_2]["avg_delay"][i])
    for i in range(0, len(organizer[center_name_3]["avg_delay"])):
        if SERVERS >= 3: avg_delay_queues[2].append(organizer[center_name_3]["avg_delay"][i])

    for i in range(0, len(organizer[center_name_1]["avg_number"])):
        if SERVERS >= 1: avg_number_queues[0].append(organizer[center_name_1]["avg_number"][i])
    for i in range(0, len(organizer[center_name_2]["avg_number"])):
        if SERVERS >= 2: avg_number_queues[1].append(organizer[center_name_2]["avg_number"][i])
    for i in range(0, len(organizer[center_name_3]["avg_number"])):
        if SERVERS >= 3: avg_number_queues[2].append(organizer[center_name_3]["avg_number"][i])

    if model == 1 and SERVERS >= 4:
        for i in range(0, len(organizer[center_name_4]["avg_wait"])):
            avg_wait_queues[3].append(organizer[center_name_1]["avg_wait"][i])
        for i in range(0, len(organizer[center_name_5]["avg_wait"])):
            if SERVERS >= 5: avg_wait_queues[4].append(organizer[center_name_2]["avg_wait"][i])
        for i in range(0, len(organizer[center_name_6]["avg_wait"])):
            if SERVERS >= 6: avg_wait_queues[5].append(organizer[center_name_3]["avg_wait"][i])

        for i in range(0, len(organizer[center_name_4]["avg_delay"])):
            avg_delay_queues[3].append(organizer[center_name_1]["avg_delay"][i])
        for i in range(0, len(organizer[center_name_5]["avg_delay"])):
            if SERVERS >= 5: avg_delay_queues[4].append(organizer[center_name_2]["avg_delay"][i])
        for i in range(0, len(organizer[center_name_6]["avg_delay"])):
            if SERVERS >= 6: avg_delay_queues[5].append(organizer[center_name_3]["avg_delay"][i])

        for i in range(0, len(organizer[center_name_4]["avg_number"])):
            avg_number_queues[3].append(organizer[center_name_1]["avg_number"][i])
        for i in range(0, len(organizer[center_name_5]["avg_number"])):
            if SERVERS >= 5: avg_number_queues[4].append(organizer[center_name_2]["avg_number"][i])
        for i in range(0, len(organizer[center_name_6]["avg_number"])):
            if SERVERS >= 6: avg_number_queues[5].append(organizer[center_name_3]["avg_number"][i])

    res = transientTemplate
    res["JOBS"] = jobs_acquisition

    for j in range(0, len(avg_number_global)):
        res["GLOBAL AVG NUMBER"].append({"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
        res["GLOBAL AVG WAIT"].append({"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
        res["GLOBAL AVG DELAY"].append({"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})

    if model == 0:
        # MSMQ_SB_NETWORK
        for j in range(1, 4):
            for k in range(0, len(avg_number_global)):
                res["QUEUE" + str(j) + " AVG NUMBER"].append(
                    {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
                res["QUEUE" + str(j) + " AVG WAIT"].append(
                    {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
                res["QUEUE" + str(j) + " AVG DELAY"].append(
                    {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
    else:
        for j in range(1, SERVERS + 1):
            for k in range(0, len(avg_number_global)):
                res["QUEUE" + str(j) + " AVG NUMBER"].append(
                    {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
                res["QUEUE" + str(j) + " AVG WAIT"].append(
                    {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})
                res["QUEUE" + str(j) + " AVG DELAY"].append(
                    {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})

    for j in range(1, SERVERS + 1):
        for k in range(0, len(avg_number_global)):
            res["UTILIZATION" + str(j)].append(
                {"mean": 0.0, "half_confidence_interval": 0.0, "stdev": 0.0, "confidence": 95})

    for j in range(0, len(avg_number_global)):
        if len(avg_number_global[j]) >= 4:
            mean, stdev, half_interval = estimate(avg_number_global[j])
            res["GLOBAL AVG NUMBER"][j]["mean"] = mean
            res["GLOBAL AVG NUMBER"][j]["stdev"] = stdev
            res["GLOBAL AVG NUMBER"][j]["half_confidence_interval"] = half_interval

    for j in range(0, len(avg_wait_global)):
        if len(avg_wait_global[j]) >= 4:
            mean, stdev, half_interval = estimate(avg_wait_global[j])
            res["GLOBAL AVG WAIT"][j]["mean"] = mean
            res["GLOBAL AVG WAIT"][j]["stdev"] = stdev
            res["GLOBAL AVG WAIT"][j]["half_confidence_interval"] = half_interval

    for j in range(0, len(avg_delay_global)):
        if len(avg_delay_global[j]) >= 4:
            mean, stdev, half_interval = estimate(avg_delay_global[j])
            res["GLOBAL AVG DELAY"][j]["mean"] = mean
            res["GLOBAL AVG DELAY"][j]["stdev"] = stdev
            res["GLOBAL AVG DELAY"][j]["half_confidence_interval"] = half_interval

    if model == 0:
        # MSMQ_SB_NETWORK
        for j in range(1, 4):
            for k in range(0, len(avg_wait_queues[j - 1])):
                if len(avg_wait_queues[j - 1]) >= 4:
                    mean, stdev, half_interval = estimate(avg_wait_queues[j - 1][k])
                    res["QUEUE" + str(j) + " AVG WAIT"][k]["mean"] = mean
                    res["QUEUE" + str(j) + " AVG WAIT"][k]["stdev"] = stdev
                    res["QUEUE" + str(j) + " AVG WAIT"][k]["half_confidence_interval"] = half_interval

            for k in range(0, len(avg_delay_queues[j - 1])):
                if len(avg_delay_queues[j - 1]) >= 4:
                    mean, stdev, half_interval = estimate(avg_delay_queues[j - 1][k])
                    res["QUEUE" + str(j) + " AVG DELAY"][k]["mean"] = mean
                    res["QUEUE" + str(j) + " AVG DELAY"][k]["stdev"] = stdev
                    res["QUEUE" + str(j) + " AVG DELAY"][k]["half_confidence_interval"] = half_interval

            for k in range(0, len(avg_number_queues[j - 1])):
                if len(avg_number_queues[j - 1]) >= 4:
                    mean, stdev, half_interval = estimate(avg_number_queues[j - 1][k])
                    res["QUEUE" + str(j) + " AVG NUMBER"][k]["mean"] = mean
                    res["QUEUE" + str(j) + " AVG NUMBER"][k]["stdev"] = stdev
                    res["QUEUE" + str(j) + " AVG NUMBER"][k]["half_confidence_interval"] = half_interval
    else:
        for j in range(1, SERVERS + 1):
            for k in range(0, len(avg_wait_queues[j - 1])):
                if len(avg_wait_queues[j - 1]) >= 4:
                    mean, stdev, half_interval = estimate(avg_wait_queues[j - 1][k])
                    res["QUEUE" + str(j) + " AVG WAIT"][k]["mean"] = mean
                    res["QUEUE" + str(j) + " AVG WAIT"][k]["stdev"] = stdev
                    res["QUEUE" + str(j) + " AVG WAIT"][k]["half_confidence_interval"] = half_interval

            for k in range(0, len(avg_delay_queues[j - 1])):
                if len(avg_delay_queues[j - 1]) >= 4:
                    mean, stdev, half_interval = estimate(avg_delay_queues[j - 1][k])
                    res["QUEUE" + str(j) + " AVG DELAY"][k]["mean"] = mean
                    res["QUEUE" + str(j) + " AVG DELAY"][k]["stdev"] = stdev
                    res["QUEUE" + str(j) + " AVG DELAY"][k]["half_confidence_interval"] = half_interval

            for k in range(0, len(avg_number_queues[j - 1])):
                if len(avg_number_queues[j - 1]) >= 4:
                    mean, stdev, half_interval = estimate(avg_number_queues[j - 1][k])
                    res["QUEUE" + str(j) + " AVG NUMBER"][k]["mean"] = mean
                    res["QUEUE" + str(j) + " AVG NUMBER"][k]["stdev"] = stdev
                    res["QUEUE" + str(j) + " AVG NUMBER"][k]["half_confidence_interval"] = half_interval

    for j in range(1, SERVERS + 1):
        for k in range(0, len(avg_utilizations[j - 1])):
            mean, stdev, half_interval = estimate(avg_utilizations[j - 1][k])
            res["UTILIZATION" + str(j)][k]["mean"] = mean
            res["UTILIZATION" + str(j)][k]["stdev"] = stdev
            res["UTILIZATION" + str(j)][k]["half_confidence_interval"] = half_interval

    for t in res.keys():
        if t in ["interarrival", "servers", "seed", "JOBS"]:
            continue

        headerbuilder = 0

        if model == 0:
            # MSMQ_SB_NETWORK
            title = "Size Based MSMQ - " + t
        elif model == 1:
            # MG1_ABS_NETWORK
            title = "SSQ Abstract Network - " + t

        seeds, values, errors, jobs = [], [], [], []

        x = transientList[0]['acquisition_time']
        for subdict in res[t]:
            values.append(subdict['mean'])
            errors.append(subdict['half_confidence_interval'])

        for value in jobs_acquisition:
            jobs.append(value)

        if realistic == 0:
            title += "\n" + str(SERVERS) + " Servers -  Avg Interarrival time: " + str(interarrivals) + "min"
        else:
            title += "\n" + str(SERVERS) + " Servers -  Avg Interarrival time: variable"
        title += "\n Finite Horizon Statistics"

        if len(x) == len(values) and len(x) == len(errors):
            fig, axs = plt.subplots(2, 1)
            axs[0].set_xscale('log')
            plt.xlabel("jobs")

            cellText, rows = [], []

            for j in range(len(values)):
                # Building cellText to create table
                row = []
                if j % round(len(values) / 8) == 0:
                    row.append(str(values[j]))
                    row.append("±" + str(errors[j]))
                    row.append("95%")
                    cellText.append(row)
                    rows.append("n° JOB: " + str(jobs[j]))

            # Plotting Table and Graph
            cols = ("MEAN VALUE", "ERROR", "CONFIDENCE LEVEL")
            axs[1].axis('tight')
            axs[1].axis('off')
            axs[1].table(cellText=cellText,
                         rowLabels=rows,
                         cellLoc='center',
                         colLabels=cols,
                         loc='center')
            axs[0].errorbar(x, values, errors, fmt='.')
            axs[0].set_title(title, fontsize=8)
            plt.subplots_adjust(left=0.25, bottom=0.1)
            plt.savefig(path + "/" + t + ".png", dpi=350)
            plt.close()


def transientPlotter2(path, model, transientList, realistic, statistics):

    global transientTemplate
    interarrivals = transientTemplate["interarrival"]
    SERVERS = int(transientTemplate["servers"])
    x = transientList[0]["index"]
    if realistic: x = transientList[0]["acquisition_time"]
    edgecols = ['b', 'g', 'r', 'k', 'm']
    minlenght = INFINITE

    for t in transientList:
        minlenght = min( minlenght, len(t["global"]["avg_"+statistics]) )

    if model == 0:
        for k in transientList[0].keys():
            legend = []
            if k in ["global", "q1", "q2", "q3" ]:
                i = 0
                for t in transientList:
                    if not realistic: plt.xscale('log')
                    x = t["acquisition_time"][:minlenght]
                    if not realistic : plt.scatter( x, t[str(k)]["avg_"+statistics][:minlenght], facecolors='none', edgecolors=edgecols[i] )    
                    else:  plt.scatter( x, t[str(k)]["avg_"+statistics][:minlenght], facecolors='none', edgecolors=edgecols[i], s=10 ) 
                    legend.append("Initial Seed : " + str(t["seed"]))
                    i += 1

                title = "Advanced :: AVERAGE "+ statistics.upper()+ " " + str(k) + " - TRANSIENT BEHAVIOUR"
                if realistic:   title += "\n Avg Interarrivals: variable - Servers : variable" 
                else:           title += "\n Avg Interarrivals: " + str(interarrivals) + " - Servers : " + str(SERVERS)

                plt.legend(legend)
                if realistic == 1 :
                    plt.axvline(x = 120, linestyle='dashed', color = 'k')
                    plt.axvline(x = 300, linestyle='dashed', color = 'k')
                    plt.axvline(x = 420, linestyle='dashed', color = 'k')
                    plt.axvline(x = 720, linestyle='dashed', color = 'k')
                    plt.axvline(x = 840, linestyle='dashed', color = 'k')
                plt.xlabel("Time (min)")
                #plt.ylim(0, 20)
                plt.title(title)
                plt.savefig(path + "/" + k + "_avg_"+statistics+"_TP2.png", dpi=350)       
                plt.close()
    
    else:
        for k in transientList[0].keys():
            legend = []
            if k in ["global", "c1", "c2", "c3", "c4", "c5", "c6" ]:
                i = 0
                for t in transientList:
                    if not realistic: plt.xscale('log')
                    x = t["acquisition_time"][:minlenght]
                    if not realistic : plt.scatter( x, t[str(k)]["avg_delay"][:minlenght], facecolors='none', edgecolors=edgecols[i] )    
                    else:  plt.plot( x, t[str(k)]["avg_delay"][:minlenght] ) 
                    legend.append("Initial Seed : " + str(t["seed"]))
                    i += 1
 
                title = "Classic :: AVERAGE DELAY " + str(k) + " - TRANSIENT BEHAVIOUR"
                if realistic:   title += "\n Avg Interarrivals: variable - Servers : " + str(SERVERS)
                else:           title += "\n Avg Interarrivals: " + str(interarrivals) + " - Servers : " + str(SERVERS)

                if realistic == 1 :
                    plt.axvline(x = 120, linestyle='dashed', color = 'k')
                    plt.axvline(x = 300, linestyle='dashed', color = 'k')
                    plt.axvline(x = 420, linestyle='dashed', color = 'k')
                    plt.axvline(x = 720, linestyle='dashed', color = 'k')
                    plt.axvline(x = 840, linestyle='dashed', color = 'k')

                plt.legend( legend )
                plt.title(title)
                plt.savefig(path + "/" + k + "_avg_delay_TP2.png", dpi=350)       
                plt.close()

    