
import re
import json
import argparse

# Important assumtion: No Tabs for lists and lists are always indented 4 spaces

def analyse(line):
    markdown_heading = re.search(r"#+ ", line)
    bold_heading = re.match(r"\*\*.+\*\*", line)
    list_item = re.search(r" *- ", line)
    
    if markdown_heading:
        hashtags = markdown_heading.group()[:-1]
        heading_level = len(hashtags)
        
    elif(bold_heading):
        heading_level = 4
    
    else:
        heading_level = 5

    if list_item:
        white_space = list_item.group()[:-2] # This whitespace counts the list-level
        # for example: "    - "[:-2] = "    "
        list_level = len(white_space) / 4
        if list_level % 1 != 0:
            raise ValueError("indentations for lists must be 4 spaces")
        
    return (heading_level, list_level)

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
    current_heading_level = 0
    current_list_level = 0

    with open("examples/simple.md", "r") as f: # with open(args.document, "r") as f:
        lines_in_file = True

        while(lines_in_file):
            line = f.readline()
            heading_level, list_level = analyse(line)

            print(line)
            line = fix_syntax(line)
            print(line)

            if line == "":
                lines_in_file = False

            elif line == "\n":
                pass

            else:
                node = {"text":line}

                if heading_level == 5: # Normal text
                    # TODO: This could be prettier
                    parent = newest_nodes[current_heading_level]

                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

                elif heading_level > current_heading_level: # Lower order heading
                    parent = newest_nodes[current_heading_level]
                    
                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

                    current_heading_level = heading_level
                    newest_nodes[heading_level] = node

                elif heading_level <= current_heading_level:
                    parent = newest_nodes[heading_level - 1]
                    
                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

                    newest_nodes[heading_level] = node
                    current_heading_level = heading_level



    print(json.dumps(document, indent=2))




if __name__ == "__main__":
    main()