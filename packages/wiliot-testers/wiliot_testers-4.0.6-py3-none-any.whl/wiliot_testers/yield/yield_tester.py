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
"""
Calculating Yield fraction by the following steps (with elaboration):
1)Counting the unique advas in AdvaProcess class
2)Counting number of tags in CountThread
3)Creating two threads in MultiThreadingCalculation in order to run AdvaProcess instance and CountThread instance
at the same time
4)Calculating the Yield fraction according to the results we got from the instances
5)Creating two threads in MainWindow class in order to calculate the fraction by MultiThreadingCalculation instance
and to run the GUI function (open_session) at the same time.
"""

from wiliot_core import *
import csv
import serial.tools.list_ports
import PySimpleGUI as sg
from configs.inlay_data import *
from wiliot_testers.tester_utils import *
from wiliot_testers.utils.get_version import *
import serial


inlay_types_dict = {item.name: item.value for item in InlayTypes}
today = datetime.date.today()
formatted_today = today.strftime("%Y%m%d")  # without -
formatted_date = today.strftime("%Y-%m-%d")
current_time = datetime.datetime.now()
cur_time_formatted = current_time.strftime("%I%M%S")  # without :
time_formatted = current_time.strftime("%I:%M:%S")


class AdvaProcess(threading.Thread):
    """
    Counting the number of unique advas
    """

    def __init__(self, stop_event, received_channel, time_profile_val, energy_pattern_val):
        threading.Thread.__init__(self, daemon=True)
        self.gw_instance = WiliotGateway(auto_connect=True)  # gw object, in order to connect with gw
        self.all_tags = TagCollection()  # tagcollection object, in order to check packets in prepared list
        self.gw_init()
        self.stop = stop_event
        self.received_channel = received_channel
        self.time_profile_val = time_profile_val
        self.energy_pattern_val = energy_pattern_val
        self.gw_reset_config()
        self.number_of_unq_adva = 0

    def gw_init(self):
        """
        Initialize the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.reset_buffer()
            self.gw_instance.start_continuous_listener()
        else:
            print("No GateWay, please try to reconnect it.")
            exit()
        return

    def gw_reset_config(self):
        """
        Configs the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.start_continuous_listener()
            self.gw_instance.write('!set_tester_mode 1', with_ack=True)
            self.gw_instance.write('!listen_to_tag_only 1', with_ack=True)
            self.gw_instance.config_gw(received_channel=self.received_channel, time_profile_val=self.time_profile_val,
                                       energy_pattern_val=self.energy_pattern_val,
                                       start_gw_app=False, with_ack=True,
                                       effective_output_power_val=22, sub1g_output_power_val=29)
        else:
            raise Exception('Could NOT connect to GW')

    def run(self):
        """
        Receives available data then counts and returns the number of unique advas
        """
        self.gw_instance.config_gw(start_gw_app=True)
        self.number_of_unq_adva = 0
        while not self.stop.is_set():
            time.sleep(0)
            if self.gw_instance.is_data_available():
                packet_list_in = self.gw_instance.get_packets(action_type=ActionType.ALL_SAMPLE)
                for packet in packet_list_in:
                    self.all_tags.append(packet)
            else:
                continue

            self.number_of_unq_adva = len(self.all_tags.tags)
        self.gw_instance.exit_gw_api()

    def get_unq_advas(self):
        """
        returns the number of unique advas
        """
        return self.number_of_unq_adva


