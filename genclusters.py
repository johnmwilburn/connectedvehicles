import csv
import random


def get_data_from_csv(file_name):
    return_data = open(file_name)
    return_data = csv.reader(return_data)
    return_data = list(return_data)[1:]

    return return_data


def generate_data_metrics(temp_data):
    temp_node_ids = []
    initial_time = int(temp_data[1][0])
    temp_simulation_timespan = 0

    for row in temp_data:
        time = int(row[0])
        curr_id = int(row[1])

        if time == 38:
            temp_node_ids.append(curr_id)

        temp_simulation_timespan = 1 + (time - initial_time)

    return_metrics = (temp_simulation_timespan, temp_node_ids)
    return return_metrics


def identify_outliers(temp_data, temp_simulation_timespan, temp_node_ids):
    outlier_ids = []

    # Identifying nodes from dataset for which there are not enough entries, (less than simulation timespan)
    for node_id in temp_node_ids:

        num_node_entries = 0
        for row in temp_data:
            if int(row[1]) == node_id:
                num_node_entries += 1

        if num_node_entries != temp_simulation_timespan:
            outlier_ids.append(node_id)

    return outlier_ids


def remove_outliers_from_data(temp_data, outlier_ids):
    return_data = temp_data.copy()

    num_rows_removed_from_dataset = 0
    for index in range(len(temp_data)):
        for outlier_id in outlier_ids:
            if int(temp_data[index][1]) == outlier_id:
                return_data.pop(index - num_rows_removed_from_dataset)
                num_rows_removed_from_dataset += 1

    return return_data


def split_data_into_clusters(temp_data, temp_node_ids, do_shuffle):
    num_nodes = len(temp_node_ids)

    if do_shuffle:
        random.shuffle(temp_node_ids)

    cluster_one_ids = temp_node_ids[0:int(num_nodes / 2)]
    cluster_two_ids = temp_node_ids[int(num_nodes / 2): num_nodes]

    cluster_one_data = []
    cluster_two_data = []

    for node_id in cluster_one_ids:
        for row in temp_data:
            if int(row[1]) == node_id:
                cluster_one_data.append(row)

    for node_id in cluster_two_ids:
        for row in temp_data:
            if int(row[1]) == node_id:
                cluster_two_data.append(row)

    return cluster_one_ids, cluster_two_ids, cluster_one_data, cluster_two_data


def skew_data(colluding_nodes_temp, value_to_skew, skew_value):
    for row in colluding_nodes_temp:
        row[value_to_skew] = float(row[4]) * random.uniform(1 - skew_value, 1 + skew_value)
    return colluding_nodes_temp


data = get_data_from_csv('OnRamp1.csv')
simulation_timespan, node_ids = generate_data_metrics(data)

bad_ids = identify_outliers(data, simulation_timespan, node_ids)
data = remove_outliers_from_data(data, bad_ids)
node_ids = list(set(node_ids) - set(bad_ids))

randomize_clusters = True
cluster1_ids, cluster2_ids, cluster1_data, cluster2_data = split_data_into_clusters(data, node_ids, randomize_clusters)

x_coord, y_coord, speed, acceleration = 2, 3, 4, 5 # Denotes the column index of each metric in the datasets
skew_amount = 0.5
colluding_nodes_data = skew_data(cluster2_data, speed, skew_amount)
