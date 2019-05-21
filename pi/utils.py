import sys
import os
import heapq
import gzip
import time


def safe_remove(fname):
    """Remove a file if it exist"""
    if not fname:
        return False

    if os.path.exists(fname):
        os.remove(fname)

    return True


def safe_makedir(dname):
    """Make a directory if it doesn't exist, handling concurrent race conditions.
    """
    if not dname:
        return dname

    num_tries = 0
    max_tries = 5
    while not os.path.exists(dname):
        # we could get an error here if multiple processes are creating
        # the directory at the same time. Grr, concurrency.
        try:
            os.makedirs(dname)
        except OSError:
            if num_tries > max_tries:
                raise

            num_tries += 1
            time.sleep(2)

    return dname


def file_exists(fname):
    """Check if a file exists and is non-empty.
    """
    try:
        return fname and os.path.exists(fname) and os.path.getsize(fname) > 0
    except OSError:
        return False


def get_last_modification_file(dirname):
    """Find the last modification file in a directory and return it."""

    file_name_list = os.listdir(dirname)
    file_name_list.sort(key=lambda fn: os.path.getmtime(os.path.join(dirname, fn)))

    if file_name_list:

        # return the last modification file path of dirname
        return os.path.join(dirname, file_name_list[-1])
    else:
        # dirname is empty
        return ""


def _expanded_open(path, mode):
    try:
        return open(path, mode)
    except IOError:
        return open(os.path.expanduser(path), mode)


def Open(file_name, mode, compress_level=9):
    """
    Function that allows transparent usage of dictzip, gzip and
    ordinary files
    """
    if file_name.endswith(".gz") or file_name.endswith(".GZ"):
        file_dir = os.path.dirname(file_name)
        if not os.path.exists(file_dir):
            file_name = os.path.expanduser(file_name)

        return gzip.GzipFile(file_name, mode, compress_level)
    else:
        return _expanded_open(file_name, mode)


class FileForQueueing(object):
    """
    """

    def __init__(self, the_file, line, is_del_raw_file=False):
        """
        Store the file, and init current value
        """
        self.the_file = the_file
        self.finishedReadingFile = False
        self.is_del_raw_file = is_del_raw_file
        self.heap = []

        line = line
        cols = line.strip().split()
        chrom = cols[0]

        # Where possible, convert chromosome names into
        # integers for sorting. If not possible, use
        # original names.
        try:
            chrom = int(chrom.upper().strip("CHR"))
        except Exception:
            pass

        pos = int(cols[1])
        heapq.heappush(self.heap, (chrom, pos, line))

        while not self.finishedReadingFile and len(self.heap) < 100:

            try:
                line = self.the_file.next()
                cols = line.strip().split()
                chrom = cols[0]

                try:
                    chrom = int(chrom.upper().strip("CHR"))
                except Exception:
                    pass

                pos = int(cols[1])
            except StopIteration:
                self.finishedReadingFile = True
                break

            heapq.heappush(self.heap, (chrom, pos, line))

        # take the top line
        self.chrom, self.pos, self.line = heapq.heappop(self.heap)

    def __cmp__(self, other):
        """
        Comparison function. Utilises the comparison function defined in
        the AlignedRead class.
        """
        def _comparision(a, b):
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return 0

        return _comparision(self.chrom, other.chrom) or _comparision(self.pos, other.pos)

    def __del__(self):
        """
        Destructor
        """
        self.the_file.close()

        if self.is_del_raw_file:
            os.remove(self.the_file.name)

    def next(self):
        """
        Increment the iterator and yield the new value. Also, store the
        current value for use in the comparison function.
        """
        if not self.finishedReadingFile:

            try:
                line = self.the_file.next()
                cols = line.strip().split()
                chrom = cols[0]

                # Where possible, convert chromosome names into
                # integers for sorting. If not possible, use
                # original names.
                try:
                    chrom = int(chrom.upper().strip("CHR"))
                except Exception:
                    pass

                pos = int(cols[1])
                heapq.heappush(self.heap, (chrom, pos, line))

            except StopIteration:
                self.finishedReadingFile = True

        if len(self.heap) != 0:
            # Now take the top line
            self.chrom, self.pos, self.line = heapq.heappop(self.heap)
        else:
            raise StopIteration


def merge_files(temp_file_names, final_file_name, is_del_raw_file=False):
    """
    Merging output VCF/CVG files into a final big one
    log.info("Merging output VCF/CVG file(s) into final file %s" %(final_file_name))
    """

    # Final output file
    if final_file_name == "-":
        output_file = sys.stdout
    else:
        output_file = Open(final_file_name, 'wb')

    the_heap = []

    # Initialise queue
    for index, file_name in enumerate(temp_file_names):
        the_file = Open(file_name, 'rb')

        for line in the_file:

            # End of this file
            if line[0] == "#":
                if index == 0:
                    output_file.write(line)
            else:
                the_file_for_queueing = FileForQueueing(the_file, line, is_del_raw_file=is_del_raw_file)
                heapq.heappush(the_heap, the_file_for_queueing)
                break

        # If there are no calls in the temp file, we still want to
        # remove it.
        else:
            the_file.close()

            if is_del_raw_file:
                os.remove(file_name)

    # Merge-sort the output using a priority queue
    while len(the_heap) != 0:

        # Get file from heap in right order
        next_file = heapq.heappop(the_heap)
        output_file.write(next_file.line)

        # Put file back on heap
        try:
            next_file.next()
            heapq.heappush(the_heap, next_file)
        except StopIteration:
            continue

    # Close final output file
    if final_file_name != "-":
        output_file.close()

    return
