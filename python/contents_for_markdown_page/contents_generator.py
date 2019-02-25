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
# Headers i exception list are case insensitive
EXCEPTION_LIST = [
    "table of contents"
]


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Create table of contents "
                                                 "for the document written in Markdown")

    parser.add_argument("infile", help="md file to be processed")
    parser.add_argument("-l","--level", type=int, default=6,
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

    return(arg)


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


if __name__ == '__main__':

    args = parse_arguments()

    headings_and_levels = find_headings(args.infile)
    if headings_and_levels:
        base_level = headings_and_levels[0][1]

        for index, (heading, level) in enumerate(headings_and_levels):
            if level >= base_level:
                previous_level = level
                if index != 0:
                    if level - previous_level > 1:
                        print("Subheading can be only one level less")
                        sys.exit()

                subheading_indent = (level-base_level) * 2 * " "
                contents_item = subheading_indent + "- " + heading_to_md_link(heading)
                print(contents_item)
            else:
                print("Proceeding heading level is greater than the first one")
                sys.exit()

    else:
        print("Headings have not been found")

