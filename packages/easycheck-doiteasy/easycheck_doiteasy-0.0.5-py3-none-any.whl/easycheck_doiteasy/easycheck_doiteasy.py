import requests
import os
import logging
logging = logging.getLogger(__name__)



class MainMonitror():

    def __init__(self, token):
        """
        Constructor for the Monitor class.
        Parameters:
        token (str): The authentication token for the ETLCheck API.
        Attributes:
        token (str): The provided authentication token.
        domain (str): The default domain URL for API calls.
        """
        self.token = token
        self.domain = 'https://etlcheck.com'
        self.ejecution_line_ids = []


    def send_ejecution(self, name, duration, start_datetime, end_datetime, destination, total_register, successful):
        """
        Sends execution data to a specified API endpoint.

        Parameters:
        - name (str): The name of the execution.
        - duration (str): The duration of the execution in seconds.
        - start_datetime (str): The start datetime of the execution in ISO format (e.g. '2023-04-12T10:30:00Z').
        - end_datetime (str): The end datetime of the execution in ISO format (e.g. '2023-04-12T11:00:00Z').
        - destination (str): The destination of the execution.
        - total_register (int): The total number of registers processed during the execution.
        - successful (bool): Whether the execution was successful or not.
        Returns:
        - None
        Raises:
        - This method may raise an exception if the HTTP request to the API endpoint fails for any reason. In this case, an error message will be logged.
        """
        headers = {}
        domain = self.domain
        path = '/api/base/ejecution/send/'
        url = f'{domain}{path}'
        data = {
            'name': name,
            'duration': duration,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'destination': destination,
            'total_register': total_register,
            'successful': successful,
            'register_token': self.token
        }

        if len(self.ejecution_line_ids) > 0:
            data.update({'ejecution_line_ids': self.ejecution_line_ids})
        self.ejecution_line_ids = []
        try:
            requests.post(url, data=data, headers=headers)
        except Exception as e:
            logging.error(e)

    
    def send_subejecution(self, name, duration, start_datetime, end_datetime, total_register, successful):
        """
        Sends execution data to an ejecution line API endpoint.

        Parameters:
        - name (str): The name of the execution.
        - duration (str): The duration of the execution in seconds.
        - start_datetime (str): The start datetime of the execution in ISO format (e.g. '2023-04-12T10:30:00Z').
        - end_datetime (str): The end datetime of the execution in ISO format (e.g. '2023-04-12T11:00:00Z').
        - destination (str): The destination of the execution.
        - total_register (int): The total number of registers processed during the execution.
        - successful (bool): Whether the execution was successful or not.
        Returns:
        - None
        Raises:
        - This method may raise an exception if the HTTP request to the API endpoint fails for any reason. In this case, an error message will be logged.
        """    
        headers = {}
        domain = self.domain
        path = '/api/base/ejecution_line/send/'
        url = f'{domain}{path}'
        data = {
            'name': name,
            'duration': duration,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'total_register': total_register,
            'successful': successful,
            'register_token': self.token
        }
        try:
            res = requests.post(url, data=data, headers=headers)
            if res.status_code == 200:
                self.ejecution_line_ids.append(res['id'])
        except Exception as e:
            logging.error(e)



    def update_logs_directories(self, logs_dir):

        headers = {}
        domain = self.domain
        path = '/api/base/logs_directory/register/'
        url = f'{domain}{path}'
        directories = [element for element in os.listdir(logs_dir) if os.path.isdir(f'{logs_dir}/{element}')]
        ruta_absoluta = os.path.abspath(__file__)
        carpeta_raiz = os.path.basename(os.path.dirname(ruta_absoluta))
        data = {
            'origin': carpeta_raiz,
            'directories': directories,
            'register_token': self.token
        }
        res = requests.post(url, data=data, headers=headers)

    def register_file(self, log_file):

        headers = {}
        domain = self.domain
        path = '/api/base/logs_file/register/'
        file_size = os.path.getsize(log_file)/1024
        log_dir = log_file.split('/')[-2]
        log_filename = log_file.split('/')[-1]
        data = {
            'name': log_filename,
            'log_directory': log_dir,
            'file_size': file_size,
            'with_errors': False,
            'register_token': self.token
        }
        url = f'{domain}{path}'
        res = requests.post(url, data=data, headers=headers)