import re

#MAX_HEADER_LEVEL = 6
INDENT_SPACES_NUM = 7

def find_headers(file_path):
    pass
#    with open (file_path, "r") as r_file:
#        for line in r_file:

def is_heading(text_line):

    match_pattern = "(\s{0,7})(#{1,6})\s.*"




def header_to_md_link(header):

    md_header = header.lower().replace(" ", "-")

    return "[{}](#{})".format(header, md_header)

out = header_to_md_link("Header of level 1")
print(out)
