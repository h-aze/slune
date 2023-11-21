from argparse import ArgumentParser
import subprocess
import sys

from slune.savers.csv import SaverCsv
from slune.loggers.default import LoggerDefault

def submit_job(sh_path, args):
    """
    Submits a job using the Bash script at sh_path,
    args is a list of strings containing the arguments to be passed to the Bash script.
    """
    try:
        # Run the Bash script using subprocess
        command = [sh_path] + args
        subprocess.run(['sbatch'] + command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running sbatch: {e}")

def sbatchit(script_path, template_path, searcher, cargs=[], slog=None):
    """
    Carries out hyper-parameter tuning by submitting a job for each set of hyper-parameters given by tune_control, 
    for each job runs the script stored at script_path with selected hyper-parameter values and the arguments given by cargs.
    Uses the template file with path template_path to guide the creation of the sbatch script for each job. 
    Args:
        - script_path (string): Path to the script (of the model) to be run for each job.

        - template_path (string): Path to the template file used to create the sbatch script for each job.

        - searcher (Searcher): Searcher object used to select hyper-parameter values for each job.

        - cargs (list): List of strings containing the arguments to be passed to the script for each job. 
                        Must be a list even if there is just one argument, default is empty list.

        - slog (Saver): Saver object (instantiated with a Logger object) used if we want to check if there are existing runs so we don't rerun.
                        Don't give a Saver object if you want to rerun all jobs!
    """
    if slog != None:
        searcher.check_existing_runs(slog)
    # Create sbatch script for each job
    for args in searcher:
        # Submit job
        submit_job(template_path, [script_path] + cargs + args)
    print("Submitted all jobs!")

def lsargs():
    """
    Returns the script name and a list of the arguments passed to the script.
    """
    args = sys.argv
    return args[0], args[1:]

def garg(args, arg_names):
    """
    Finds the argument with name arg_names (if its a string) in the list of arguments args_ls and returns its value.
    If arg_names is a list of strings then returns a list of the values of the argument names in arg_names.
    """
    def single_garg(arg_name):
        # Check if arg_name is a string
        if type(arg_name) != str:
            raise TypeError(f"arg_name must be a string, got {type(arg_name)}")
        # Find index of argument
        arg_index = [i for i, arg in enumerate(args) if arg_name in arg]
        # Return value error if argument not found
        if not arg_index:
            raise ValueError(f"Argument {arg_name} not found in arguments {args}")
        # Return value of argument
        if len(arg_index) > 1:
            raise ValueError(f"Multiple arguments with name {arg_name} found in arguments {args}")
        return args[arg_index[0]].split("=")[1]
    if type(arg_names) == list:
        return [single_garg(arg_name) for arg_name in arg_names]
    else:
        return single_garg(arg_names)

def get_csv_slog(params = None, root_dir='slune_results'):
    return SaverCsv(LoggerDefault(), params = params, root_dir=root_dir)