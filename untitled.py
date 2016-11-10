from flask import Flask, render_template, request
import work.isConsistant
app = Flask(__name__)

def matrix_to_int(matrix):
    final_matrix =[]
    try:
        for i in matrix.split('\r'):
            tmp = []
            for j in i.split(' '):
                tmp.append(int(j))
            final_matrix.append(tmp)
    except ValueError:
        return "Please input valid matrix again"
    return final_matrix

def matrix_to_str(matrix):
    final_matrix = []
    for k in matrix:
        tmp = []
        for i in k:
            tmp.append(str(i))
        final_matrix.append(tmp)
    return final_matrix

def convert_to_matrix(s):

    new_matrix = '\\begin{array}{'
    if len(s[0]) - 1 == 0:
        return '\\begin{array}{c}\end{array}'
    new_matrix += 'c' * (len(s[0]) - 1) + '|c}'
    for line in s[:len(s[0])]:
        for line_element in line[:len(line) - 1]:
            new_matrix += line_element + "&"
        new_matrix += str(line[-1]) + '\\\\\n\n'
    new_matrix += '\end{array}'

    return new_matrix

def get_main(matrix):
    final_matr = []
    vecror = []
    for line in matrix:
        final_matr.append(line[:len(line) - 1])
        vecror.append(line[-1])
    return final_matr, vecror


@app.route('/', methods=["GET", "POST"])
def get_index():
    if request.method == "POST":
        matrix = request.form['matrix']
        if type(matrix_to_int(matrix)) == str:
            return render_template('index.html', k=matrix_to_int(matrix), matrix=matrix, new_matrix=convert_to_matrix(matrix))
        matrix_1, vector = get_main(matrix_to_int(matrix))
        new_matrix = work.isConsistant.main(matrix_1, vector)
        message = new_matrix[1]
        new_matrix = convert_to_matrix(matrix_to_str(new_matrix[0]))
        if message == 'System is inconsistent' or message == 'Wrong size of matrix':
            return render_template('index.html', k = message, matrix = matrix, new_matrix = convert_to_matrix(matrix))
        return render_template('index.html', k = message, matrix = matrix, new_matrix = new_matrix)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run()