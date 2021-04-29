import multiprocessing
from math import floor, sqrt
import pandas as pd
import numpy as np

num_neighbors = 3
exponent = 2


# def get_sample_time(time):
#     monthday = time
#     month = int(floor(monthday * 10**-2))
#     day = monthday - month * 10**2
#     months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#     new_time = 0
#     for i in range(month-1):
#         new_time += months[i]
#     new_time += day
#     return new_time


def get_lambdai(neighbor, nearest_neighbors):
    denominator_sum = 0
    distancei = neighbor[-1]
    numerator = (1/distancei)**exponent
    for nearest_neighbor in nearest_neighbors:
        denominator_sum += (1/nearest_neighbor[-1])**exponent
    return numerator/denominator_sum


def euclidean_distance(sample_row, county_row):
    euclidean_sum = 0
    sample_x = sample_row[0]
    county_x = county_row[0]
    sample_y = sample_row[1]
    county_y = county_row[1]
    sample_time = sample_row[2]
    county_time = county_row[2]
    euclidean_sum += (sample_x - county_x) ** 2
    euclidean_sum += (sample_y - county_y) ** 2
    euclidean_sum += (sample_time - county_time) ** 2
    return sqrt(euclidean_sum)


def get_neighbors(samplePMData, county_row):
    flattened_distances_list = list()
    for row in range(len(samplePMData)):
        flattened_distances = list()
        dist = euclidean_distance(samplePMData[row], county_row)
        for data in samplePMData[row]:
            flattened_distances.append(data)
        flattened_distances.append(dist)
        flattened_distances_list.append(flattened_distances)
    flattened_distances_list.sort(key=lambda tup: tup[-1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(flattened_distances_list[i])
    return neighbors


def interpolate():
    w = 0
    nearest_neighbors = get_neighbors(training_set, test_set[row])
    for neighbor in nearest_neighbors:
        lambdai = get_lambdai(neighbor, nearest_neighbors)
        wi = neighbor[3]
        print(wi)
        w += wi * lambdai
    return w


def import_data(pm_filename):
    dataframe = pd.read_csv(pm_filename, sep='\t', header=None)
    return dataframe


def to_array(dataframe):
    return np.array(dataframe)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fold_file_names = [
        "fold1",
        "fold2",
        "fold3",
        "fold4",
        "fold5",
        "fold6",
        "fold7",
        "fold8",
        "fold9",
        "fold10"
    ]

    pool = multiprocessing.Pool(4)

    for i in range(0, 10):
        # numerator = 0

        # Import data
        training_set = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/st_sample.txt')
        training_pm = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/value_sample.txt')
        training_set["3"] = training_pm
        training_set = to_array(training_set)

        test_set = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/st_test.txt')
        test_set = to_array(test_set)

        for row in range(len(test_set)):

            interpolation = interpolate()
            print(interpolation)

        # error validation
        # validation_set = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/value_test.txt')
        # validation_set = to_array(validation_set)
        # numerator += (abs(interpolation - validation_set[row][0]) * 100) / interpolation
        # denominator = len(validation_set)
        # mape = numerator/denominator
        # print("mean absolute percentage error: " + str(mape) + "%")
