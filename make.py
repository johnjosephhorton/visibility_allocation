
import os 
import sys 
sys.path.append('/home/john/')
import research_tools.create_paper as cp

if __name__ == '__main__':
    options, args = cp.parse_terminal_input() 
    input_dir = os.getcwd() 
    cp.main(input_dir, options.output_path, options.flush, options.get_data, options.run_r, options.run_py)
