
import re
import json
import argparse
import node
import logging

# Important assumtion: No Tabs for lists and lists are always indented 4 spaces

def beget(parent, child): # or maybe better implemented as a method of some custom object? Would have to implement custom to-json function... 
    if "children" not in parent:
        parent["children"] = []

    parent["children"].add(child)

def analyse(line):
    logging.info(f"Analysing line: {line}")

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
        
        logging.info(f"list_level: {list_level}")

    else:
        level = 5
        
    logging.info(f"level: {level}")
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
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    # parser.add_argument("document", help="Convert the document from regular Markdown into Roam-readable Markdown")
    # parser.add_argument("-o -option", action="store_true", help="Some binary option, forgot what for")
    # TODO: Potential Options: destination file
    
    args = parser.parse_args()
    
    # if args.option: ...

    first_node = {
        "title":"Example title",
        "children": []
    }

    document = [first_node]

    newest_nodes = [first_node, None, None, None, None]
    list_nodes = [first_node, None, None, None, None, None, None, None]
    current_heading_level = 0
    current_list_level = 0

    with open("examples/simple.md", "r") as f: # with open(args.document, "r") as f:
        lines_in_file = True

        while(lines_in_file):
            line = f.readline()

            logging.info(f"line before syntax-fix: {line}")
            line = fix_syntax(line)
            logging.info(f"line after syntax-fix: {line}")

            level = analyse(line)

            if line == "":
                lines_in_file = False

            # elif line == "\n":
            #     pass

            # else:
            #     node = {"text":line}

                # if heading_level == 5: # lists & normal text
                #     # TODO: This could be prettier

                #     # HIER WEITER!! Listen einordnen

                #     if list_level == 0: # normal text
                #         parent = newest_nodes[current_heading_level]

                #         if "children" not in parent:
                #             parent["children"] = []
                #         parent["children"].append(node) # TODO: Simplify and generalize this child-adding in a function

                #         list_nodes[list_level] = node
                #         current_list_level = list_level

                #     elif list_level > current_list_level:
                #         parent = list_nodes[current_list_level]

                #         if "children" not in parent:
                #             parent["children"] = []
                #         parent["children"].append(node)

                #         current_list_level = list_level
                #         list_nodes[list_level] = node


                #     elif list_level < current_list_level:
                #         parent_level = current_list_level-1
                #         if parent_level == 0:
                #             parent = newest_nodes[current_heading_level]
                #         else:
                #             parent = list_nodes[parent_level] # TODO: Wenn ich auf 0 zurückgehe, parent außerhalb der Liste

                #         if "children" not in parent:
                #             parent["children"] = []
                #         parent["children"].append(node)

                #         list_nodes[current_list_level] = node
                        

                # elif heading_level > current_heading_level: # Lower order heading
                #     parent = newest_nodes[current_heading_level]
                    
                #     if "children" not in parent:
                #         parent["children"] = []
                #     parent["children"].append(node)

                #     current_heading_level = heading_level
                #     newest_nodes[heading_level] = node

                #     list_nodes[current_list_level] = node

                # elif heading_level <= current_heading_level:
                #     parent = newest_nodes[heading_level - 1]
                    
                #     if "children" not in parent:
                #         parent["children"] = []
                #     parent["children"].append(node)

                #     newest_nodes[heading_level] = node
                #     current_heading_level = heading_level



    # logging.info(json.dumps(document, indent=2))




if __name__ == "__main__":
    main()