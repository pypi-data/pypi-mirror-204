#  """
#    Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
import logging
import os.path
import PySimpleGUI as Sg
import datetime
import numpy as np
import csv
import shutil

from wiliot_core import WiliotDir
from wiliot_testers.tester_utils import upload_to_cloud_api


MAX_FILE_SIZE = 15 * 10**6  # 15 Mb


def get_files_path():
    """
    opens GUI for selecting a file and returns it
    """
    # Define the window's contents
    layout = [[Sg.Text('Choose run data file that you want to upload:'), Sg.Input(key="run_data_file"),
               Sg.FileBrowse()],
              [Sg.Text('Choose packets data file that you want to upload:'), Sg.Input(key="tags_data_file"),
               Sg.FileBrowse()],
              [Sg.Text('environment:'),
               Sg.InputCombo(('prod', 'test'), default_value="prod", key='env')],
              [Sg.Text('Tester type:'),
               Sg.InputCombo(('offline-tester', 'sample-test'), default_value="offline-tester", key='tester_type')],
              [Sg.Button('Select')]]

    # Create the window
    window = Sg.Window('upload to Cloud', layout)

    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == 'Select' and (values['run_data_file'] != '' or values['tags_data_file'] != ''):
        window.close()
        return values
    else:
        window.close()
        return None


def create_summary_message(is_upload=True, data_folder_name=''):
    """
    summary log
    :param is_upload:
    :type is_upload: bool or None
    :return:
    :rtype:
    @param data_folder_name:
    @type data_folder_name:  str
    """
    sum_msg_prefix = '\n\n\n***********************************************\n'
    sum_msg_suffix = '***********************************************\n'
    sum_msg_upload = f'********* UPLOAD: files were uploaded from {data_folder_name} *********\n'
    sum_msg = sum_msg_prefix
    if is_upload is not None:
        sum_msg += sum_msg_upload
        if not is_upload:
            sum_msg = sum_msg.replace('were', 'were NOT')
    sum_msg += sum_msg_suffix
    return sum_msg


