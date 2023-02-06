import os

if __name__ == '__main__':
    test_directories = [x[0] for x in os.walk('testcases')]

    for directory_name in test_directories:
        os.chdir(directory_name)
        os.system('python3 ../compiler.py')
        os.chdir('../..')

        input_file = open(f'{directory_name}/input.txt', 'r')
        expected_output_file = open(f'{directory_name}/output.txt', 'r')

        current_dir_input = open(f'input.txt', 'w')
        current_dir_input.write(input_file.read())
        os.system('./tester_linux.out')
        output_file = open(f'output.txt', 'r')

        if output_file.read() == expected_output_file.read():
            print(f'{directory_name} passed.')
        else:
            print(f'{directory_name} failed.')


