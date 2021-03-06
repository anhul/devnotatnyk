"""
Module docstring must be here.

Next line with explanation.
"""
import re
import sys
import argparse
import os


MAX_HEADER_LEVEL = 6
INDENT_SPACES_NUM = 7

# List of headers which are ignored and not included into table of contents
# Headers in exception list are case insensitive
EXCEPTION_LIST = [
    "table of contents"
]

# Regular expression patterns
TOC_ITEM_PTRN = " *[-\*] +\[(.+)\]\(#(.+)\)\s*"


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Create table of contents "
                                                 "for the document written in Markdown")

    parser.add_argument("infile", help="md file to be processed")
    parser.add_argument("-l", "--level", type=int, default=6,
                        choices=range(1, MAX_HEADER_LEVEL+1),
                        help="minimum level of heading to be included")
    arg = parser.parse_args()
    if os.path.isfile(arg.infile):
        if not arg.infile.lower().endswith(".md"):
            print(".md file expected")
            sys.exit()
    else:
        print("File not found")
        sys.exit()

    return arg


def find_headings(file_name):

    with open(file_name, "r") as in_file:
        heading_level_lst = []
        for line in in_file:
            heading_level = extract_heading(line)
            if heading_level:
                heading_level_lst.append(heading_level)

    return heading_level_lst


def extract_heading(text_line):
    """
    Function docstring
    """
    match_pattern = "\s{{0,{}}}(#{{1,{}}})\s.*".format(INDENT_SPACES_NUM,
                                                       MAX_HEADER_LEVEL)
    match_result = re.match(match_pattern, text_line)
    if match_result is None:
        return ()

    lev = len(match_result.group(1))
    head = text_line.strip()
    head = head.strip(" #")
    if head.lower() in EXCEPTION_LIST:
        return()

    return (head, lev)


def heading_to_md_link(header):

    md_header = header.lower().replace(" ", "-")

    return "[{}](#{})".format(header, md_header)


def is_structure_valid(heading_level_lst):
    """
    Checks whether headings in the file are placed in an order which
    makes it possible to generate valid Table Of Contents

    :param heading_level_lst: list of tuples containing heading and level of
                              the heading
    :type list
    :return: True or False
    """
    _, base_level = heading_level_lst[0]

    for index, (heading, level) in enumerate(heading_level_lst):
        if level >= base_level:
            previous_level = level
            if index != 0:
                if level - previous_level > 1:
                    print("Subheading can be only one level less")
                    return False
        else:
            print("Proceeding heading level is greater than the first one")
            return False

    return True


def add_toc_to_file(file_name, heading_level_lst):
    print(file_name)
    print(os.path.dirname(file_name))
    print(os.path.split(file_name))
    print(os.path.abspath(file_name))
    print(os.path.basename(file_name))
    print(os.path.splitext(file_name))
    f_name, f_ext = os.path.splitext(file_name)

    with open(f_name + "_edit" + f_ext, "w") as updated_file:
        with open(file_name, "r") as original_file:

            updated_file.write("## Table Of Contents\n")

            _, base_level = heading_level_lst[0]
            for heading, level in heading_level_lst:
                subheading_indent = (level - base_level) * 2 * " "
                toc_item = subheading_indent + "- " + heading_to_md_link(heading) + "\n"
                print(toc_item)
                updated_file.write(toc_item)

            for line in original_file:
                if not is_toc_item(line):
                    updated_file.write(line)


def is_toc_item(line):

    match_result = re.match(TOC_ITEM_PTRN, line)
    if match_result is None:
        return False

    toc_item_part1 = match_result.group(1).lower().split()
    if "-".join(toc_item_part1) != match_result.group(2):
        return False

    return True


if __name__ == '__main__':

    args = parse_arguments()

    headings_and_levels = find_headings(args.infile)
    if not headings_and_levels:
        print("Headings have not been found")
        sys.exit()

    if not is_structure_valid(headings_and_levels):
        sys.exit()

    add_toc_to_file(args.infile, headings_and_levels)









