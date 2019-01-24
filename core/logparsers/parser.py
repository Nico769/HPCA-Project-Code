from collections import defaultdict
from sys import argv
import re
import os
import pandas as pd

# global variable for the number of MPI nodes
glob_num_nodes = 0
# constant label for the number of MPI nodes
nodes_label = 'nodes_number'

def has_mo_match(matched_object):
    '''Determine if matched_object is None or not'''
    if matched_object is not None:
        return True
    else:
        return False
        
def parse_monte_carlo_time(line):
    '''Parse the slowest processor and its execution time 
       for the monte_carlo_pi algorithm using Regular Expressions'''
    matched = re.compile(r'time\:\s(\d{1,6}\.\d{1,6})').search(line)
    if has_mo_match(matched):
        return matched.group(1)
    else:
        return None

def parse_matmul_exec_type_time(line):
    '''Parse 'serial' or 'parallel' keywords and the execution time
       for the matmul algorithm using Regular Expressions'''
    matched = re.compile(r'(serial|parallel).*?((\d{1,6}\.\d{1,6}))').search(line)
    if has_mo_match(matched):
        return matched.group(1), matched.group(2)
    else:
        return None
        
def parse_end(line):
    '''Parse End marker using Regular Expressions'''
    matched = re.compile(r'End').search(line)
    if has_mo_match(matched):
        return matched.group()
    else:
        return None

def sanitize_filename(name):
    '''Verifies if the provided filename is legal and returns its \'mpi.*.*.csv\' relative'''
    # a list containing False and an empty string because the provided filename is not valid
    err_list = [False,'']
    if 'mpi' not in name and 'log' not in name:
        return err_list

    # name looks promising, let's tokenize it
    tokenized_name = name.split('.')
    # try to pop log extension, don't need it
    try:
        tokenized_name.remove('log')
    except ValueError:
        print('DEBUG: tokenized_name doesn\'t contain log keyword')
        return err_list
    
    # tokenized_name should be like this: ['mpi', '6', '100']
    # which means the csv_filename is going to be: 'mpi.6.100.csv'
    csv_filename = '{0}.{1}.{2}.csv'.format(tokenized_name[0], tokenized_name[1], tokenized_name[2])
    # Store the tokenized number of MPI nodes
    global glob_num_nodes
    glob_num_nodes = tokenized_name[1]
    # return True and csv_filename since the validation has been successful
    return [True, csv_filename]

def log_file_to_dataframe(log_content_list):
    '''Provides a Pandas DataFrame given a properly formed log file's content
    '''
    # init an empty defaultdict, it is convenient for indexing the data
    # in the format we want
    measurements = defaultdict(dict)
    # keep track of the number of measurements in the log file
    measurement_counter = 1
    for line in log_content_list:
        if parse_monte_carlo_time(line) is not None:
            # line contains the time of the slowest processor, let's save it
            time = parse_monte_carlo_time(line)
            slowest_label = 'slowest_node_mc_pi'
            # add the Slowest label and the parsed time to measurements dict
            # having measurement_counter index. This yelds to a dict of dicts
            measurements[measurement_counter][slowest_label] = time
            # and the nodes_number label too
            measurements[measurement_counter][nodes_label] = glob_num_nodes
        elif parse_matmul_exec_type_time(line) is not None:
            # line contains serial/parallel keyword and the execution time
            result = parse_matmul_exec_type_time(line)
            execution_type = result[0] + '_matmul'
            time = result[1]
            # add the execution type and the time to measurements dict
            # having measurement_counter index. This yelds to a dict of dicts
            measurements[measurement_counter][execution_type] = time
            # and the nodes_number label too
            measurements[measurement_counter][nodes_label] = glob_num_nodes
        elif parse_end(line) is not None:
            # line contains 'End' marker, end of this measurement reached
            measurement_counter += 1
    # convert the measurements dict to a DataFrame
    df = pd.DataFrame(measurements).T
    # rename the df default index to Measurements
    df.index.name = 'Measurements'
    return df

# define a couple of user-oriented messages
usage_msg = 'Usage: \'python parser.py [log_file_to_parse.log]\'\n'
fileformat_msg = '''[log_file_to_parse.log] must adhere the following conventions:\n
            - Sequential/parallel PI logs naming convention:
            mpi$num_nodes.$num_trials.log
            - Sequential/parallel MatMul logs naming convention:
            mpi$num_nodes.$mat_dim.log
            '''
wrong_fileformat_msg = 'Are you sure you\'re using the correct log file? Please try again.'

# get the user input; hopefully it's a proper log filename
filename = argv[1] if len(argv) > 1 else None
# declare an empty string for the csv filename we will generate at the end of this script
csv_filename = ''

# do a couple of checks on the user input
if filename is None:
    print(usage_msg)
    print(fileformat_msg)
    exit()
else:
    print('About to parse: \'{0}\''.format(filename))
    # verify if we are dealing with a valid format
    check_name_list = sanitize_filename(filename)
    if check_name_list[0] == False:
        print(wrong_fileformat_msg)
        print('Exiting...')
        exit()
    else:
        print('Parsing \'{0}\'...'.format(filename))
        csv_filename = check_name_list[1]
        
print('Creating a CSV file:', csv_filename)
# declare an empty list for the log file's content
log_content_list = []
# construct the correct path for the logs folder. Please note the hardcoded folders!
home_folder_env = os.environ['HOME']
logs_folder = os.path.join(home_folder_env, 'cloud/core/logparsers/logs/')
# if the logs folder can't be found on logs_folder path exit gracefully
if not os.path.exists(logs_folder):
    print('Ops! Logs folder can\'t be found at', logs_folder)
    print('Exiting...')
    exit()
# read the log file's content and store it as a list of strings
with open(logs_folder + filename) as f:
    log_content_list = f.readlines()

# strip the newline char from the list
log_content_list = [x.strip('\n') for x in log_content_list]
# filter out empty strings, just to speedup the regex matching
log_content_list = list(filter(None, log_content_list))
# convert the relevant log file's content to a DataFrame
df = log_file_to_dataframe(log_content_list)
# construct the correct path for the csv folder. Please note the hardcoded folders!
csv_folder = os.path.join(home_folder_env, 'cloud/core/logparsers/csv/')
# try to create the csv folder if it doesn't exist.
# Note that os.mkdir creates the child folder (e.g. csv) only!
if not os.path.exists(csv_folder):
    print('csv folder doesn\'t exist. Creating one at \'{0}\''.format(csv_folder))
    os.mkdir(csv_folder)
# convert this df to a csv file
df.to_csv(csv_folder + csv_filename, encoding='utf-8-sig', sep=';')
print('\'{0}\' created'.format(csv_filename))
print('Done.\n')