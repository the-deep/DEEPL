import os
import time


class Resource:
    """
    Any resource that gives/writes raw data. Eg: file, s3, other web links
    """
    FILE = 1 << 0
    WEB = 1 << 1
    DIRECTORY = 1 << 2
    ENVIRONMENT = 1 << 3
    FILE_AND_ENVIRONMENT = FILE | ENVIRONMENT
    WEB_AND_ENVIRONMENT = WEB | ENVIRONMENT
    DIRECTORY_AND_ENVIRONMENT = DIRECTORY | ENVIRONMENT

    def __init__(self, location, type=FILE):
        """
        @location: directory or web location
        @name: filename
        """
        self.location = location
        self.type = type
        self.validate()

    def validate(self):
        if self.is_environ():
            if not os.environ.get(self.location):
                raise Exception('Please set the environment variable {}'.
                                format(self.location))
        if self.is_file():
            self.__validate_file_path()
        if self.is_directory():
            self.__validate_directory()
        elif self.is_web():
            self.__validate_web_path()

    def __validate_file_path(self, check_file_exists=False):
        check_path = self.get_resource_location()
        if not check_file_exists:
            check_path = os.path.dirname(check_path)
        if not os.path.exists(check_path):
            raise Exception('No such location: {}'.format(check_path))

    def __validate_web_path(self):
        raise Exception('Validation for web is not yet implemented')

    def __validate_directory(self):
        to_check = self.get_resource_location()
        if not os.path.isdir(to_check):
            raise Exception ('No such location: {}'.format(to_check))

    def get_data(self):
        """Return plain data after reading from the resource"""
        if self.is_file():
            # To read file, it should exist
            self.__validate_file_path(check_file_exists=True)
            return self.__get_file_data()
        elif self.is_web():
            return self.get_web_data()
        else:
            raise Exception(
                "Invalid resource type. Should be either file or web"
            )

    def write_data(self, data):
        if self.is_file():
            self.__write_data_file(data)
        elif self.is_web():
            self.__write_data_web(data)
        else:
            raise Exception('Invalid type')

    def __write_data_file(self, data):
        location = self.get_resource_location()
        with open(location, 'w') as f:
            f.write(data)

    def __write_data_web(self, data):
        raise Exception('__write_data_web is not implemented')

    def __get_file_data(self, fullpath=None):
        fullpath = self.get_resource_location()
        with open(fullpath) as f:
            return f.read()

    def get_resource_location(self):
        """Get location from env if set else self.location"""
        if self.is_environ():
            try:
                return os.environ[self.location]
            except Exception as e:
                # TODO: something meaningful and useful
                raise e
        else:
            return self.location

    def is_environ(self):
        return self.type & Resource.ENVIRONMENT != 0

    def is_file(self):
        return self.type & Resource.FILE != 0

    def is_directory(self):
        return self.type & Resource.DIRECTORY != 0

    def is_web(self):
        return self.type & Resource.WEB != 0


def merge_lists(la, lb, key=lambda x: x):
    """
    Merge two sorted lists
    @la: first list
    @lb: second list (order doesn't matter though)
    @key: comparison key
    """
    merged = []
    lena, lenb = len(la), len(lb)
    lb_ind, la_ind = 0, 0
    while lb_ind < lenb:
        bval = key(lb[lb_ind])
        while la_ind < lena and key(la[la_ind]) <= bval:
            merged.append(la[la_ind])
            la_ind += 1
        merged.append(lb[lb_ind])
        lb_ind += 1
    # if some left in a
    merged.extend(la[la_ind:])
    return merged


def timeit(func_to_be_tracked):
    """Decorator to calculate elapsed time for a function"""
    def wrapper(*args, **kwargs):
        start = time.time()
        func_to_be_tracked(*args, **kwargs)
        end = time.time()
        fname = func_to_be_tracked.__name__
        print("The function '{}' took {}ms.".format(fname, end - start))
    return wrapper


def compress_sparse_vector(sparse_vec):
    """Given a sparse vector [0., 0., ..., 0.213, ... ],
    return its compressed form [(index, nonzero_value), ...,
        (last_index, last_value)]. Returning last index and value will store
    the information about original sparse vector length.
    """
    compressed = []
    size = len(sparse_vec)
    for i, x in enumerate(sparse_vec[:-1]):
        if x:
            compressed.append((i, x))
    # append the last one
    compressed.append((size - 1, sparse_vec[-1]))
    return compressed


def get_env_path_or_exception(env_var):
    indicespath = os.environ.get(env_var)
    if not indicespath or not os.path.isdir(indicespath):
        raise Exception(
            "Please set the environment variable {} to the \
directory where the index files are stored.".format(env_var)
        )
    return indicespath


if __name__ == '__main__':
    import random
    # do test if merge works fine or not
    for x in range(50000):
        randlen1 = random.randrange(5, 50)
        randlen2 = random.randrange(5, 50)
        randlist1 = [random.randrange(1000) for _ in range(randlen1)]
        randlist2 = [random.randrange(1000) for _ in range(randlen2)]
        merged = randlist1 + randlist2
        assert merge_lists(sorted(randlist1), sorted(randlist2)) ==\
            sorted(merged), "Merging sorted and whole sorted should be same"
