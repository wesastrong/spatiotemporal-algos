import multiprocessing
import numpy as np
import pandas as pd

from functools import partial
from math import floor, sqrt


# def write_mape(mape, file_names, count):
#     with open('10FoldCrossValidation/' + file_names[count] + '/10foldcv_sf' + file_names[count] + '.txt', 'a') as f:
#         f.write(str(mape))
#         print(str(mape))
#     f.close()


def write_w(interpolation, file_names, count):
    with open('10FoldCrossValidation/' + file_names[count] + '/10foldcv_sf' + file_names[count] + '.txt', 'a') as f:
        f.write(str(interpolation))
        f.write('\n')
        print(str(interpolation))
    f.close()


def get_lambdai(neighbor, nearest_neighbors, exponent):
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


def get_neighbors(samplePMData, county_row, num_neighbors):
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


def interpolate(training_set, n, p, file_names, count, test_row):
    w = 0
    nearest_neighbors = get_neighbors(training_set, test_row, n)
    for neighbor in nearest_neighbors:
        lambdai = get_lambdai(neighbor, nearest_neighbors, p)
        wi = neighbor[3]
        w += wi * lambdai
    write_w(w, file_names, count)


def import_data(pm_filename):
    dataframe = pd.read_csv(pm_filename, sep='\t', header=None)
    return dataframe


def to_array(dataframe):
    return np.array(dataframe)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    num_neighbors = int(input("For how many nearest neighbors would you like to interpolate? "))
    exponent = float(input("Enter a float to use as an exponent in the weighting process: "))
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

    for i in range(0, 10):
        pool = multiprocessing.Pool(4)

        # Import data
        training_set = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/st_sample.txt')
        training_pm = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/value_sample.txt')
        training_set["3"] = training_pm
        training_set = to_array(training_set)

        test_set = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/st_test.txt')
        test_set = to_array(test_set)
        size = floor(len(test_set)/4)

        validation_set = import_data('10FoldCrossValidation/'+fold_file_names[i]+'/value_test.txt')
        validation_set = to_array(validation_set)

        temp = partial(interpolate, training_set, num_neighbors, exponent, fold_file_names, i)
        interpolations = pool.map(func=temp, iterable=test_set, chunksize=size)

        pool.close()
