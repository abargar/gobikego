#!/Python33/python
"""
ST-DBSCAN: Sptio-Temporal DBSCAN
"""

import numpy as np
from random import shuffle
from sklearn.neighbors import NearestNeighbors
import read_data
from sklearn.cluster.dbscan_ import DBSCAN, dbscan
import json

def get_neighbor(index, neighbors_models, X_array, eps_array):
    index_neighbor_array = []
    for i in range(len(eps_array)):
        index_neighbor = neighbors_models[i].radius_neighbors(X_array[i][index], return_distance=False)[0]
        index_neighbor_array.append(index_neighbor)
    ret_index_neighbor = index_neighbor_array[0]
    # print "0", len(ret_index_neighbor)
    for i in range(1, len(eps_array)):
        ret_index_neighbor = np.intersect1d(ret_index_neighbor, index_neighbor_array[i])
        # print i, len(ret_index_neighbor)
    return ret_index_neighbor

def get_neighbor_model(X, eps):
    neighbors_model = NearestNeighbors(radius=eps, leaf_size=30, algorithm='ball_tree')
    neighbors_model.fit(X)
    # print neighbors_model
    return neighbors_model

def stdbscan(X_array, eps_array, min_samples=200):
    # X / eps Array: (start-station), (end-station), (start-time, end-time)
    num_eps = len(eps_array)
    # print num_eps, len(X_array)
    if num_eps != len(X_array) or num_eps < 1:
        # print "err 1"
        return

    # print len(X_array[0])
    num_data = len(X_array[0])


    index_order = range(num_data)
    shuffle(index_order)

    neighbors_models = []
    for i in range(num_eps):
        # print X_array[i]
        neighbors_model = get_neighbor_model(X_array[i], eps_array[i])
        neighbors_models.append(neighbors_model)

        # for j in range(num_data):
        #     print eps_array[0]
        #     tempind = neighbors_model.radius_neighbors(X_array[0][j], return_distance=False)[0]
        #     print j, len(tempind), tempind

    labels = -np.ones(num_data, dtype=np.int)

    label_num = 0

    for index in index_order:
        if labels[index] != -1:
            continue

        # print 'index', index

        index_neighborhood = get_neighbor(index, neighbors_models, X_array, eps_array)



        # print 'len', len(index_neighborhood)
        if len(index_neighborhood) < min_samples:
            continue

        labels[index] = label_num
        candidates = [index]

        while len(candidates) > 0:
            new_candidates = []
            for c in candidates:
                c_neighborhood = get_neighbor(c, neighbors_models, X_array, eps_array)

                noise = np.where(labels[c_neighborhood] == -1)[0] # labels[] == -1 from c_neighborhood
                noise = c_neighborhood[noise]
                labels[noise] = label_num

                # print 'noise', noise

                for neighbor in noise:
                    n_neighborhood = get_neighbor(neighbor, neighbors_models, X_array, eps_array)

                    if len(n_neighborhood) >= min_samples:
                        new_candidates.append(neighbor)

            candidates = new_candidates
        label_num += 1
    return labels


def format_result(result_dic_array):
    formated_result = {}
    for entry in result_dic_array:
        if entry['category'] == -1:
            continue
        category = entry['category']
        if not formated_result.has_key(category):
            formated_result[category] = {}
        start_st_id = entry['start_st_id']
        end_st_id = entry['end_st_id']
        if not formated_result[category].has_key(start_st_id):
            formated_result[category][start_st_id] = {}
        if not formated_result[category][start_st_id].has_key(end_st_id):
            formated_result[category][start_st_id][end_st_id] = 1
        else:
            formated_result[category][start_st_id][end_st_id] += 1
    return formated_result


if __name__ == '__main__':
    print 'Content-type: json\n\n'
    # trip_file_path = "../data/hubway_2011_trips_info.json"
    # station_file_path = "../data/hubway_2011_stations_info.json"

    c = '--'

    # result_file_path = "./temp_result_" + "0am_2am" + ".json"
    # result_format_file_path = "./temp_result_" + "0am_2am" + "_format.json"

#     station_info_dict = read_station_info(station_file_path)
#     print station_info_dict

    X_trip_start_station, X_trip_end_station, X_trip_start_end_time, index_tripid_lookup_table, trip_info_dict = read_data.get_X_for_trip_start_end_station_time()
    Xarray = [X_trip_start_station, X_trip_end_station, X_trip_start_end_time]
    # print Xarray
    # print "read done"
    # print len(X_trip_start_station)
    # print X_trip_start_station

####


    labels = stdbscan(Xarray, [0.005, 0.005, 20 * 600000])

    result_dic_array = []
    for i in range(len(labels)):
        trip_id = index_tripid_lookup_table[i]
        category = labels[i]
        trip_info_dict[trip_id]['category'] = category
        result_dic_array.append(trip_info_dict[trip_id])

    formated_result = format_result(result_dic_array)

    result_json = json.dumps(result_dic_array, indent=4)
    result_json_format = json.dumps(formated_result, indent=4)

    print(result_json_format)

    # f = open(result_file_path, 'w')
    # f.write(result_json)
    # f.close()

    # f = open(result_format_file_path, 'w')
    # f.write(result_json_format)
    # f.close()