class CountThread(threading.Thread):
    """
    Counting the number of tags
    """

    def __init__(self, stop_event, rows=1):
        threading.Thread.__init__(self, daemon=True)
        self.available_ports = [s.device for s in serial.tools.list_ports.comports()]
        self.get_ports_of_arduino()
        self.baud = '9600'
        self.ports = self.get_ports_of_arduino()
        try:
            self.comPortObj = serial.Serial(self.ports[0], self.baud, timeout=0.1)
        except serial.SerialException:
            print("NO ARDUINO")
        self.rows = rows
        self.stop = stop_event
        self.tested = 0

    def get_ports_of_arduino(self):
        """
        Gets all the ports we have, then chooses Arduino's ports
        """

        arduino_ports = []
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                arduino_ports.append(p.device)
        if not arduino_ports:
            print('NO ARDUINO')

        return arduino_ports

    def run(self):
        """
        Tries to read data and then counts the number of tags
        """

        while not self.stop.is_set():
            time.sleep(1)
            data = ''
            try:
                data = self.comPortObj.readline()

            except e:
                print("NO READLINE")
            buf = b''
            if data.__len__() > 0:
                buf += data
                if b'\n' in buf:
                    try:
                        tmp = buf.decode().strip(' \t\n\r')
                        if "pulses detected" in tmp:
                            self.tested += self.rows

                    except e:
                        print('Warning: Could not decode counter data or Warning: Could not decode counter data')
                        continue
        self.comPortObj.close()

    def get_tested(self):
        """
        returns the number of tags
        """
        return self.tested


class MultithreadedCalculation(threading.Thread):
    """
    Calculating the yield fraction by multi-threading process
    """

    def __init__(self, stop_event, received_channel, time_profile_val, energy_pattern_val, rows=1):
        threading.Thread.__init__(self, daemon=True)
        self.rows = rows
        self.adva_process = AdvaProcess(stop_event, received_channel, time_profile_val, energy_pattern_val)
        self.count_thread = CountThread(stop_event, self.rows)
        self.stop = stop_event
        self.result = 0

    def run(self):
        """
        The multi-threading process
        """
        self.adva_process.start()
        self.count_thread.start()
        while not self.stop.is_set():
            time.sleep(3)

            unq_advas = self.adva_process.get_unq_advas()
            tags_num = self.count_thread.get_tested()
            if tags_num > 0:
                self.result = unq_advas / tags_num
                print(self.result)

        self.adva_process.stop.set()
        self.count_thread.stop.set()
        self.adva_process.join()
        self.count_thread.join()

    def get_result(self):
        return self.result


