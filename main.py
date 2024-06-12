import re
def convert_lists(markdown_text):
    lines = markdown_text.split('\n')
    in_unordered_list = False
    in_ordered_list = False
    latex_lines = []

    for line in lines:
        unordered_match = re.match(r'^\s*-\s+(.*)', line)
        ordered_match = re.match(r'^\s*\d+\.\s+(.*)', line)

        if unordered_match:
            if not in_unordered_list:
                latex_lines.append('\\begin{itemize}')
                in_unordered_list = True
            latex_lines.append(f'\\item {unordered_match.group(1)}')
        elif ordered_match:
            if not in_ordered_list:
                latex_lines.append('\\begin{enumerate}')
                in_ordered_list = True
            latex_lines.append(f'\\item {ordered_match.group(1)}')
        else:
            if in_unordered_list:
                latex_lines.append('\\end{itemize}')
                in_unordered_list = False
            if in_ordered_list:
                latex_lines.append('\\end{enumerate}')
                in_ordered_list = False
            latex_lines.append(line)

    if in_unordered_list:
        latex_lines.append('\\end{itemize}')
    if in_ordered_list:
        latex_lines.append('\\end{enumerate}')

    return '\n'.join(latex_lines)
def markdown_to_latex(markdown_text):
    # Convert headers
    markdown_text = re.sub(r'##### (.*)', r'\\subparagraph{\1}', markdown_text)
    markdown_text = re.sub(r'#### (.*)', r'\\paragraph{\1}', markdown_text)
    markdown_text = re.sub(r'### (.*)', r'\\subsubsection{\1}', markdown_text)
    markdown_text = re.sub(r'## (.*)', r'\\subsection{\1}', markdown_text)
    markdown_text = re.sub(r'# (.*)', r'\\section{\1}', markdown_text)

    # Convert bold and italics
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', markdown_text)
    markdown_text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', markdown_text)

    # Convert images
    markdown_text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'\\begin{figure}[!h] \\centering \\includegraphics{\2} \\caption{\1} \\end{figure}', markdown_text)

    # Convert links
    markdown_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', markdown_text)

    # Convert lists
    markdown_text = convert_lists(markdown_text)

    # Convert inline code
    markdown_text = re.sub(r'`(.*?)`', r'\\texttt{\1}', markdown_text)

    markdown_text = "\\documentclass{article}\n\\usepackage{hyperref}\n\\usepackage{graphicx}\n\\begin{document}\n"+ markdown_text + "\n\\end{document}"

    return markdown_text


INPUT_FILE_NAME = "in.md"
OUTPUT_FILE_NAME = "out.tex"

input_file = open(INPUT_FILE_NAME, 'r')
output_file = open(OUTPUT_FILE_NAME, 'w')

markdown_text = input_file.read()
latex_text = markdown_to_latex(markdown_text) 
output_file.write(latex_text)