def If_Elsif_Insertion(vector, filepath):
    """
    This function adds the terms 'If' and 'Elsif' in the appropriate places.
    Input Parameters:
        vector = Number of vertical bars (|) in each line of the file;
        filepath = Name of the file where the adjustments will be made.
    """
    groups = [list(range(len(vector)))] 
    while groups: 
        current_group = groups.pop(0) 
        subgroups_to_analyze = []    
        for i in current_group: 
            value = vector[i] 
            for j in current_group:
                if i != j: 
                    if vector[j] == value: 
                        with open(filepath, 'r') as file: 
                            lines = file.readlines()
                        lines[j] = lines[j].replace("---", "if") 
                        lines[i] = lines[i].replace("---", "elsif") 
                        with open(filepath, 'w') as file: 
                            file.write(''.join(lines)) 
                        subgroup1 = current_group[current_group.index(j) + 1:current_group.index(i)]
                        subgroup2 = current_group[current_group.index(i) + 1:]
                        subgroups_to_analyze.extend([subgroup1, subgroup2])
                        break
                    else:
                        break
        groups.extend(subgroups_to_analyze)
        
def Decreased_indentation(filepath):
    """
    This function analyzes line indentations to identify conditional structure 
    blocks.
    Input parameters:
        filepath = Name of the file where the reading will be performed.
    Output parameters:
        lines_with_smaller_indentation = Vector containing indices of lines that
        have an indentation smaller than the previous line.

    """
    line_with_smaller_indentation = []
    with open(filepath, 'r') as file: 
        lines = file.readlines()
    for i in range(1, len(lines)):
        current_line = lines[i]
        previous_line = lines[i - 1]
        current_indentation = len(current_line) - len(current_line.lstrip())
        previous_indentation = len(previous_line) - len(previous_line.lstrip())     
        if current_indentation == 0:
            pass
        elif current_indentation < previous_indentation:
            line_with_smaller_indentation.append(i)
    return line_with_smaller_indentation

def Insertion_terms(filepath, index):
    """
    This function identifies the position where the 'end_if' term should be 
    placed.
    Input parameters:
        filepath = Name of the file where the reading will be performed.
        index = Vector that stores lines with indentation smaller than the 
        previous line.
    Output parameters:
        lines_with_smaller_indices = Vector that stores the indices of lines
        where the term "end_if" should be added;
        indentation = Vector that stores the number of spaces at the beginning 
        of lines stored in the index vector that have lines below with smaller
        indentation;
        tabulation = Vector that stores the number of spaces at the beginning of
        lines stored in the index vector that do not have lines below with
        smaller indentation.

    """
    
    with open(filepath, 'r') as original_file:
        lines = original_file.readlines()
    lines_with_additions = []; lines_with_smaller_indices = []; indentation = []
    tabulation = []
    for i, line in enumerate(lines):
        lines_with_additions.append(line)
        if i in index: 
            indentationlinei = len(lines[i]) - len(lines[i].lstrip())
            j = i + 1 
            while j < len(lines): 
                analyzed_line= lines[j]
                analyzed_indentation = len(analyzed_line) - len(analyzed_line.lstrip())
                lines_limit = len(lines) - 1
                if analyzed_indentation < indentationlinei:
                    lines_with_smaller_indices.append(j)
                    indentation.append(indentationlinei)
                    break
                elif j == lines_limit:
                    tabulation.append(len(lines[i]) - len(lines[i].lstrip()))
                    break
                else:
                    j += 1 
    return lines_with_smaller_indices, indentation, tabulation