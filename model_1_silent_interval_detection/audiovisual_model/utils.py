import csv
import json
import logging
import os
import shutil


class TrainClock(object):
    """ Clock object to track epoch and step during training
    """
    def __init__(self):
        self.epoch = 0
        self.minibatch = 0
        self.step = 0

    def tick(self):
        self.minibatch += 1
        self.step += 1

    def tock(self):
        self.epoch += 1
        self.minibatch = 0

    def make_checkpoint(self):
        return {
            'epoch': self.epoch,
            'minibatch': self.minibatch,
            'step': self.step
        }

    def restore_checkpoint(self, clock_dict):
        self.epoch = clock_dict['epoch']
        self.minibatch = clock_dict['minibatch']
        self.step = clock_dict['step']


class Table(object):
    def __init__(self, filename):
        '''
        create a table to record experiment results that can be opened by excel
        :param filename: using '.csv' as postfix
        '''
        assert '.csv' in filename
        self.filename = filename

    @staticmethod
    def merge_headers(header1, header2):
        #return list(set(header1 + header2))
        if len(header1) > len(header2):
            return header1
        else:
            return header2

    def write(self, ordered_dict):
        '''
        write an entry
        :param ordered_dict: something like {'name':'exp1', 'acc':90.5, 'epoch':50}
        :return:
        '''
        if os.path.exists(self.filename) == False:
            headers = list(ordered_dict.keys())
            prev_rec = None
        else:
            with open(self.filename) as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                prev_rec = [row for row in reader]
            headers = self.merge_headers(headers, list(ordered_dict.keys()))

        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            if not prev_rec == None:
                writer.writerows(prev_rec)
            writer.writerow(ordered_dict)


class WorklogLogger:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file,
                            level=logging.DEBUG,
                            format='%(asctime)s - %(threadName)s -  %(levelname)s - %(message)s')

        self.logger = logging.getLogger()

    def put_line(self, line):
        self.logger.info(line)


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name):
        self.name = name
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def save_args(args, save_dir):
    param_path = os.path.join(save_dir, 'params.json')

    with open(param_path, 'w') as fp:
        json.dump(args.__dict__, fp, indent=4, sort_keys=True)


def ensure_dir(path):
    """
    create path by first checking its existence,
    :param paths: path
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def ensure_dirs(paths):
    """
    create paths by first checking their existence
    :param paths: list of path
    :return:
    """
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            ensure_dir(path)
    else:
        ensure_dir(paths)


def remkdir(path):
    """
    if dir exists, remove it and create a new one
    :param path:
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def get_parent_dir(path):
    """Get parent directory"""
    return os.path.abspath(os.path.join(path, os.pardir))


def get_path_same_dir(path, new_file_name):
    """Get the absolute path of a new file that is in the same directory as another file"""
    return os.path.join(get_parent_dir(path), new_file_name)


def get_basename_no_ext(path):
    """Get the basename of a file without the extension"""
    return os.path.splitext(os.path.basename(path))[0]


def cycle(iterable):
    while True:
        for x in iterable:
            yield x


def print_dictionary(dictionary, sep=',', key_list=None, omit_keys=False):
    """ Pretty print dictionary """
    if key_list is None:
        key_list = dictionary.keys()
    print('{', end='')
    for idx, key in enumerate(key_list):
        end_str = sep + ' ' if idx < len(key_list)-1 else ''
        if not omit_keys:
            print('\'{}\': \'{}\''.format(key, dictionary[key]), end=end_str)
        else:
            print('\'{}\''.format(dictionary[key]), end=end_str)
    print('}')


def find_common_path(str1, str2):
    """ Find common path between two paths (strings) """
    return os.path.commonprefix([str1, str2])


def test():
    pass


if __name__ == '__main__':
    test()
