import re

MAX_HEADER_LEVEL = 6
INDENT_SPACES_NUM = 7


def find_headings(file_path):

    with open(file_path, "r") as in_file:
        heading_level_lst = []
        for line in in_file:
            heading_level = extract_heading(line)
            if heading_level:
                heading_level_lst.append(heading_level)

    return heading_level_lst


def extract_heading(text_line):
    """

    :rtype: tuple
    """
    match_pattern = "\s{{0,{}}}(#{{1,{}}})\s.*".format(
                                      INDENT_SPACES_NUM,
                                      MAX_HEADER_LEVEL)

    match_result = re.match(match_pattern, text_line)

    if match_result is None:
        return ()
        
    level = len(match_result.group(1))
    heading = text_line.strip()
    heading = heading.strip(" #")
    
    return (heading, level)


def heading_to_md_link(header):

    md_header = header.lower().replace(" ", "-")

    return "[{}](#{})".format(header, md_header)


if __name__ == '__main__':

    file_path = "test_page.md"
    headings_and_levels = find_headings(file_path)
    if headings_and_levels:
        base_level = headings_and_levels[0][1]

        for index in range(len(headings_and_levels)):
            heading, level = headings_and_levels[index]
            if index != 0:
                pass
            subheading_indent = (level-base_level) * 2 * " "
            contents_item = subheading_indent +  "- " + heading_to_md_link(heading)
            print(contents_item)

    else:
        print("Headings have not been found")
