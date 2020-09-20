


current_level = 0
parents = {
    0 = parent_0
    1 = parent_1
    2 = parent_2 
    3 = parent_3
}

for line in line_gen:
    # Process one line
    if line is text:
        parents[current_level].add(line)
    elif line is heading:
        if line.level > current_level:
            # nest under and switch level
            parents[lcurrent_level].add(line)
            current_level = line.level
            parents[line.level] = line
        elif line.level <= current_level:
            current_level = line.level - 1
            parents[current_level].add(line)



