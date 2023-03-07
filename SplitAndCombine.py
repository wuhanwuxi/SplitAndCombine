import os
import sys


# target_size_list is in percent, sum should be 100%
def split(whole_filename, target_path, target_prefix, target_size_list):
    total_file_size = os.path.getsize(whole_filename)
    last_part_size = total_file_size
    print("split %s to %d parts to %s with prefix %s" % (whole_filename, len(target_size_list), target_path, target_prefix))
    # print("total size: %d\n" % total_file_size)
    file_size_list = []
    # calculate each file size
    for index in range(len(target_size_list)):
        if index != len(target_size_list) - 1:
            part_size = int(total_file_size * target_size_list[index]) // 100
            file_size_list.append(part_size)
            last_part_size -= part_size
        else:
            file_size_list.append(last_part_size)

    whole_file = open(whole_filename, "rb")
    for index in range(len(target_size_list)):
        # print("size %d: %d\n" % (index, file_size_list[index]))
        part_file = open(os.path.join(target_path, "%s_%d" % (target_prefix, index)), 'wb+')
        context = whole_file.read(file_size_list[index])
        part_file.write(context)
        part_file.close()
    whole_file.close()


def combine(folder, filename_list, target_filename):
    print("combine %d files into %s" % (len(filename_list), target_filename))
    target_file = open(target_filename, "wb+")
    for filename in filename_list:
        part_file = open(os.path.join(folder, filename), "rb")
        target_file.write(part_file.read())
    return


usage = """usages: 
SplitAndCombine split <full_file_name> <target_output_folder_path> <target_part_file_prefix> <percentage_size_list>
    split a file into several part files with different size calculated by percentage

SplitAndCombine combine <folder_path> <target_filename> <part_file_name_1> <part_file_name_2> ...

example
python SplitAndCombine.py split "C:\workspace\BigFile.tar" "C:\workspace" "part" 15 25 34 26
python SplitAndCombine.py combine "C:\workspace" "C:\workspace\BigFile.tar" "part_0" "part_1" "part_2" "part_3"
"""

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(usage)

    if sys.argv[1] == 'split':
        target_size_list = []
        for index in range(5, len(sys.argv)):
            target_size_list.append(int(sys.argv[index]))
        split(sys.argv[2], sys.argv[3], sys.argv[4], target_size_list)
    elif sys.argv[1] == 'combine':
        target_file_list = []
        for index in range(4, len(sys.argv)):
            target_file_list.append(sys.argv[index])
        combine(sys.argv[2], target_file_list, sys.argv[3])
    else:
        print(usage)
