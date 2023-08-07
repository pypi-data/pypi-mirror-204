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
import signal
import socket
import subprocess
from os.path import isfile, isdir
from tkinter import Tk, INSERT, END, filedialog, Toplevel
from tkinter.font import Font
import serial.tools.list_ports
import pygubu
import json
import os
import sys
import multiprocessing
import logging
import datetime
import time
import threading
import pandas as pd
import numpy as np
import csv
import re

from wiliot_core import WiliotGateway, StatType, ActionType, DataType, valid_output_power_vals, valid_bb, \
    valid_sub1g_output_power
from wiliot_core import TagCollection, PacketList, Packet
from wiliot_core import WiliotDir
from wiliot_tools.local_gateway_gui.utils.gw_macros import macros
from wiliot_tools.local_gateway_gui.utils.debug_mode import debug_flag

from wiliot_tools.utils.get_version import get_version

DECRYPTION_MODE = False


def print_exceptions():
    package_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(package_dir, "extended")

    if (os.path.isfile(path) and os.path.getsize(path) > 0) or debug_flag['debug_bool']:
        return True
    return False


try:
    from wiliot_core import DecryptedTagCollection
    from wiliot_tools.extended.pixie_analyzer.config_files.plot_config import plot_config
    from wiliot_tools.extended.pixie_analyzer.pixie_analyzer import PixieAnalyzer

    DECRYPTION_MODE = True
    print('Working on decrypted mode')
except Exception as e:
    if print_exceptions():
        print('Working on encrypted mode')  # SHOULD NOT BE PRINTED FOR PUBLIC USER!
        print(e)  # SHOULD NOT BE PRINTED FOR PUBLIC USER!
    pass

try:  # live plots
    from wiliot_tools.local_gateway_gui.feature_flags import *
    from collections import deque
    import random
    import dash
    from dash.dependencies import Output, Input, State
    from dash.exceptions import PreventUpdate

    from dash import dcc
    from dash import html
    import plotly
    import plotly.graph_objs as go


except Exception as e:
    LIVE_PLOTS_ENABLE = False
    # print('Live plotting is disabled')  # SHOULD NOT BE PRINTED FOR PUBLIC USER!
    # print(e)  # SHOULD NOT BE PRINTED FOR PUBLIC USER!

# default config values:
EP_DEFAULT = 18  # Energizing pattern
EPs_DEFAULT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
               50, 51, 52)  # All Energizing pattern
TP_O_DEFAULT = 5  # timing profile on
TP_P_DEFAULT = 15  # timing profile period
PI_DEFAULT = 0  # pace interval
RC_DEFAULT = 37
RCs_DEFAULT = (37, 38, 39)
DATA_TYPES = ('raw', 'processed', 'statistics', 'full_UID_mode', 'decoded_packet')
CONFIG_SUM = "EP:{EP}\nTP_ON:{TP_ON}\nTP_P:{TP_P}\nRC:{RC}\nPI:{PI}\nF:{F}"
baud_rates = ["921600"]
energy_pattern_dict = {18: 'Energizing on channel 39 only',
                       20: '20% channel 37 , 80% channel 39',
                       50: 'Energizing in 915Mhz',
                       51: 'Energizing on both channel 39 and 915Mhz',
                       }

__version__ = get_version()


