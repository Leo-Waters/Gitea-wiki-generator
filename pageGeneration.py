from DataModel import *
def generate_pages(root_node,working_directory):
    generate_page(root_node,working_directory)

def generate_page(node,working_directory):

    page_file_name=working_directory+node.get_file_name()

    file = open(page_file_name, "w")

    file.write(node.get_page_markup())

    file.close()

    #generate pages for child nodes
    for child in node.children:
        if(child.generates_page):
            generate_page(child,working_directory)