class UploadTestersData(object):
    def __init__(self):
        """
        This function check the selected user files and upload them to the cloud.
        If the file exceed the size limit it split it
        """
        self.values = None
        self.logger = None

        self.get_files_path()
        if self.values is None:
            print('user exited the program')
            return

        self.set_logging()
        file_status = self.check_files()
        if not file_status:
            return

        # check file size:
        self.all_run_names = [self.values['run_data_file']]
        self.all_packets_names = [self.values['tags_data_file']]
        self.tester_type = self.values['tester_type']
        file_size = os.stat(self.values['tags_data_file']).st_size
        if file_size > MAX_FILE_SIZE and 'offline' in self.tester_type:
            self.split_large_file(run_data=self.values['run_data_file'], packet_data=self.values['tags_data_file'],
                                  size=file_size)

    def get_files_path(self):
        """
            opens GUI for selecting a file and returns it
            """
        # Define the window's contents
        layout = [[Sg.Text('Choose run data file that you want to upload:'), Sg.Input(key="run_data_file"),
                   Sg.FileBrowse()],
                  [Sg.Text('Choose packets data file that you want to upload:'), Sg.Input(key="tags_data_file"),
                   Sg.FileBrowse()],
                  [Sg.Text('environment:'),
                   Sg.InputCombo(('prod', 'test'), default_value="prod", key='env')],
                  [Sg.Text('owner id:'),
                   Sg.Input('wiliot-ops', key='owner_id')],
                  [Sg.Text('Tester type:'),
                   Sg.InputCombo(('offline-tester', 'sample-test'), default_value="offline-tester", key='tester_type')],
                  [Sg.Button('Select')]]

        # Create the window
        window = Sg.Window('upload to Cloud', layout)

        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == 'Select' and (values['run_data_file'] != '' or values['tags_data_file'] != ''):
            window.close()
            self.values = values
        else:
            window.close()
            self.values = None

    def set_logging(self):

        # set log path
        if os.path.isfile(self.values['run_data_file']):
            files_dir = os.path.dirname(self.values['run_data_file'])
        elif os.path.isfile(self.values['tags_data_file']):
            files_dir = os.path.dirname(self.values['run_data_file'])
        else:
            env_dir = WiliotDir()
            files_dir = os.path.join(env_dir.get_tester_dir("upload_to_cloud"), "logs")
            if not os.path.isdir(files_dir):
                env_dir.create_dir(files_dir)
        log_path = os.path.join(files_dir,
                                datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'upload_to_cloud.log')

        # set logger:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S'))
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S'))
        stream_handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('Manual Upload')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        self.logger = logger

    def check_files(self):
        if not os.path.isfile(self.values['run_data_file']) or not self.values['run_data_file'].endswith('.csv'):
            self.logger.warning('UPLOAD: run_data file format is not csv, please insert a csv file')
            self.logger.info(create_summary_message(False))
            return False
        if not os.path.isfile(self.values['tags_data_file']) or not self.values['tags_data_file'].endswith('.csv'):
            self.logger.warning('UPLOAD: tags_data file format is not csv, please insert a csv file')
            self.logger.info(create_summary_message(False))
            return False
        return True

    def split_large_file(self, run_data, packet_data, size):

        def get_new_path_name(original_path, k, total, file_str):
            new_folder_name = os.path.dirname(original_path) + f'_{k}_out_of_{n_splits}'
            new_file_name = os.path.basename(original_path).replace(f'@{file_str}_data.csv',
                                                                    f'_{k}_out_of_{total}@{file_str}_data.csv')
            if not os.path.isdir(new_folder_name):
                os.makedirs(new_folder_name)
            return os.path.join(new_folder_name, new_file_name)

        n_splits = int(np.ceil(size / MAX_FILE_SIZE))
        part = 1
        all_packets_path = []
        all_run_path = []
        # read
        f_read = open(packet_data, 'r')
        reader = csv.DictReader(f_read, delimiter=',')
        col_names = reader.fieldnames
        # write first file
        new_packet_path = get_new_path_name(packet_data, part, n_splits, 'packets')
        all_packets_path.append(new_packet_path)
        f_write = open(new_packet_path, 'w', newline='')
        writer = csv.DictWriter(f_write, fieldnames=col_names)
        writer.writeheader()
        last_loc = 0
        for i, row in enumerate(reader):
            if os.stat(new_packet_path).st_size < MAX_FILE_SIZE or int(row['tag_run_location']) == last_loc:
                writer.writerow(row)
                last_loc = int(row['tag_run_location'])
            else:  # we need to split the file
                f_write.close()
                part += 1
                new_packet_path = get_new_path_name(packet_data, part, n_splits, 'packets')
                all_packets_path.append(new_packet_path)
                f_write = open(new_packet_path, 'w', newline='')
                writer = csv.DictWriter(f_write, fieldnames=col_names)
                writer.writeheader()
                writer.writerow(row)
                last_loc = int(row['tag_run_location'])
        f_write.close()
        if part > n_splits:
            self.logger.info(
                f'Since the file cannot be split in the middle of location data, a mismatch happened and '
                f'the number of parts is bigger than the number of split (i.e you will have a file with '
                f'the suufix {part}_out_of{n_splits}')
        # duplicate run data:
        for i in range(part):
            new_run_path = get_new_path_name(run_data, i+1, n_splits, 'run')
            all_run_path.append(new_run_path)
            shutil.copyfile(run_data, new_run_path)

        self.all_run_names = all_run_path
        self.all_packets_names = all_packets_path

    def upload_to_cloud(self):
        if self.tester_type == 'offline-tester':
            self.tester_type = 'offline-test'

        all_status = []
        for run_path, packet_path in zip(self.all_run_names, self.all_packets_names):
            try:
                upload_success = upload_to_cloud_api(batch_name=os.path.dirname(run_path),
                                                     tester_type=self.tester_type,
                                                     run_data_csv_name=run_path,
                                                     tags_data_csv_name=packet_path,
                                                     to_logging=True, env=self.values['env'],
                                                     is_batch_name_inside_logs_folder=False,
                                                     logger_=self.logger.name, packets_instead_tags=True,
                                                     owner_id=self.values['owner_id'],
                                                     is_path=True)
            except Exception as e:
                self.logger.warning(f'UPLOAD: during upload_to_cloud_api an error occurred: {e}')
                upload_success = False

            self.logger.info(
                create_summary_message(is_upload=upload_success, data_folder_name=os.path.dirname(run_path)))
            all_status.append(upload_success)
        return all(all_status)


if __name__ == '__main__':
    # upload to cloud
    upload_obj = UploadTestersData()
    status = upload_obj.upload_to_cloud()

    print(f"done with status {status}")