class GatewayUI(object):
    gwCommandsPath = os.path.join(os.path.abspath('utils'), '.gwCommands.json')
    gwUserCommandsPath = os.path.join(os.path.abspath('utils'), '.gwUserCommands.json')
    gwAllCommands = []
    gwCommands = []
    gwUserCommands = []
    filter_state = False
    send_data_to_another_app = False
    portActive = False
    log_state = False
    autoscroll_state = True
    logger = logging.getLogger('root')
    stat_type = StatType.N_FILTERED_PACKETS
    log_path = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'gw_log.{}'.format("log")

    def __init__(self, main_app_folder='', array_out=None, tk_frame=None):
        print('GW UI mode is activated')
        print(__version__)
        self.busy_processing = False
        self.close_requested = False
        # check which mode we are:
        self.decryption_mode = DECRYPTION_MODE
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()
        self.multi_tag = TagCollection()
        self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])
        self.filter_tag = [re.compile('')]
        self.data_handler_listener = None
        self.UID_mode = False
        if self.decryption_mode:
            try:
                self.myPixieAnalyzer = PixieAnalyzer()
                self.packet_decoder = self.myPixieAnalyzer.PacketDecoder()
            except Exception as e:
                self.myPixieAnalyzer = None
                if print_exceptions():
                    print('problem during loading PixieAnalyzer: {}'.format(e))

        self.env_dir = WiliotDir()
        self.logs_dir = os.path.join(self.env_dir.get_tester_dir("local_gateway_gui"), "logs")
        if not isdir(self.logs_dir):
            self.env_dir.create_dir(self.logs_dir)

        if LIVE_PLOTS_ENABLE:
            self.init_live_plot()
            self.prev_packet_cntr = 0

        # 2: Load an ui file
        utils_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils')
        if self.decryption_mode:
            uifile = os.path.join(utils_path, 'gw_debugger.ui')
        else:
            uifile = self.get_encrypted_ui(os.path.join(utils_path, 'gw_debugger.ui'))
        builder.add_from_file(uifile)
        builder.add_resource_path(utils_path)

        if tk_frame:
            self.ttk = tk_frame  # tkinter.Frame , pack(fill="both", expand=True)
        else:
            self.ttk = Tk()
        self.ttk.title(f"Wiliot Local Gateway GUI Application (V{__version__})")

        # 3: Create the widget using a self.ttk as parent
        self.mainwindow = builder.get_object('mainwindow', self.ttk)

        self.ttk = self.ttk

        # set the scroll bar of the main textbox
        textbox = self.builder.get_object('recv_box')
        scrollbar = self.builder.get_object('scrollbar')
        textbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=textbox.yview)
        self.builder.get_object('scrollbar').set(self.builder.get_object('recv_box').index(INSERT),
                                                 self.builder.get_object('recv_box').index(END))
        self.builder.get_object('recv_box').grid()

        self.builder.connect_callbacks(self)

        # upload pre-defined commands
        self.gwCommandsPath = os.path.join(main_app_folder, self.gwCommandsPath)
        if isfile(self.gwCommandsPath):
            with open(self.gwCommandsPath, 'r') as f:
                self.gwCommands = json.load(f)

        self.gwUserCommandsPath = os.path.join(main_app_folder, self.gwUserCommandsPath)
        if isfile(self.gwUserCommandsPath):
            with open(self.gwUserCommandsPath, 'r') as f:
                self.gwUserCommands = json.load(f)

        self.gwAllCommands = self.gwCommands + self.gwUserCommands

        # define array to export data for other applications
        if array_out is None:
            self.data_out = multiprocessing.Queue()
        else:
            self.data_out = array_out

        self.ttk.lift()
        self.ttk.attributes("-topmost", True)
        self.ttk.attributes("-topmost", False)

        self.ObjGW = WiliotGateway(logger_name='root')
        self.config_param = {}
        self.formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')
        self.logger_num = 1

        # update ui
        if self.decryption_mode:
            self.decrypted_multi_tag = DecryptedTagCollection()
            self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])
            self.plot_config = plot_config()
            self.custom_plot = True
            self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('load_log')['state'] = 'disabled'
        else:
            self.decrypted_multi_tag = None
            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'disabled'

            self.plot_config = None
            self.custom_plot = False

        self.ui_update('init')
        self.ui_update('available_ports')

        self.ttk.protocol("WM_DELETE_WINDOW", self.close_window)

        self.ttk.after_idle(self.periodic_call)
        self.ttk.mainloop()

    @staticmethod
    def get_encrypted_ui(ui_path):
        decrypted_guis = ['save_to_file', 'plot_log', 'load_log', 'custom_plots', 'packet_show_button',
                          'analysis_plot_label', 'live_plot_label']
        enc_ui_path = ui_path.replace('.ui', '_encrypted.ui')
        if os.path.isfile(enc_ui_path):
            return enc_ui_path

        with open(ui_path, 'r') as f:
            lines = f.readlines()
            new_lines = []
            need_to_del_section = False
            n_child = 0
            for line in lines:
                if not need_to_del_section:
                    for dec_gui in decrypted_guis:
                        if dec_gui in line:
                            need_to_del_section = True
                            break
                if need_to_del_section:
                    if 'child' in line:
                        n_child += 1
                    if n_child == 2:
                        need_to_del_section = False
                        n_child = 0
                else:
                    new_lines.append(line)

        with open(enc_ui_path, 'w') as new_f:
            new_f.writelines(new_lines)
        return enc_ui_path

    def get_log_file_name(self, filename=None):
        if filename is None:
            filename = self.builder.get_object('log_path').get()
        if filename:
            filename = filename.strip("\u202a")  # strip left-to-right unicode if exists
            if os.path.isfile(filename):
                return filename
            return os.path.join(self.logs_dir, filename)
        else:
            return None

    def get_filter_text(self, text=''):
        if len(text) > 0:
            text = text.replace(' ', '')
            self.filter_tag = text.split(',')
            self.filter_tag = [re.compile(f.lower()) for f in self.filter_tag]
        else:
            self.filter_tag = [re.compile('')]

    def is_filtered(self, packet):
        for f in self.filter_tag:
            if f.pattern.startswith('^'):
                if f.search(packet.decoded_data['tag_id'][-4:].lower()):
                    return True
            else:
                if f.search(packet.decoded_data['tag_id'].lower()):
                    return True
        return False

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time(), "Was busy processing:", self.busy_processing)

    def periodic_call(self):
        if not self.close_requested:
            self.busy_processing = True
            self.busy_processing = False
            self.ttk.after(500, self.periodic_call)

        else:
            print("Destroying GUI at:", time.time())
            try:
                self.ObjGW.exit_gw_api()
                if self.data_handler_listener is not None and self.data_handler_listener.is_alive():
                    self.data_handler_listener.join()
                if LIVE_PLOTS_ENABLE:
                    self.live_plots_event.set()
                if self.log_state:
                    logging.FileHandler(self.get_log_file_name()).close()
                self.exit_packet_show()
                self.ttk.destroy()
                exit(0)
            except Exception as e:
                print('problem during periodic call: {}'.format(e))
                exit(1)

    def on_connect(self):
        if not self.portActive:  # Port is not opened
            try:
                port = self.builder.get_object('port_box').get().rsplit(' ', 1)[0]
                baud = self.builder.get_object('baud_rate_box').get().rsplit(' ', 1)[0]
                if port == '' or baud == '':
                    return

                if self.ObjGW.open_port(port, baud):  # open and check if succeed
                    self.print_function(str_in="> Port successfully opened")
                    self.portActive = True
                    self.builder.get_object('connect_button').configure(text='Disconnect')
                    # print version:
                    self.print_function(str_in=self.ObjGW.hw_version + '=' + self.ObjGW.sw_version)
                    self.builder.get_object('recv_box').see(END)
                    # config gw to receive packets (and not only manage bridges):
                    rsp = self.ObjGW.write('!set_tester_mode 1', with_ack=True)
                    if 'command complete event' in rsp['raw'].lower():
                        self.config_param['pacer_val'] = '0'
                        self.config_param['filter'] = 'N'
                    # update UI:
                    self.ui_update('connect')
                    self.start_listening()
                    # update config:
                    rsp = self.ObjGW.write('!print_config_extended', with_ack=True)
                    if rsp['raw'] and 'unsupported' not in rsp['raw'].lower():
                        self.print_function(rsp['raw'])
                        self.from_gw_msg_to_config_param(rsp['raw'])

                else:
                    self.print_function(str_in="> Can't open Port - check connection parameters and try again")
                    self.portActive = False
            except Exception as e:
                self.print_function(str_in="> Encounter a problem during connection: {}".format(e))

        else:  # Port is opened, close it...
            try:
                self.print_function(str_in="> Disconnecting from Port")
                self.ObjGW.stop_continuous_listener()
                self.ObjGW.close_port()
                self.builder.get_object('connect_button').configure(text="Connect")
                self.portActive = False
                self.ui_update('connect')
            except Exception as e:
                self.print_function(str_in="> Encounter a problem during disconnection: {}".format(e))

    def from_gw_msg_to_config_param(self, gw_msg):
        conv_str = [{'msg': 'Energizing Pattern=', 'param': 'energy_pattern'},
                    {'msg': 'Scan Ch/Freq=', 'param': 'received_channel'},
                    {'msg': 'Transmit Time=', 'param': 'time_profile_on'},
                    {'msg': 'Cycle Time=', 'param': 'time_profile_period'}]
        for d in conv_str:
            if d['msg'] in gw_msg:
                x = gw_msg.split(d['msg'])[1].split(',')[0]
                try:
                    int(x)
                    self.config_param[d['param']] = x
                except Exception as e:
                    pass
        self.ui_update('config')

    def start_listening(self):
        # start listening:
        self.ObjGW.start_continuous_listener()
        if self.data_handler_listener is None or not self.data_handler_listener.is_alive():
            self.data_handler_listener = threading.Thread(target=self.recv_data_handler, args=())
            self.data_handler_listener.start()

    def on_search_ports(self):
        self.ObjGW.available_ports = [s.device for s in serial.tools.list_ports.comports() if
                                      'Silicon Labs' in s.description or 'CP210' in s.description]
        if len(self.ObjGW.available_ports) == 0:
            self.ObjGW.available_ports = [s.name for s in serial.tools.list_ports.comports()
                                          if 'Silicon Labs' in s.description or 'CP210' in s.description]
        # update ui:
        self.ui_update('available_ports')

    def on_send_to_additional_app(self):
        self.send_data_to_another_app = self.builder.get_variable('send_data_state').get()
        if self.send_data_to_another_app:
            self.print_function(str_in="> Send data to additional app via tcp/ip communication ({}:{})".format(
                self.ObjGW.socket_host, self.ObjGW.socket_port))
        else:
            self.print_function(str_in="> Stop sending data to additional app")
            self.ObjGW.close_socket_connection()

    def recv_data_handler(self):
        print("DataHandlerProcess Start")
        consecutive_exception_counter = 0
        while True:
            time.sleep(0)
            try:
                if self.close_requested or not self.portActive:
                    print("DataHandlerProcess Stop")
                    return

                # check if there is data to read
                if self.ObjGW.is_data_available():
                    self.UID_mode = False
                    action_type = ActionType.ALL_SAMPLE
                    # get data
                    data_type = DataType.RAW
                    if self.builder.get_object('data_type').get() == 'raw':
                        data_type = DataType.RAW
                    elif self.builder.get_object('data_type').get() == 'processed':
                        data_type = DataType.PROCESSED
                    elif self.builder.get_object('data_type').get() == 'statistics':
                        data_type = DataType.PACKET_LIST
                    elif self.builder.get_object('data_type').get() == 'full_UID_mode':
                        self.UID_mode = True
                        if self.decryption_mode:
                            data_type = DataType.DECODED
                        else:
                            data_type = DataType.PACKET_LIST
                    elif self.builder.get_object('data_type').get() == 'decoded_packet' and self.decryption_mode:
                        data_type = DataType.DECODED
                    else:
                        data_type = DataType.PROCESSED

                    data_in = self.ObjGW.get_packets(action_type=action_type, num_of_packets=None,
                                                     data_type=data_type,
                                                     send_to_additional_app=self.send_data_to_another_app)

                    if data_type == DataType.PACKET_LIST:

                        for packet in data_in.packet_list:
                            for f in self.filter_tag:
                                if f.search(packet.packet_data['adv_address'].lower()):
                                    self.multi_tag.append(packet)
                                    if self.UID_mode:
                                        self.print_function(str_in='AdvA: ' + str(packet.packet_data['adv_address']))
                                else:
                                    continue
                                # self.print_function(str_in=str(d))

                        if int((time.time() % 5)) == 0 and not self.UID_mode:
                            # self.on_clear(restart=False)
                            statistics_df = self.multi_tag.get_statistics_list()
                            all_data_str = statistics_df

                            self.print_function(str_in='---------------------- '
                                                       '{}: Tags Statistics '
                                                       '----------------------'.format(datetime.datetime.now()))
                            for d in all_data_str:
                                self.print_function(str_in=str(d))

                    elif data_type == DataType.DECODED:
                        for packet in data_in.packet_list:
                            if packet.get_packet_version() < 2.1:
                                continue
                            if self.is_filtered(packet):
                                self.decrypted_multi_tag.append(packet)

                                self.update_tags_count_label(self.decrypted_multi_tag.get_tags_count())

                                if LIVE_PLOTS_ENABLE:
                                    if self.prev_packet_cntr != packet.decoded_data['packet_cntr']:

                                        try:
                                            for live_plots_attribute in LIVE_PLOTS_ATTRIBUTES:
                                                if live_plots_attribute.lower() in packet.decoded_data.keys():
                                                    self.live_plots_data[live_plots_attribute]['X'].append(
                                                        packet.gw_data['time_from_start'].item(0))
                                                    self.live_plots_data[live_plots_attribute]['Y'].append(
                                                        packet.decoded_data[live_plots_attribute.lower()])
                                                    # self.Y.append(packet.decoded_data['packet_cntr'])
                                        except Exception as e:
                                            print(e)
                                    self.prev_packet_cntr = packet.decoded_data['packet_cntr']
                            else:
                                continue
                            decrypted_packet = self.decrypted_multi_tag.get_last_added_packet()
                            if self.UID_mode:
                                try:
                                    decrypted_packet_id = decrypted_packet.decoded_data['tag_id']
                                    log_text = 'TagID: ' + decrypted_packet_id
                                except Exception as e:
                                    print("Couldn't decrypt packet")
                            else:
                                log_text = decrypted_packet.to_oneline_log()
                            if log_text is None:
                                continue

                            self.print_function(log_text)

                            if self.send_data_to_another_app:
                                packet_dict_to_main = {'time': decrypted_packet.gw_data['time_from_start'],
                                                       'raw': decrypted_packet.get_packet_string()}
                                self.data_out.put(packet_dict_to_main)

                    else:
                        if data_type == DataType.PROCESSED:
                            for pkt in data_in:
                                for f in self.filter_tag:
                                    if f.search(pkt['adv_address'].lower()):
                                        data_str = []
                                        for key, value in pkt.items():
                                            data_str.append("{}:{}".format(key, value))
                                        all_data_str = ','.join(data_str)
                                        self.print_function(str_in=all_data_str)
                                        # add it to the JTAG GUI if needed:
                                        if self.send_data_to_another_app:
                                            self.data_out.put(pkt)
                                    else:
                                        continue
                        if data_type == DataType.RAW:
                            for pkt in data_in:
                                data_str = []
                                for key, value in pkt.items():
                                    # The 4 next rows are just to make 'time' with the same number of
                                    # digits for all packets
                                    if key == 'time':
                                        value = '{:.6f}'.format(value)
                                    data_str.append("{}:{}".format(key, value))
                                all_data_str = ','.join(data_str)
                                self.print_function(str_in=all_data_str)
                                # add it to the JTAG GUI if needed:
                                if self.send_data_to_another_app:
                                    self.data_out.put(pkt)
                    consecutive_exception_counter = 0
            except Exception as e:
                print("DataHandlerProcess Exception: {}".format(e))
                consecutive_exception_counter = consecutive_exception_counter + 1
                if consecutive_exception_counter > 10:
                    print("Abort DataHandlerProcess")
                    return

    def on_macro_folder(self):
        macro_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils', 'gw_macros.py')
        self.print_function(str_in=f"> Go to {macro_path} to edit macros")

    def on_update_gw_version(self):
        self.print_function(str_in="> Updating GW version, please wait...")
        version_path_entry = self.builder.get_object('version_path').get()
        if version_path_entry:
            version_path_entry = version_path_entry.strip("\u202a")  # strip left-to-right unicode if exists
            if not os.path.isfile(version_path_entry):
                self.print_function(str_in="> cannot find the entered gw version file:")
                return

        success_update = self.ObjGW.update_version(versions_path=version_path_entry)
        # listen again:
        self.start_listening()
        if success_update:
            self.print_function(str_in="> Update GW version was completed [{}]".format(self.ObjGW.sw_version))
        else:
            self.print_function(str_in="> Update GW version was failed ")

    def on_reset(self):
        self.ObjGW.reset_gw()
        time.sleep(1)
        self.ObjGW.write('!set_tester_mode 1', with_ack=True)
        self.ObjGW.reset_listener()

    def exit_packet_show(self):
        try:
            # Check if the Bokeh server is already running on port 5006 and kill it
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 5006))  # bokeh port
            if result == 0:
                # Server is already running on port 5006, kill it and start a new server
                if sys.platform == "darwin" or sys.platform == 'linux':
                    p = subprocess.Popen(['lsof', '-i', ':5006'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = p.communicate()
                    pid = out.decode('utf-8').split('\n')[1].split()[1]
                else:
                    # windows
                    p = os.popen('netstat -ano | findstr :5006')
                    out = p.read()
                    pid_list = list(set([pid.split(' ')[-1] for pid in out.split('\n') if '0.0.0.0:5006' in pid]))
                    if len(pid_list) != 1:
                        self.print_function("Could not decide which process to kill: {}".format(pid_list))
                        return
                    pid = pid_list[0]
                os.kill(int(pid), signal.SIGILL)
            # kill packet show if running:
            os.kill(int(self.ObjGW.socket_port), signal.SIGILL)

        except Exception as e:
            self.print_function(f"Error during exit_packet_show: {e}")

    def on_packet_show(self):
        self.send_data_to_another_app = True
        try:
            # Check if the Bokeh server is already running on port 5006 and kill it
            self.exit_packet_show()

            # Server is not running on port 5006, start a new server and show the app
            package_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(package_dir, "extended", "packet_show", "packet_show.py")
            subprocess.Popen(['bokeh', 'serve', '--port', '5006', '--show', path])

        except Exception as e:
            self.print_function(f"Error during on_packet_show: {e}")

    def on_enter_write(self, args):
        if args.char == '\r':
            self.on_write()

    def on_write(self):
        cmd_value = self.builder.get_object('write_box').get()
        rsp_val = self.ObjGW.write(cmd_value, with_ack=True, max_time=0.100)
        self.on_user_event(user_event_text=cmd_value)
        self.print_function(', '.join(['{}: {}'.format(k, v) for k, v in rsp_val.items()]))

        if cmd_value.strip() not in list(self.builder.get_object('write_box')['values']):
            temp = list(self.builder.get_object('write_box')['values'])

            # keep only latest instances
            if temp.__len__() == 20:
                temp.pop(0)
            if len(self.gwUserCommands) >= 20:
                self.gwUserCommands.pop(0)
            self.gwUserCommands.append(cmd_value)
            temp.append(cmd_value)
            self.builder.get_object('write_box')['values'] = tuple(temp)
            with open(self.gwUserCommandsPath, 'w+') as f:
                json.dump(self.gwUserCommands, f)

        self.ui_update(state='config')

    def on_run_macro(self):
        from wiliot_tools.local_gateway_gui.utils.gw_macros import macros  # import again to check changes during run
        selected_macro = self.builder.get_object('macros_ddl').get()
        if selected_macro in macros.keys():
            data_handler_listener = threading.Thread(target=self.run_macro, args=())
            data_handler_listener.start()
        else:
            self.print_function("Please select a valid macro")

    def run_macro(self):
        selected_macro = self.builder.get_object('macros_ddl').get()
        macro_commands = macros[selected_macro]
        for c in macro_commands:
            command_value = c["command"]
            time_value = c["wait"]
            self.print_function("Command: {c},\t Wait: {t}".format(c=command_value, t=time_value))
            command_start_time = time.time()
            if command_value == 'user_event':
                self.on_user_event(user_event_text=c.get('values', 'user_event'))
            elif command_value == 'save_log':
                self.on_processed_data(c.get('values', r'~/Downloads/output.csv'))
            else:
                rsp_val = self.ObjGW.write(command_value, with_ack=True)
                self.on_user_event(user_event_text=command_value)
                self.print_function(', '.join(['{}: {}'.format(k, v) for k, v in rsp_val.items()]))
                # self.start_listening()
            while time.time() - command_start_time < time_value:
                time.sleep(1)
        self.print_function('Macro {selected_macro} Done.'.format(selected_macro=selected_macro))

    def on_config(self):
        filter_val = self.filter_state
        pacer_val = int(self.builder.get_object('pace_inter').get())
        energ_ptrn_val = int(self.builder.get_object('energizing_pattern').get())

        time_profile_val = [int(self.builder.get_object('timing_profile_on').get()),
                            int(self.builder.get_object('timing_profile_period').get())]
        received_channel_val = int(self.builder.get_object('received_channel').get())
        self.print_function(str_in="> Setting GW configuration...")
        if energ_ptrn_val in energy_pattern_dict.keys():
            self.print_function(str_in='Setting pattern {energ_ptrn_val} -> {pattern_explanation}'.format(
                energ_ptrn_val=str(energ_ptrn_val), pattern_explanation=energy_pattern_dict[energ_ptrn_val]))

        config_param_set, gateway_response = self.ObjGW.config_gw(filter_val=filter_val, pacer_val=pacer_val,
                                                                  energy_pattern_val=energ_ptrn_val,
                                                                  time_profile_val=time_profile_val,
                                                                  received_channel=received_channel_val,
                                                                  with_ack=True)
        # update config parameters:
        for key, value in config_param_set.__dict__.items():
            if key == 'filter' or key == 'modulation':
                self.config_param[key] = str(value)[0]
            else:
                self.config_param[key] = str(value)

        self.ui_update(state='config')
        self.print_function(str_in="> Configuration is set")

    def on_set_filter(self):
        self.filter_state = self.builder.get_variable('filter_state').get()
        self.print_function(str_in='> Setting filter...')
        config_param_set, _ = self.ObjGW.config_gw(filter_val=self.filter_state, with_ack=True)
        self.config_param["filter"] = str(config_param_set.filter)[0]

        self.ui_update(state='config')

    def on_clear(self, restart=True):
        self.builder.get_object('recv_box').delete('1.0', END)
        self.builder.get_object('recv_box').see(END)
        if self.decryption_mode:
            self.update_tags_count_label(0)
        if restart:
            self.multi_tag = TagCollection()
            if self.decryption_mode:
                self.decrypted_multi_tag = DecryptedTagCollection()
                self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])
                if LIVE_PLOTS_ENABLE:
                    self.reset_live_plot()

    def set_logger(self, level=logging.DEBUG):
        """
        setup logger to allow running multiple logger
        """
        handler = logging.FileHandler(self.get_log_file_name())
        handler.setFormatter(self.formatter)

        self.logger = logging.getLogger('logger{}'.format(self.logger_num))
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
        self.logger_num = self.logger_num + 1

    def on_filter_id(self, args):
        if args.char == '\r':
            f_input = self.builder.get_object('filter_id').get()
            if not f_input == 'filter ids':
                self.get_filter_text(f_input)
            if LIVE_PLOTS_ENABLE:
                self.reset_live_plot()

    def on_log(self):
        self.log_state = not self.log_state
        if self.log_state:
            check_log_path = self.get_log_file_name()
            if not check_log_path:
                self.log_state = False
                self.print_function(str_in='> Log path is invalid')
                self.builder.get_object('log_button')['text'] = 'Start Log'
                return
            try:
                self.set_logger()

                self.print_function(str_in='> Start Logging [{}]'.format(self.get_log_file_name()))
                self.builder.get_object('log_button')['text'] = 'Stop Log'
                return
            except Exception as e:
                self.print_function(str_in='> Log path is invalid: {}'.format(e))
                self.log_state = False
                self.builder.get_object('log_button')['text'] = 'Start Log'
                return
        else:
            self.builder.get_object('log_button')['text'] = 'Start Log'
            self.print_function(str_in='> Stop Logging')
            logging.FileHandler(self.get_log_file_name()).close()
            self.on_processed_data(output_path=self.get_log_file_name())
            # reset log path and user events
            self.log_path = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + 'gw_log.{}'.format("log")
            self.builder.get_object('log_path').delete(0, 'end')
            self.builder.get_object('log_path').insert(END, self.log_path)
            self.user_events = pd.DataFrame(columns=['user_event_time', 'user_event_data'])

    def on_autoscroll(self):
        self.autoscroll_state = self.builder.get_variable('autoscroll_state').get()

    def on_data_type_change(self, selected):
        if selected.widget.get() == 'decoded_packet' or selected.widget.get() == 'full_UID_mode':
            self.builder.get_object('filter_id')['state'] = 'enabled'
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id').insert(0, 'filter ids')
            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'enabled'
                self.builder.get_object('plot_log')['state'] = 'enabled'
            self.on_clear()

        else:
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id')['state'] = 'disabled'
            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'disabled'
                self.builder.get_object('plot_log')['state'] = 'disabled'
            self.update_tags_count_label(clear=True)

    def update_tags_count_label(self, count=0, clear=False):
        text_obj = self.builder.get_object('tags_count')
        text_obj.delete("end")
        if clear:
            text_obj.insert(END, "\n".format(
                tag_format=str(count)))
        else:
            text_obj.insert(END, "\ntags count: {tag_format}".format(
                tag_format=str(count)))
        text_obj.see(END)

    def on_custom_plots(self):
        t = Toplevel(self.ttk)
        CustomPlotGui(plot_config=self.plot_config, print_func=self.print_function, tk_frame=t)

    def on_user_event(self, user_event_text=None):
        if user_event_text is None:
            user_event_text = self.builder.get_object('user_event_text').get()
        self.print_function(str_in="user_event_time: {}, User event: {}".format(self.ObjGW.get_curr_timestamp_in_sec(),
                                                                                user_event_text))
        user_event_row = {'user_event_time': self.ObjGW.get_curr_timestamp_in_sec(), 'user_event_data': user_event_text}
        self.user_events = self.user_events.append(user_event_row, ignore_index=True)

    def on_plot_log(self):
        plots_location = filedialog.askdirectory(initialdir="~/Documents",
                                                 title="Choose output location")
        if plots_location != '':
            if len(self.decrypted_multi_tag) > 0:
                try:
                    self.print_function(str_in="Starting plot analyzing")
                    plot_thread = threading.Thread(target=self.myPixieAnalyzer.plot_graphs,
                                                   args=(self.decrypted_multi_tag, self.user_events, 6, 'Yes', 50,
                                                         False, self.plot_config, plots_location))
                    plot_thread.start()
                    self.print_function(
                        str_in='Plot files will be saved in {plots_location}'.format(plots_location=plots_location))
                except PermissionError as pe:
                    self.print_function(
                        str_in='Got "{strerror}" in folder: {plots_location}'.format(strerror=pe.strerror,
                                                                                     plots_location=plots_location))
                except Exception as e:
                    self.print_function(str_in='Unknown error: {}'.format(e))

            else:
                self.print_function(str_in='No packets received in decoded_packet mode yet.')
        else:
            self.print_function(str_in='No output location selected.')

    def on_load_log(self):
        file_path_input = filedialog.askopenfilename(initialdir="~/Documents",
                                                     title="Select packet log input file",
                                                     filetypes=[("csv files", "*.csv")])
        plots_location = filedialog.askdirectory(initialdir="~/Documents",
                                                 title="Choose output location")
        if plots_location != '':
            if '_plot.csv' not in file_path_input:
                self.print_function(str_in='Invalid file, choose *_plot.csv file')
            elif file_path_input != '':
                try:
                    self.print_function(str_in="Starting plot analyzing")
                    start = time.time()
                    [_, plot_data, user_event] = self.packet_decoder.parse(input=file_path_input)

                    user_event_file = file_path_input.replace('_plot', '_user_event')
                    if os.path.isfile(user_event_file):
                        user_event = pd.read_csv(user_event_file, index_col=False)

                    end = time.time()
                    self.print_function(str_in='PlotGraphsGen2: {t}'.format(t=round(end - start, 2)))

                    if len(plot_data) > 0:
                        plot_thread = threading.Thread(target=self.myPixieAnalyzer.plot_graphs,
                                                       args=(plot_data, user_event, 6, 'Yes', 50,
                                                             False, self.plot_config, plots_location))
                        plot_thread.start()
                        self.print_function(
                            str_in='Plot files will be saved in {plots_location}'.format(plots_location=plots_location))
                    else:
                        self.print_function(str_in='Empty TagCollection')
                except Exception as e:
                    self.print_function(str_in='problem during on_load_log: {}'.format(e))
            else:
                self.print_function(str_in='No file selected.')
        else:
            self.print_function(str_in='No output location selected.')

    def extract_packet_list_from_log(self, log_path=None):
        packet_list = PacketList()
        packets, packets_time = self.extract_packets_from_log(log_path=log_path)
        for p, t in zip(packets, packets_time):
            packet_list.append(Packet(raw_packet=p, time_from_start=t))
        return packet_list

    def extract_packets_from_log(self, log_path=None):
        if log_path is None:
            self.print_function(str_in='no log path was found. Export csv failed')
            return
        try:
            packets = []
            packets_time = []
            if isfile(log_path):
                f = open(log_path, 'r')
                lines = f.readlines()

                for line in lines:
                    if 'raw:process_packet("' in line or 'is_valid_tag_packet:True' in line:
                        # a data line
                        if 'raw:process_packet("' in line:
                            re_match = re.search("process_packet\(\"(\w+)\"", line)
                            packet_raw = str(re_match.groups(1)[0])
                        else:  # packet: ABCD format (data type = processed
                            re_match = re.search(",packet:(\w+)", line)
                            packet_raw = str(re_match.groups(1)[0])
                        if 'time_from_start:' in line:
                            re_match = re.search("time_from_start:(\d+.\d+)", line)
                            packet_time = float(re_match.groups(1)[0])
                        else:
                            re_match = re.search("time:(\d+.\d+)", line)
                            packet_time = float(re_match.groups(1)[0])

                        packets.append(packet_raw)
                        packets_time.append(packet_time)
                f.close()
            return packets, packets_time
        except Exception as e:
            self.print_function(str_in='export packets from log was failed due to: {}'.format(e))
            return None, None

    def create_csv(self, log_path=None):

        def create_config_csv(data_in):
            # create config type:
            comments = '-'  # self.builder.get_object('csv_comment').get()
            if comments == 'add comments':
                comments = '-'
            config_data = {'commonRunName': [common_run_name],
                           'comments': [comments]}
            # generate the csv file:
            with open(log_path.replace('.log', '_config.csv'), 'w', newline='') as f_config:
                writer_cld = csv.writer(f_config)
                writer_cld.writerow(list(config_data.keys()))
                writer_cld.writerows(list(map(list, zip(*[val for val in config_data.values()]))))
                f_config.close()

        if log_path is None:
            self.print_function(str_in='no log path was found. Export csv failed')
            return

        common_run_name = 'gw_gui_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            if isfile(log_path):
                packets, packets_time = self.extract_packets_from_log(log_path=log_path)
                if packets is None or packets_time is None:
                    self.print_function(str_in='export csv failed')
                    return

                data_to_csv = {'commonRunName': [common_run_name] * len(packets),
                               'encryptedPacket': packets, 'time': packets_time}

                # generate the csv file:
                with open(log_path.replace('.log', '_data.csv'), 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(list(data_to_csv.keys()))
                    writer.writerows(list(map(list, zip(*[val for val in data_to_csv.values()]))))
                    f.close()
                # generate config file according to cloud convention:
                create_config_csv(data_to_csv)
            else:
                self.print_function(str_in='invalid log path: {}\nexport csv was failed'.format(log_path))
        except Exception as e:
            self.print_function(str_in='export csv was failed due to: {}'.format(e))

    @staticmethod
    def return_time_str():
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        return dt_string

    def on_processed_data(self, output_path=None):
        if self.decryption_mode and (self.builder.get_object('data_type').get() == 'decoded_packet' or
                                     self.builder.get_object('data_type').get() == 'full_UID_mode'):
            if len(self.decrypted_multi_tag) > 0:
                if output_path is None:
                    csv_location = filedialog.asksaveasfilename(
                        filetypes=[("txt file", ".csv")], defaultextension=".csv", title='Choose location to save csv',
                        initialfile='{current_date}.csv'.format(current_date=self.return_time_str()))
                else:
                    csv_location = output_path
                if csv_location != '':
                    try:
                        if '.log' in csv_location:
                            csv_location = csv_location.replace('.log', '.csv')
                        csv_location = csv_location.replace('.csv', '_plot.csv')
                        user_event_location = csv_location.replace('_plot.csv', '_user_event.csv')
                        self.decrypted_multi_tag.to_csv(csv_location)
                        self.user_events.to_csv(user_event_location, index=False)
                        self.print_function(
                            str_in='Export multi-tag csv - {path}'.format(
                                path=csv_location))
                    except Exception as e:
                        self.print_function(str_in=e.__str__())
                else:
                    self.print_function(str_in='No output location selected.')
            else:
                self.print_function(str_in='No packets received in decoded_packet mode yet.')
        else:
            if output_path is not None:
                log_path = output_path
            else:
                log_path = self.get_log_file_name()
            if '.log' in log_path:
                user_event_location = log_path.replace('.log', '_user_event.csv')
            else:
                user_event_location = log_path.replace('.csv', '_user_event.csv')
            self.user_events.to_csv(user_event_location, index=False)
            try:
                processed_log_path = log_path.replace('.log', '_packet_process.csv')
                packet_list = self.extract_packet_list_from_log(log_path=log_path)
                packet_list.to_csv(processed_log_path)
                mt_processed_log_path = log_path.replace('.log', '_statistics_process.csv')
                mt = TagCollection()
                for packet in packet_list:
                    mt.append(packet)
                stat_df = mt.get_statistics()
                stat_df.to_csv(path_or_buf=mt_processed_log_path)
                # check if csv file was created
                if isfile(processed_log_path):
                    self.print_function('processed csv file was created: {}'.format(processed_log_path))
                else:
                    self.print_function('processed csv file was not created')
                if isfile(mt_processed_log_path):
                    self.print_function('multi tag csv file was created: {}'.format(mt_processed_log_path))
                else:
                    self.print_function('multi tag csv file was not created')
            except Exception as e:
                self.print_function('processed csv file was failed due to: {}'.format(e))
                return

    def on_custom_ep(self):
        # open a new gui:
        tk_frame = Toplevel(self.ttk)
        CustomEPGui(gw_obj=self.ObjGW, print_func=self.print_function, tk_frame=tk_frame)

    def ui_update(self, state):
        # updating UI according to the new state
        if state == 'init':
            self.builder.get_object('write_box')['values'] = tuple(self.gwAllCommands)
            self.builder.get_object('macros_ddl')['values'] = tuple(macros.keys())
            # default config values:
            self.builder.get_object('energizing_pattern')['values'] = tuple(EPs_DEFAULT)
            self.builder.get_object('energizing_pattern').set(EP_DEFAULT)
            self.builder.get_object('timing_profile_on').set(TP_O_DEFAULT)
            self.builder.get_object('timing_profile_period').set(TP_P_DEFAULT)
            self.builder.get_object('pace_inter').set(PI_DEFAULT)
            self.builder.get_object('received_channel')['values'] = tuple(RCs_DEFAULT)
            self.builder.get_object('received_channel').set(RC_DEFAULT)

            self.config_param = {"energy_pattern": str(EP_DEFAULT),
                                 "received_channel": str(RC_DEFAULT),
                                 "time_profile_on": str(TP_O_DEFAULT),
                                 "time_profile_period": str(TP_P_DEFAULT),
                                 "pacer_val": str(PI_DEFAULT),
                                 "filter": "N"}

            self.builder.get_object('config_sum').insert(END, CONFIG_SUM.format(
                RC="", EP="", TP_ON="", TP_P="", PI="", F=""))
            self.builder.get_object('config_sum').see(END)
            if self.decryption_mode:
                self.builder.get_object('data_type')['values'] = tuple(DATA_TYPES)
            else:
                self.builder.get_object('data_type')['values'] = tuple(DATA_TYPES[:-1])
            self.builder.get_object('data_type').set('raw')

            self.builder.get_object('log_button')['text'] = 'Start Log'
            self.builder.get_object('log_path').insert(END, self.log_path)

            self.builder.get_variable('autoscroll_state').set(self.autoscroll_state)
            self.builder.get_variable('send_data_state').set(self.send_data_to_another_app)

            if self.decryption_mode:
                self.builder.get_object('save_to_file')['state'] = 'disabled'
                self.builder.get_object('plot_log')['state'] = 'disabled'
            self.builder.get_object('filter_id').delete(0, 'end')
            self.builder.get_object('filter_id')['state'] = 'disabled'
            if self.decryption_mode:
                self.builder.get_object('load_log')['state'] = 'enabled'
                self.builder.get_object('custom_plots')['state'] = 'enabled'

            ver_num, _ = self.ObjGW.get_latest_version_number()
            if ver_num is not None:
                self.builder.get_object('version_num').insert(END, 'new:' + ver_num)
            self.builder.get_object('version_num_cur').insert(END, 'current:')
            self.builder.get_object('version_browser')['state'] = 'disable'

        elif state == 'available_ports':
            if self.ObjGW.available_ports:
                self.print_function(str_in=f'> Finished searching for ports, available ports: '
                                           f'{", ".join(self.ObjGW.available_ports)}')
                self.builder.get_object('port_box')['values'] = tuple(self.ObjGW.available_ports)
            else:
                self.print_function(str_in="no serial ports were found. please check your connections and refresh")
            self.builder.get_object('baud_rate_box')['values'] = tuple(baud_rates)
            self.builder.get_object('port_box')['state'] = 'enabled'
            self.builder.get_object('baud_rate_box')['state'] = 'enabled'
            self.builder.get_object('baud_rate_box').set(baud_rates[0])

        elif state == 'connect':
            if self.portActive:
                # connected
                enable_disable_str = 'enabled'
                enable_disable_con_str = 'disabled'
                self.builder.get_object('version_num_cur').delete('1.0', END)
                self.builder.get_object('version_num_cur').insert(END, 'current:' + self.ObjGW.sw_version)
            else:
                # disconnected
                enable_disable_str = 'disabled'
                enable_disable_con_str = 'enabled'
                self.builder.get_object('version_num_cur').delete('1.0', END)
                self.builder.get_object('version_num_cur').insert(END, 'current:')

            self.builder.get_object('config_button')['state'] = enable_disable_str
            self.builder.get_object('energizing_pattern')['state'] = enable_disable_str
            self.builder.get_object('timing_profile_on')['state'] = enable_disable_str
            self.builder.get_object('timing_profile_period')['state'] = enable_disable_str
            self.builder.get_object('pace_inter')['state'] = enable_disable_str
            self.builder.get_object('set_filter')['state'] = enable_disable_str
            self.builder.get_object('write_button')['state'] = enable_disable_str
            self.builder.get_object('write_box')['state'] = enable_disable_str
            self.builder.get_object('macros_ddl')['state'] = enable_disable_str
            self.builder.get_object('run_macro')['state'] = enable_disable_str
            self.builder.get_object('reset_button')['state'] = enable_disable_str
            self.builder.get_object('send_data')['state'] = enable_disable_str
            self.builder.get_object('received_channel')['state'] = enable_disable_str
            self.builder.get_object('data_type')['state'] = enable_disable_str
            self.builder.get_object('update_button')['state'] = enable_disable_str
            self.builder.get_object('version_path')['state'] = enable_disable_str
            self.builder.get_object('version_browser')['state'] = enable_disable_str
            # self.builder.get_object('custom_ep')['state'] = enable_disable_str  #TODO remove comment when fw support

            self.builder.get_object('port_box')['state'] = enable_disable_con_str
            self.builder.get_object('baud_rate_box')['state'] = enable_disable_con_str

        elif state == 'config':
            self.builder.get_object('config_sum').delete(1.0, END)
            self.builder.get_object('config_sum').insert(END,
                                                         CONFIG_SUM.format(RC=self.config_param["received_channel"],
                                                                           EP=self.config_param["energy_pattern"],
                                                                           TP_ON=self.config_param["time_profile_on"],
                                                                           TP_P=self.config_param[
                                                                               "time_profile_period"],
                                                                           PI=self.config_param["pacer_val"],
                                                                           F=self.config_param["filter"]))
            self.builder.get_object('config_sum').see(END)

    def on_log_browser(self):
        path_loc = filedialog.asksaveasfilename(
            filetypes=[("txt file", ".log")], defaultextension=".log", title='Choose location to save log',
            initialfile='gw_log_{}.log'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
        self.builder.get_object('log_path').delete(0, 'end')
        self.builder.get_object('log_path').insert(END, path_loc)

    def on_version_browser(self):
        path_loc = filedialog.askopenfilename(
            filetypes=[("txt file", ".zip")], defaultextension=".zip", title='Choose version file location')
        self.builder.get_object('version_path').delete(0, 'end')
        self.builder.get_object('version_path').insert(END, path_loc)

    def print_function(self, str_in):
        try:
            recv_box = self.builder.get_object('recv_box')
            recv_box.insert(END, str_in + '\n')
            recv_box.config()
            if self.autoscroll_state:
                recv_box.see(END)
            if self.log_state:
                self.logger.info(str_in)
        except Exception as e:
            print('print function failed due to: {}'.format(e))

    def init_live_plot(self):
        self.live_plots_event = threading.Event()
        self.reset_live_plot()

        self.dash_app = dash.Dash(__name__)
        self.dash_app.title = 'Wiliot - Live view'
        app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

        build_layout = [html.Div([
            html.H1("Wiliot - Live plot - BETA"),
            html.A([
                html.Img(
                    src='https://www.wiliot.com/src/uploads/Wiliotlogo.png',
                    style={
                        'height': '8%',
                        'width': '8%',
                        'float': 'right',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 0,
                        'padding-right': 0,
                        'padding-bottom': 10,

                    })
            ], href='https://www.wiliot.com/')]),
            html.Div([
                html.H3("Live view of {packet_attribute} over time.".format(
                    packet_attribute=LIVE_PLOTS_ATTRIBUTES[0])
                ),
                dcc.Graph(
                    id='live-graph-scatter-0',
                    animate=LIVE_PLOTS_ANIMATE, style={'height': '90vh'})]),
            html.Div([
                html.H3(
                    "Live view of {packet_attribute} over time.".format(
                        packet_attribute=LIVE_PLOTS_ATTRIBUTES[1])),
                dcc.Graph(
                    id='live-graph-scatter-1',
                    animate=LIVE_PLOTS_ANIMATE), ]),
            html.Div([
                html.H3(
                    "Live view of {packet_attribute} over time.".format(
                        packet_attribute=LIVE_PLOTS_ATTRIBUTES[2])),
                dcc.Graph(
                    id='live-graph-scatter-2',
                    animate=LIVE_PLOTS_ANIMATE), ]),
            html.Div([
                html.H3(
                    "Live view of {packet_attribute} over time.".format(
                        packet_attribute=LIVE_PLOTS_ATTRIBUTES[3])),
                dcc.Graph(
                    id='live-graph-scatter-3',
                    animate=LIVE_PLOTS_ANIMATE), ]),
            html.Div([
                html.H3(
                    "Live view of {packet_attribute} over time.".format(
                        packet_attribute=LIVE_PLOTS_ATTRIBUTES[4])),
                dcc.Graph(
                    id='live-graph-scatter-4',
                    animate=LIVE_PLOTS_ANIMATE),

                dcc.Interval(
                    id='graph-update',
                    interval=1000,
                    n_intervals=0
                )
            ])
        ]

        self.dash_app.layout = html.Div(build_layout)

        @self.dash_app.callback(
            Output('live-graph-scatter-{idx}'.format(idx=0), 'figure'),
            [Input('graph-update', 'n_intervals')],
        )
        def update_graph_scatter(n):
            traces = []

            # IMPLEMENT FILTER HERE - LO PROXIMITY VALUE IS IN self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]
            n = 6
            num_of_outliers = 2
            lo_prox_list_x = list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X'])
            lo_prox_list_y = list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['Y'])

            current_sample_x = len(list(self.live_plots_data['filter']['X']))
            current_sample_y = len(list(self.live_plots_data['filter']['Y']))

            try:
                while len(lo_prox_list_x) >= n + current_sample_x:
                    y_total = lo_prox_list_y[current_sample_y:current_sample_y + n]
                    x_total = lo_prox_list_x[current_sample_x:current_sample_x + n]
                    y_total.sort()
                    y_total = [x for x in y_total if x > 2481 or (x > 2460 and x < 2479)]
                    if len(y_total) < num_of_outliers * 2:
                        y_total = self.live_plots_data['filter']['Y'][-1]
                    else:
                        y_total = y_total[num_of_outliers:-num_of_outliers]

                    self.live_plots_data['filter']['Y'].append(np.average(y_total))
                    self.live_plots_data['filter']['X'].append(x_total[-1])
                    current_sample_x = len(list(self.live_plots_data['filter']['X']))

            except Exception as e:
                print(e)
            traces.append(plotly.graph_objs.Scatter(
                x=list(self.live_plots_data['filter']['X']),
                y=list(self.live_plots_data['filter']['Y']),
                name='filtered'.format(idx=1),
                mode='lines+markers',
                line={"color": "#42C4F7", },
            ))
            # DO NOT CHANGE BLOCK BELOW
            traces.append(plotly.graph_objs.Scatter(
                x=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X']),
                y=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['Y']),
                name='lo_max_prox'.format(idx=0),
                mode='lines+markers',
                line={"color": "#f74242", },
            ))

            try:
                if len(self.live_plots_data['filter']['Y']) > LIVE_PLOTS_HISTORY:
                    y_range = [
                        min(list(self.live_plots_data['filter']['Y'])[-LIVE_PLOTS_HISTORY:]) - 2,
                        max(list(self.live_plots_data['filter']['Y'])[-LIVE_PLOTS_HISTORY:]) + 2]
                else:
                    y_range = [
                        min(self.live_plots_data['filter']['Y']) - 2,
                        max(self.live_plots_data['filter']['Y']) + 2]

                return {
                    'data': traces, 'layout': go.Layout(
                        xaxis=dict(range=[
                            max(max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X']) - LIVE_PLOTS_HISTORY, 0),
                            max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X'])]),
                        yaxis=dict(range=y_range)
                        # plot_bgcolor=app_color["graph_bg"],
                        # paper_bgcolor=app_color["graph_bg"],
                        # font={"color": "#fff"},
                        # height=500,
                    )}
            except ValueError as ve:
                pass
            except Exception as e:
                print('problem during update_graph scatter: {}'.format(e))

        @self.dash_app.callback(
            Output('live-graph-scatter-{idx}'.format(idx=1), 'figure'),
            [Input('graph-update', 'n_intervals')],
        )
        def update_graph_scatter(n):
            traces = []

            traces.append(plotly.graph_objs.Scatter(
                x=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[1]]['X']),
                y=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[1]]['Y']),
                name='Scatter {idx}'.format(idx=1),
                mode='lines+markers',
            ))
            try:
                return {
                    'data': traces, 'layout': go.Layout(
                        xaxis=dict(range=[
                            max(max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X']) - LIVE_PLOTS_HISTORY, 0),
                            max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X'])]),
                    )}
            except ValueError as ve:
                pass
            except Exception as e:
                print(e)

        @self.dash_app.callback(
            Output('live-graph-scatter-{idx}'.format(idx=2), 'figure'),
            [Input('graph-update', 'n_intervals')],
        )
        def update_graph_scatter(n):
            traces = []
            traces.append(plotly.graph_objs.Scatter(
                x=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[2]]['X']),
                y=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[2]]['Y']),
                name='Scatter {idx}'.format(idx=2),
                mode='lines+markers',
            ))
            # )
            try:
                return {
                    'data': traces, 'layout': go.Layout(
                        xaxis=dict(range=[
                            max(max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X']) - LIVE_PLOTS_HISTORY, 0),
                            max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X'])]),
                        # yaxis=dict(range=[
                        #     min(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[2]]['Y']),
                        #     max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[2]]['Y'])]),
                    )}
            except ValueError as ve:
                pass
            except Exception as e:
                print(e)

        @self.dash_app.callback(
            Output('live-graph-scatter-{idx}'.format(idx=3), 'figure'),
            [Input('graph-update', 'n_intervals')],
        )
        def update_graph_scatter(n):
            traces = []
            traces.append(plotly.graph_objs.Scatter(
                x=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[3]]['X']),
                y=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[3]]['Y']),
                name='Scatter {idx}'.format(idx=3),
                mode='lines+markers',
            ))
            # )

            try:
                return {
                    'data': traces, 'layout': go.Layout(
                        xaxis=dict(range=[
                            max(max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X']) - LIVE_PLOTS_HISTORY, 0),
                            max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X'])]),
                        # yaxis=dict(range=[
                        #     min(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[3]]['Y']),
                        #     max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[3]]['Y'])]),
                    )}
            except ValueError as ve:
                pass
            except Exception as e:
                print(e)

        @self.dash_app.callback(
            Output('live-graph-scatter-{idx}'.format(idx=4), 'figure'),
            [Input('graph-update', 'n_intervals')],
        )
        def update_graph_scatter(n):
            traces = []
            traces.append(plotly.graph_objs.Scatter(
                x=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[4]]['X']),
                y=list(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[4]]['Y']),
                name='Scatter {idx}'.format(idx=4),
                mode='lines+markers',
            ))
            # )
            try:
                return {
                    'data': traces, 'layout': go.Layout(
                        xaxis=dict(range=[
                            max(max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X']) - LIVE_PLOTS_HISTORY, 0),
                            max(self.live_plots_data[LIVE_PLOTS_ATTRIBUTES[0]]['X'])]),
                    )}
            except ValueError as ve:
                pass
            except Exception as e:
                print(e)

        if LIVE_PLOTS_ENABLE:
            live_plot_listener = threading.Thread(target=self.live_plot_task, args=())
            self.live_plot_thread = live_plot_listener.start()

    def reset_live_plot(self):
        self.live_plots_data = {}
        self.print_function('Live plotting avaialbe in http://127.0.0.1:8050/')
        for live_plots_attribute in LIVE_PLOTS_ATTRIBUTES:
            self.live_plots_data[live_plots_attribute] = {'X': deque().copy(),
                                                          'Y': deque().copy()}
            self.live_plots_data['filter'] = {'X': deque().copy(),
                                              'Y': deque().copy()}
            # self.live_plots_data[live_plots_attribute]['X'].append(0)
            # self.live_plots_data[live_plots_attribute]['Y'].append(0)

    def live_plot_task(self):
        self.dash_app.run_server(dev_tools_hot_reload=False, debug=False)
        while True:
            time.sleep(1)
            if self.live_plots_event.is_set():
                break
        print('Live plotting has been stopped')


class CustomEPGui(object):

    def __init__(self, gw_obj=None, print_func=None, tk_frame=None):
        self.close_requested = False
        if gw_obj is None:
            self.gw_obj = WiliotGateway()
        else:
            self.gw_obj = gw_obj
        if print_func is None:
            self.print_func = print
        else:
            self.print_func = print_func
        self.ep_builder = pygubu.Builder()
        ep_ui_file = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils'), 'custom_ep.ui')
        self.ep_builder.add_from_file(ep_ui_file)
        if tk_frame:
            self.ttk_ep = tk_frame
        else:
            self.ttk_ep = Tk()

        self.ttk_ep.title('Wiliot Custom Energy Pattern')
        self.custom_ep_window = self.ep_builder.get_object('custom_ep_window', self.ttk_ep)
        self.ep_builder.connect_callbacks(self)
        self.ttk_ep.lift()
        self.ttk_ep.attributes("-topmost", True)
        # update ui
        self.energy_power_2_4 = [p['abs_power'] for p in valid_output_power_vals]
        self.ep_builder.get_object('beacon_2_4_power')['values'] = tuple([self.energy_power_2_4[-1] - b
                                                                          for b in valid_bb])
        self.ep_builder.get_object('beacon_2_4_power').set(self.energy_power_2_4[-1])
        self.ep_builder.get_object('energy_2_4_power')['values'] = tuple(self.energy_power_2_4)
        self.ep_builder.get_object('energy_2_4_power').set(self.energy_power_2_4[-1])
        self.ep_builder.get_object('energy_sub1g_power')['values'] = tuple(valid_sub1g_output_power)
        self.ep_builder.get_object('energy_sub1g_power').set(valid_sub1g_output_power[-1])
        font = Font(family="Segoe UI", size=12)
        self.ttk_ep.option_add("*TCombobox*Listbox*Font", font)
        self.ttk_ep.option_add("*TCombobox*Font", font)
        self.ttk_ep.protocol("WM_DELETE_WINDOW", self.close_window)
        self.ttk_ep.after_idle(self.periodic_call)
        self.ttk_ep.mainloop()

    def on_set_custom_ep(self):
        custom_ep_dict = {'scan_ch': None, 'period_2_4': None, 'beacon_to_beacon': None, 'beacon_to_energy': None,
                          'beacon_2_4_duration': None, 'beacon_2_4_frequencies': None, 'beacon_2_4_power': None,
                          'energy_2_4_duration': None, 'energy_2_4_frequencies': None, 'energy_2_4_power': None,
                          'period_sub1g': None,
                          'energy_sub1g_duration': None, 'energy_sub1g_frequencies': None, 'energy_sub1g_power': None
                          }

        def extract_val(field_name):
            try:
                if 'frequencies' in field_name:
                    # extract a list:
                    all_freq = self.ep_builder.get_object(field_name).get()
                    all_freq = all_freq.replace(' ', '')
                    all_freq = all_freq.split(',')
                    val_list = []
                    for f in all_freq:
                        if f != '':
                            val_list.append(int(f))
                    return val_list
                else:
                    return int(self.ep_builder.get_object(field_name).get())
            except Exception as e:
                print('failed to extract the value of field {} due to {}'.format(field_name, e))

        for k in custom_ep_dict.keys():
            custom_ep_dict[k] = extract_val(k)

        custom_gw_commands = []
        if custom_ep_dict['scan_ch'] is not None:
            custom_gw_commands.append('!scan_ch {} 37'.format(custom_ep_dict['scan_ch']))

        if custom_ep_dict['period_2_4'] is not None:
            custom_gw_commands.append('!set_2_4_ghz_time_period {}'.format(custom_ep_dict['period_2_4']))

        if custom_ep_dict['beacon_2_4_duration'] is not None and custom_ep_dict['beacon_2_4_frequencies'] is not None:
            cmd = '!set_beacons_pattern {} {}'.format(custom_ep_dict['beacon_2_4_duration'],
                                                      len(custom_ep_dict['beacon_2_4_frequencies']))
            for f in custom_ep_dict['beacon_2_4_frequencies']:
                cmd += ' {}'.format(f)
            if custom_ep_dict['beacon_to_beacon'] is not None:
                cmd += ' {}'.format(custom_ep_dict['beacon_to_beacon'])
                if custom_ep_dict['beacon_to_energy'] is not None:
                    cmd += ' {}'.format(custom_ep_dict['beacon_to_energy'])
            custom_gw_commands.append(cmd)

        if custom_ep_dict['beacon_2_4_power'] is not None:
            custom_gw_commands.append('!beacons_backoff {}'.format(valid_output_power_vals[-1]['abs_power'] -
                                                                   custom_ep_dict['beacon_2_4_power']))

        if custom_ep_dict['energy_2_4_frequencies'] is not None \
                and custom_ep_dict['energy_sub1g_frequencies'] is not None:
            cmd = '!set_dyn_energizing_pattern 6 {} {}'.format(len(custom_ep_dict['energy_sub1g_frequencies']) > 0,
                                                               len(custom_ep_dict['energy_2_4_frequencies']))
            for f in custom_ep_dict['energy_2_4_frequencies']:
                cmd += ' {}'.format(f)
            if custom_ep_dict['energy_2_4_duration'] is not None:
                cmd += ' {}'.format(custom_ep_dict['energy_2_4_duration'])
            custom_gw_commands.append(cmd)

        if custom_ep_dict['energy_2_4_power'] is not None:
            abs_output_power_index = self.energy_power_2_4.index(custom_ep_dict['energy_2_4_power'])
            custom_gw_commands.append(
                '!bypass_pa {}'.format(valid_output_power_vals[abs_output_power_index]['bypass_pa']))
            custom_gw_commands.append(
                '!output_power {}'.format(valid_output_power_vals[abs_output_power_index]['gw_output_power']))

        if custom_ep_dict['period_sub1g'] is not None:
            custom_gw_commands.append('!set_sub_1_ghz_time_period {}'.format(custom_ep_dict['period_sub1g']))

        if custom_ep_dict['energy_sub1g_frequencies'] is not None:
            cmd = '!set_sub_1_ghz_energy_params {}'.format(len(custom_ep_dict['energy_sub1g_frequencies']))
            for f in custom_ep_dict['energy_sub1g_frequencies']:
                cmd += ' {}'.format(f)
            if custom_ep_dict['energy_sub1g_duration'] is not None:
                cmd += '{}'.format(custom_ep_dict['energy_sub1g_duration'])
            custom_gw_commands.append(cmd)

        if custom_ep_dict['energy_sub1g_power'] is not None:
            custom_gw_commands.append('!set_sub_1_ghz_power {}'.format(custom_ep_dict['energy_sub1g_power']))

        custom_gw_commands.append('!gateway_app')
        # send gw commands:
        for cmd in custom_gw_commands:
            rsp = self.gw_obj.write(cmd, with_ack=True)
            self.print_func('time: {}, command:{}, response:{}'.format(rsp['time'], cmd, rsp['raw']))

        self.close_requested = True
        pass

    def on_cancel_custom_ep(self):
        self.close_requested = True

    def periodic_call(self):
        if not self.close_requested:
            self.ttk_ep.after(500, self.periodic_call)

        else:
            print("Destroying Custom EP GUI at:", time.time())
            try:
                self.ttk_ep.destroy()
            except Exception as e:
                print('problem occured during exit the gui: {}'.format(e))
                exit(1)

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time())