class MainWindow:
    """
    The main class the runs the GUI and supervise the multi-threading process of fraction's calculation and GUI viewing
    """

    def __init__(self):
        self.multi = None
        self.stop = threading.Event()
        self.selected = ''
        self.wafer_lot = ''
        self.wafer_number = ''
        self.operator = ''
        self.run_start_time = ''
        self.run_end_time = ''
        self.tester_type = 'yield-test'
        self.tester_station_name = ''
        self.comments = ''
        self.gw_version = ''
        self.advas = 0
        self.run_responsive_tags_yield = 0  # still don't have a pass criteria
        self.result = 0
        self.run_passed_tags_yield = 0  # still don't have a pass criteria
        self.rows_number = 1
        self.upload_flag = True

    def run(self):
        """
        Viewing the window and checking if the process stops
        """

        self.open_session()
        self.overlay_window()
        self.multi.stop.set()
        self.multi.join()

    def run_data_to_csv(self, csv_dict, file_path, cmn_r_name, run_end_time, total_run_tested,
                        total_run_responding_tags, total_run_passed_tags, py_wiliot_version):
        """
        Saves a csv file with all the needed features
        """
        with open(file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([
                'common_run_name', 'tester_station_name', 'operator',
                'run_start_time', 'run_end_time', 'wafer_lot', 'wafer_number', 'tester_type',
                'comments', 'inlay', 'total_run_tested', 'total_run_responding_tags',
                'total_run_passed_tags', 'run_responsive_tags_yield', 'run_passed_tags_yield',
                'gw_version',
                'py_wiliot_version', 'upload_date', 'number_of_rows', 'received_channel', 'energy_pattern_val',
                'time_profile_val', ])
            if self.selected == '':
                # exit()
                pass
            value = csv_dict[self.selected]
            csv_writer.writerow(
                [
                    cmn_r_name, self.tester_station_name, self.operator,
                    formatted_date + ' ' + self.run_start_time,
                    formatted_date + ' ' + run_end_time,
                    self.wafer_lot, self.wafer_number, self.tester_type, self.comments, self.selected, total_run_tested,
                    total_run_responding_tags, total_run_passed_tags, self.run_responsive_tags_yield,
                    self.run_passed_tags_yield, self.gw_version, py_wiliot_version,
                    formatted_date + ' ' + time_formatted,
                    value['number_of_rows'], value['received_channel'], value['energy_pattern_val'],
                    value['time_profile_val'],
                ])

    def overlay_window(self):
        """
        The small window open session
        """

        start_time = datetime.datetime.now()
        self.run_start_time = start_time.strftime("%I:%M:%S")
        yes_or_no = ['Yes', 'No']
        layout = [
            [sg.Text('YIELD Fraction is :', font=4)],
            [sg.Output(key='yield', font=4, size=(60, 7))],
            [sg.Text('Do you want to stop or upload?')],
            [sg.Button('Stop'), [sg.Text('Upload:', font=6)],
             [sg.Combo(values=yes_or_no, default_value=yes_or_no[0], key='upload', font=4, enable_events=True)]]
        ]
        sub = False
        window = sg.Window('Upload CSV files', layout, modal=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event in ('Stop', 'upload'):
                if event == 'upload':
                    if values['upload'] == 'No':
                        self.upload_flag = False
                    else:
                        self.upload_flag = True  # if we press No then yes
                if event == 'Stop':
                    self.stop.set()
                    end_time = datetime.datetime.now()
                    run_end_time = end_time.strftime("%I:%M:%S")
                    advas = self.multi.adva_process.get_unq_advas()
                    tags_num = self.multi.count_thread.get_tested()
                    result = self.multi.get_result()
                    cmn = self.wafer_lot + '.' + self.wafer_number + '_' + formatted_today + '_' + cur_time_formatted
                    py_wiliot_version = get_version()
                    d = WiliotDir()
                    d.create_tester_dir(tester_name='yield_tester')
                    yield_test_app_data = d.get_tester_dir('yield_tester')
                    run_path = os.path.join(yield_test_app_data, cmn)
                    if not os.path.exists(run_path):
                        os.makedirs(run_path)
                    final_path_run_data = os.path.join(run_path, cmn + '@run_data.csv')

                    try:
                        self.run_data_to_csv(csv_dictionary, final_path_run_data, cmn, run_end_time,
                                             tags_num, advas, result, py_wiliot_version)
                    except Exception as e:
                        print(e)
                    try:
                        tag_df = self.multi.adva_process.all_tags.get_df()
                        tag_df.insert(loc=len(tag_df.columns), column='common_run_name', value=cmn)
                        final_path_packets_data = os.path.join(run_path, cmn + '@packets_data.csv')
                        tag_df.to_csv(final_path_packets_data, index=False)
                        if self.upload_flag:
                            try:
                                is_uploaded = upload_to_cloud_api(cmn, self.tester_type,
                                                                  run_data_csv_name=final_path_run_data,
                                                                  tags_data_csv_name=final_path_packets_data,
                                                                  env='test',
                                                                  packets_instead_tags=True, is_path=True)
                                if is_uploaded:
                                    print("Successful upload")
                                else:
                                    print("Unsuccessful upload")
                            except Exception as e:
                                print(e)
                                print("Upload function failure")

                    except Empty:
                        print("NO PACKETS RECEIVED")

                    sub = True
                    break
                if sub:
                    break

        window.close()
        return sub

    def open_session(self):
        """
        opening a session for the process
        """
        if os.path.exists("configs/gui_input_do_not_delete.json"):
            with open("configs/gui_input_do_not_delete.json", "r") as f:
                previous_input = json.load(f)

        else:
            previous_input = {'inlay': '', 'number': '', 'number_of_rows': '', 'received_channel': '',
                              'energy_pattern_val': '', 'time_profile_val': '', 'tester_station_name': '',
                              'comments': '', 'operator': '', 'wafer_lot': '', 'wafer_num': ''}
        selected_inlay = csv_dictionary[previous_input['inlay']]
        self.rows_number = selected_inlay['number_of_rows']
        energy_pat = selected_inlay['energy_pattern_val']
        time_pro = selected_inlay['time_profile_val']
        rec_channel = selected_inlay['received_channel']
        lst_inlay_options = list(inlay_types_dict.keys())
        layout = [

            [sg.Text('Wafer Lot:', font=4)],
            [sg.InputText(key='wafer_lot', default_text=previous_input['wafer_lot'], font=4)],

            [sg.Text('Wafer Number:', font=4)],
            [sg.InputText(key='wafer_num', default_text=previous_input['wafer_num'], font=4)],

            [sg.Text('Inlay:', font=4)],
            [sg.Combo(values=lst_inlay_options, default_value=previous_input['inlay'], key='inlay', font=4,
                      enable_events=True)],

            [
                sg.Column([[sg.Text('Energy Pattern:', font=4),
                            sg.Text(energy_pat, key='energy_pattern_val', font=4)]]),
                sg.Column([[sg.Text('Time Profile:', font=4),
                            sg.Text(time_pro, key='time_profile_val', font=4)]]),
                sg.Column([[sg.Text('Number of rows:', font=4), sg.Text(self.rows_number, key='rows', font=4)]]),
                sg.Column([[sg.Text('Received Channel:', font=4),
                            sg.Text(rec_channel, key='received_channel', font=4)]])
            ],

            [sg.Text('Tester Station Name:', font=4)],
            [sg.InputText(previous_input['tester_station_name'], key='tester_station_name', font=4)],
            [sg.Text('Comments:', font=4)],
            [sg.InputText(previous_input['comments'], key='comments', font=4)],

            [sg.Text('Operator:', font=4)],
            [sg.InputText(previous_input['operator'], key='operator', font=4)],

            [sg.Submit()]]

        window = sg.Window('WILIOT Yield Tester', layout, finalize=True)

        while True:
            event, values = window.read()
            if event == 'inlay':
                inlay_select = values['inlay']
                self.selected = values['inlay']
                self.wafer_lot = values['wafer_lot']
                self.wafer_number = values['wafer_num']

                if inlay_select in csv_dictionary:
                    selected_inlay = csv_dictionary[inlay_select]
                    self.rows_number = selected_inlay['number_of_rows']
                    energy_pat = selected_inlay['energy_pattern_val']
                    time_pro = selected_inlay['time_profile_val']
                    rec_channel = selected_inlay['received_channel']

                else:
                    self.rows_number = 'Invalid Selection'
                    energy_pat = 'Invalid Selection'
                    time_pro = 'Invalid Selection'
                    rec_channel = 'Invalid Selection'

                window.find_element('rows').Update(value=self.rows_number)
                window.find_element('energy_pattern_val').Update(value=energy_pat)
                window.find_element('time_profile_val').Update(value=time_pro)
                window.find_element('received_channel').Update(value=rec_channel)
            if event == 'Submit':  # Button clicked
                self.comments = values['comments']
                self.tester_station_name = values['tester_station_name']
                self.operator = values['operator']
                self.multi = MultithreadedCalculation(self.stop, rec_channel,
                                                      time_pro, energy_pat, self.rows_number)
                self.gw_version = self.multi.adva_process.gw_instance.get_gw_version()[0]
                self.multi.start()
                with open("configs/gui_input_do_not_delete.json", "w") as f:
                    json.dump(values, f)
                break
            elif event == sg.WIN_CLOSED:
                exit()

        window.close()


if __name__ == '__main__':
    m = MainWindow()
    m.run()