import subprocess
from dotenv import load_dotenv
import logging
import datetime
import os

load_dotenv('docking_server.env')
qvina_root_path = os.getenv('QVINA_ROOT_PATH')
ligand_path = os.getenv('LIGAND_PATH')
receptor_path = os.getenv('RECEPTOR_PATH')
output_path = os.getenv('OUTPUT_PATH')
logger = logging.getLogger('django')
logger.setLevel(logging.ERROR)

def prep_configuration_file(request):
    receptor = request.data['receptor']
    center_x = request.data['center_x']
    center_y = request.data['center_y']
    center_z = request.data['center_z']
    size_x = request.data['size_x']
    size_y = request.data['size_y']
    size_z = request.data['size_z']
    exhaustiveness = request.data['exhaustiveness']
    ligand = request.data['ligand']

    config_file = open('conf.txt', 'r')
    lines = config_file.readlines()
    config_file.close()
    for index, line in enumerate(lines):
        if index == 0:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {receptor_path}{receptor}\n'
        if index == 1:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {center_x}\n'
        if index == 2:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {center_y}\n'
        if index == 3:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {center_z}\n'
        if index == 4:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {size_x}\n'
        if index == 5:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {size_y}\n'
        if index == 6:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {size_z}\n'
        if index == 7:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {exhaustiveness}\n'
        if index == 8:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {ligand_path}{ligand}\n'
        if index == 9:
            line_split = line.split()
            line = f'{line_split[0]} {line_split[1]} {output_path}{ligand}\n'
        lines[index] = line

    with open('conf.txt', 'w') as config_file:
        config_file.writelines(lines)

    sys_commands = ['qvina-w --config conf.txt']
    qvina_proc = subprocess.Popen(sys_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    qvina_output = qvina_proc.stdout.read()
    qvina_error = qvina_proc.stderr.read()
    if len(qvina_error) > 0:
        logger.error(f'''[{datetime.datetime.now()}]
                {qvina_error}
                ''')
