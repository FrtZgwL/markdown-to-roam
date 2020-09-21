
import re
import json

# class Node(text):
#     def __init__(self, text):
#         self.text = text
#         self.level = 0

#     def __str__(self):
#         return self.text

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
    first_node = {
        "title":"Example title",
        "children": []
    }

    document = [first_node]

    newest_nodes = [first_node, None, None, None, None]
    current_level = 0

    with open("examples/simple.md", "r") as f:
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




# current_level = 0
# parents = {
#     0 = parent_0
#     1 = parent_1
#     2 = parent_2 
#     3 = parent_3
# }

# for line in line_gen:
#     # Process one line
#     if line is text:
#         parents[current_level].append(line)
#     elif line is heading:
#         if line.level > current_level:
#             # nest under and switch level
#             parents[lcurrent_level].append(line)
#             current_level = line.level
#             parents[line.level] = line
#         elif line.level <= current_level:
#             current_level = line.level - 1
#             parents[current_level].append(line)



