import os
import time
import timeit

solution_path = 'solution_Melnikov.py'
wikipedia_path = 'tests/wikipedia_sample.txt'
index_path = 'index.json'


def check():
    print('Start')
    if os.path.exists(index_path):
        os.remove(index_path)

    start = time.time()
    os.system(f'python {solution_path} build --dataset {wikipedia_path} --index {index_path}')
    end = time.time()
    if not os.path.exists(index_path):
        return 'Inverted index was not saved to disk'
    print(f'Index was prepared: {end-start}s')

    test_file_names = os.listdir('tests')
    test_input_data_files = sorted([
        filename
        for filename in test_file_names
        if filename.endswith('.in')
    ])

    for test_number, in_filename in enumerate(test_input_data_files, start=1):
        print(f'Run test #{test_number}')
        in_filename = f'tests/{in_filename}'
        ans_filename = in_filename.replace('.in', '.out')
        out_filename = 'temp.output'

        try:

            command = f'python {solution_path} query --index {index_path} --query_file {in_filename} > {out_filename}'
            start = time.time()
            os.system(command)
            end = time.time()
            print(f'Test Finished: {end - start}s')
        except Exception as e:
            return f'Problem while running your solution. {e}'

        with open(ans_filename, 'r', encoding='utf8') as f_ans:
            answer = f_ans.read().strip()

        with open(out_filename, 'r', encoding='utf8') as f_out:
            output = f_out.read().strip()

        if answer != output:
            feed_back = f'Failed test #{test_number}. Please try again!'
            feed_back += '\n\nYour output:\n' + output
            feed_back += '\n\nCorrect answer:\n' + answer
            return feed_back

    return 'Correct!'


if __name__ == '__main__':
    print(check())