class CustomPlotGui(object):

    def __init__(self, plot_config=None, print_func=None, tk_frame=None):
        self.close_requested = False
        if print_func is None:
            self.print_func = print
        else:
            self.print_func = print_func
        if plot_config is None:
            self.plot_config = None
        else:
            self.plot_config = plot_config
        self.plot_builder = pygubu.Builder()
        plots_ui_file = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils'),
                                     'custom_plots.ui')
        self.plot_builder.add_from_file(plots_ui_file)
        if tk_frame:
            self.ttk_plots = tk_frame
        else:
            self.ttk_plots = Tk()

        self.ttk_plots.title('Wiliot Custom plots')
        self.custom_plots_window = self.plot_builder.get_object('custom_plots_window', self.ttk_plots)
        self.plot_builder.connect_callbacks(self)

        # update ui
        self.plot_builder.get_variable('summary_cb_state').set(self.plot_config.plot_files.get('summary', True))
        self.plot_builder.get_variable('tags_detailed_cb_state').set(
            self.plot_config.plot_files.get('tags_detailed', True))

        self.plot_builder.get_variable('analysis_plot_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('analysis_plot', True))
        self.plot_builder.get_variable('rx_tx_intervals_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('rx_tx_intervals', True))
        self.plot_builder.get_variable('wkup_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('wkup_metrics', True))
        self.plot_builder.get_variable('aux_meas_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('aux_meas_metrics', True))
        self.plot_builder.get_variable('lo_dco_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('lo_dco_metrics', True))
        self.plot_builder.get_variable('sprinkler_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('sprinkler_metrics', True))
        self.plot_builder.get_variable('sym_dco_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('sym_dco_metrics', True))
        self.plot_builder.get_variable('sensing_metrics_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('sensing_metrics', True))
        self.plot_builder.get_variable('temp_comp_and_tuning_cb_state').set(
            self.plot_config.detailed_tag_graphs.get('temp_comp_and_tuning', True))

        # self.ttk_plots.lift()
        # self.ttk_plots.attributes("-topmost", True)

        self.ttk_plots.protocol("WM_DELETE_WINDOW", self.close_window)
        self.ttk_plots.after_idle(self.periodic_call)
        self.ttk_plots.mainloop()

    def on_set_custom_plot(self):
        self.plot_config.plot_files['summary'] = self.plot_builder.get_variable('summary_cb_state').get()
        self.plot_config.plot_files['tags_detailed'] = self.plot_builder.get_variable('tags_detailed_cb_state').get()

        self.plot_config.detailed_tag_graphs['analysis_plot'] = self.plot_builder.get_variable(
            'analysis_plot_cb_state').get()
        self.plot_config.detailed_tag_graphs['rx_tx_intervals'] = self.plot_builder.get_variable(
            'rx_tx_intervals_cb_state').get()
        self.plot_config.detailed_tag_graphs['wkup_metrics'] = self.plot_builder.get_variable(
            'wkup_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['aux_meas_metrics'] = self.plot_builder.get_variable(
            'aux_meas_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['lo_dco_metrics'] = self.plot_builder.get_variable(
            'lo_dco_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['sprinkler_metrics'] = self.plot_builder.get_variable(
            'sprinkler_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['sym_dco_metrics'] = self.plot_builder.get_variable(
            'sym_dco_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['sensing_metrics'] = self.plot_builder.get_variable(
            'sensing_metrics_cb_state').get()
        self.plot_config.detailed_tag_graphs['temp_comp_and_tuning'] = self.plot_builder.get_variable(
            'temp_comp_and_tuning_cb_state').get()

        self.close_requested = True
        pass

    def on_cancel_custom_plot(self):
        self.close_requested = True

    def periodic_call(self):
        if not self.close_requested:
            self.ttk_plots.after(500, self.periodic_call)

        else:
            print("Destroying Custom EP GUI at:", time.time())
            try:
                self.ttk_plots.destroy()
            except Exception as e:
                print('problem occured during exit the gui: {}'.format(e))
                exit(1)

    def close_window(self):
        self.close_requested = True
        print("User requested close at:", time.time())


if __name__ == '__main__':
    # Run the UI
    GWApp = GatewayUI()
    # CustomPlotGui(plot_config=plot_config())
