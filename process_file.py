
import re
import json
import argparse
import logging

from node import Node

# Important assumtion: No Tabs for lists and lists are always indented 4 spaces

def beget(parent, child): # or maybe better implemented as a method of some custom object? Would have to implement custom to-json function... 
    if "children" not in parent:
        parent["children"] = []

    parent["children"].add(child)

def analyse(line):
    logging.info(f"Analysing line: {line[:-1]}")

    markdown_heading = re.search(r"#+ ", line)
    bold_heading = re.match(r"\*\*.+\*\*", line)
    list_item = re.search(r" *- ", line)
    
    if markdown_heading:
        hashtags = markdown_heading.group()[:-1]
        level = len(hashtags)
        
    elif(bold_heading):
        level = 4
    
    elif list_item:
        white_space = list_item.group()[:-2] # This whitespace counts the list-level
        # for example: "    - "[:-2] = "    "
        if len(white_space) % 4 != 0:
            raise ValueError("indentations for lists must be 4 spaces")
        list_level = int(len(white_space) / 4)

        level = 5 + list_level # Lowest tier list items are same as normal text, then they increment on top
        
        logging.debug(f"list_level: {list_level}")

    else:
        level = 5
        
    logging.debug(f"level: {level}")
    return level

def fix_syntax(line):
    bullet_1 = re.compile(r" \+ ") #r"\s*+ "
    bullet_2 = re.compile(r" \* ") # r"\s*\* "

    # fix bullets:
    line = re.sub(bullet_1, " - ", line)
    line = re.sub(bullet_2, " - ", line)

    # fix bold and italics:
    # TODO: This creates a bug that messes up lines wit "*"
    line = re.sub(re.compile(r"\*"),  "_",  line)
    line = re.sub(re.compile(r"__"), "**", line)
    line = re.sub(re.compile(r"_"),  "__", line)

    return line


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # parser.add_argument("document", help="Convert the document from regular Markdown into Roam-readable Markdown")
    # parser.add_argument("-o -option", action="store_true", help="Some binary option, forgot what for")
    # TODO: Potential Options: destination file
    
    args = parser.parse_args()

    title_node = Node("example title", is_title=True)
    previous_node = title_node

    with open("examples/simple.md", "r") as f: # with open(args.document, "r") as f:
        lines_in_file = True

        while(lines_in_file):
            line = f.readline()

            # Fixing and analysing line for level
            line = fix_syntax(line)
            level = analyse(line)

            if line == "":
                lines_in_file = False

            elif line == "\n":
                pass

            else:
                current_node = Node(line, level)
                ancestry = previous_node.get_ancestry()

                for ancestor in ancestry:
                    if current_node.level > ancestor.level:
                        ancestor.beget(current_node)
                        break

                previous_node = current_node

        pretty_string = json.dumps(title_node.get_tree_below(), indent=2)
        logging.info(f"Final document structure:\n{pretty_string}")



    # logging.info(json.dumps(document, indent=2))




if __name__ == "__main__":
    main()