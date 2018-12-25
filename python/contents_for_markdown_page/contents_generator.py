import re

MAX_HEADER_LEVEL = 6
INDENT_SPACES_NUM = 7

def find_headings(file_path):

    with open (file_path, "r") as in_file:
        for line in in_file:
            level = heading_level(line)
            if level is not None:
                heading = extract_heading(line)
                print(heading)
                print(heading_to_md_link(heading))


def heading_level(text_line):

    match_pattern = "\s{{0,{}}}(#{{1,{}}})\s.*".format(
                                      INDENT_SPACES_NUM,
                                      MAX_HEADER_LEVEL)

    match_result = re.match(match_pattern,text_line)

    if match_result is not None:
        level = len(match_result.group(1))
    else:
        level = None

    return level

def extract_heading(text_line):

    heading = text_line.strip()
    heading = heading.strip(" #")
    return heading


def heading_to_md_link(header):

    md_header = header.lower().replace(" ", "-")

    return "[{}](#{})".format(header, md_header)
