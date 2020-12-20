
import re
import json
import argparse
import logging

from node import Node


def analyse(line):
    logging.info(f"Analysing line: {line[:-1]}")

    markdown_heading = re.search(r"#+ ", line)
    bold_heading = re.match(r"\*\*.+\*\*", line)
    list_item = re.search(r" *- ", line)

    is_list_item = False
    
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

        is_list_item = True
        
        logging.debug(f"list_level: {list_level}")

    else:
        level = 5
        
    logging.debug(f"level: {level}")
    return level, is_list_item


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

def remove_bullet(line, level):
    return line[4*(level - 5) + 2:]


def main():
    logging.basicConfig(level=logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument("document", help="Convert this document from regular Markdown into Roam-readable JSON.")
    parser.add_argument("-o", "--output", help="Write output to this document.")
    # parser.add_argument("-o -option", action="store_true", help="Some binary option, forgot what for")
    # TODO: Potential Options: destination file
    
    args = parser.parse_args()

    title_node = Node(args.document, is_title=True)
    previous_node = title_node

    with open(args.document, "r") as f: # with open(args.document, "r") as f:
        lines_in_file = True

        while(lines_in_file):
            line = f.readline()

            # Fixing and analysing line for level
            line = fix_syntax(line)
            level, is_list_item = analyse(line)
            if is_list_item:
                line = remove_bullet(line, level)

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


    final_tree = title_node.get_tree_below()
    
    if args.output: # file for output given
        with open(args.output, "w") as f:
            json.dump(final_tree, f, indent=2)
    else: # just output to command line
        pretty_string = json.dumps(final_tree, indent=2)
        print(pretty_string)


if __name__ == "__main__":
    main()