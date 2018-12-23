#MAX_HEADER_LEVEL = 6
#
#def markdown_contents(page_path):
#
#    with open (page_path, "r") as r_file:
def header_to_md_link(header):

    md_header = header.lower().replace(" ", "-")

    return "[{}](#{})".format(header, md_header)

out = header_to_md_link("Header of level 1")
print(out)
