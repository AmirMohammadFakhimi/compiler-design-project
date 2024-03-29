import os

import code_gen
import parser
import subprocess

import compiler
import parser
import scanner

# just for LINUX
if __name__ == '__main__':
    # test_directories = os.listdir('testcases')
    test_directories = []

    for i in range(1, 10):
        test_directories.append(f'T{i}')

    for directory_name in test_directories:
        if directory_name.startswith('.'):
            continue

        input_file = open(f'testcases/{directory_name}/input.txt', 'r')
        expected_output_file = open(f'testcases/{directory_name}/expected.txt', 'r')
        expected_output = expected_output_file.read().strip()
        expected_output_file.close()

        current_dir_input = open(f'input.txt', 'w')
        current_dir_input.write(input_file.read())
        current_dir_input.close()
        input_file.close()

        compiler.reset_compiler()
        scanner.initial_scanner()
        parser.run_parser()
        compiler.create_pb_file()

        output = subprocess.Popen('./tester_linux.out', stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
        wants_output = ""
        for line in output.splitlines():
            if line.startswith('PRINT'):
                wants_output += str(line) + '\n'
        wants_output = wants_output.strip()

        if wants_output == expected_output:
            print(f'{directory_name} passed.')
        else:
            print(f'{directory_name} failed.')


