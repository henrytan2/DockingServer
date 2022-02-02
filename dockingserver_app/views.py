from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .business.qvina import prep_configuration_file
import requests
import subprocess
import os

FASPR_PATH = os.getenv('FASPR_PATH')

class DockingAPI(APIView):
    def post(self, request):
        response = True
        # prep_configuration_file(request)
        pdb_name = request.data['pdb_name']
        pdb_api_url = f'https://files.rcsb.org/download/{pdb_name}.pdb'
        pdb_download_response = requests.get(pdb_api_url)
        faspr_input_dir = 'faspr_input.pdb'
        faspr_output_dir = 'faspr_output.pdb'
        if pdb_download_response.status_code == 200:
            pdb_content = pdb_download_response.content.decode('utf-8')
            with open(faspr_input_dir, 'w+') as faspr_input:
                faspr_input.write(pdb_content)
                faspr_input.close()
            faspr_commands = [f'"{FASPR_PATH}FASPR" -i {faspr_input_dir} -o {faspr_output_dir}']
            faspr_proc = subprocess.Popen(faspr_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            faspr_output = faspr_proc.stdout.read()
            faspr_err = faspr_proc.stderr.read()
        return Response(response)
