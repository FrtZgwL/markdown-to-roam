
import re
import json
import argparse

def analyse(line):
    markdown_heading = re.search(r"#+ ", line)
    bold_heading = re.match(r"\*\*.+\*\*", line)
    
    if markdown_heading:
        hashtags = markdown_heading.group()[:-1]
        level = len(hashtags)
        
    elif(bold_heading):
        level = 4
    
    else:
        level = 5
        
    return (line, level)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("document", help="Convert the document from regular Markdown into Roam-readable Markdown")
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
    current_level = 0

    with open("examples/simple.md", "r") as f: # with open(args.document, "r") as f:
        lines_in_file = True

        while(lines_in_file):
            line, level = analyse(f.readline())

            if line == "":
                lines_in_file = False

            elif line == "\n":
                pass

            else:
                node = {"text":line}

                if level == 5: # Normal text
                    parent = newest_nodes[current_level]

                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

                elif level > current_level: # Lower order heading
                    parent = newest_nodes[current_level]
                    
                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

                    current_level = level
                    newest_nodes[level] = node

                elif level <= current_level:
                    parent = newest_nodes[level - 1]
                    
                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

                    newest_nodes[level] = node
                    current_level = level

    print(json.dumps(document, indent=2))




if __name__ == "__main__":
    main()