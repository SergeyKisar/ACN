from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QComboBox, QCheckBox
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import configparser
import webbrowser
import platform
import paramiko
import logging
import ftplib
import glob
import yaml
import time
import sys
import os
import re

NAME_MAP = {
    'Bel-TOL-IX_sw0': '172.16.2.254',
    'Bel-REP-IX_sw0': '172.16.3.254',
    'Bel-OSK-IX_sw0': '172.16.4.254',
    'Bel-ZAS-IX_sw0': '172.16.5.254',
    'Bel-NOV-IX_sw0': '172.16.6.254',
    'Bel-LUN-IX_sw0': '172.16.7.254',
    'Bel-PUL-IX_sw0': '172.16.8.254',
    'Bel-STU-IX_sw0': '172.16.9.254',
    'Bel-SUM-IX_sw0': '172.16.10.254'
}

NAME_MAP_sw = 0

NAME_MAP_olt = {
 'Bel-TOL-IX_olt_1': '172.16.2.101',
 'Bel-TOL-IX_olt_2': '172.16.2.102',
 'Bel-TOL-IX_olt_3': '172.16.2.103',
 'Bel-TOL-IX_olt_4': '172.16.2.104',
 'Bel-TOL-IX_olt_5': '172.16.2.105',
 'Bel-TOL-IX_olt_6': '172.16.2.106',
 'Bel-TOL-IX_olt_7': '172.16.2.107',
 'Bel-TOL-IX_olt_8': '172.16.2.108',
 'Bel-TOL-IX_olt_9': '172.16.2.109',
 'Bel-TOL-IX_olt_10': '172.16.2.110',
 'Bel-REP-IX_olt_1': '172.16.3.101',
 'Bel-REP-IX_olt_2': '172.16.3.102',
 'Bel-REP-IX_olt_3': '172.16.3.103',
 'Bel-REP-IX_olt_4': '172.16.3.104',
 'Bel-REP-IX_olt_5': '172.16.3.105',
 'Bel-REP-IX_olt_6': '172.16.3.106',
 'Bel-REP-IX_olt_7': '172.16.3.107',
 'Bel-REP-IX_olt_8': '172.16.3.108',
 'Bel-REP-IX_olt_9': '172.16.3.109',
 'Bel-REP-IX_olt_10': '172.16.3.110',
 'Bel-OSK-IX_olt_1': '172.16.4.101',
 'Bel-OSK-IX_olt_2': '172.16.4.102',
 'Bel-OSK-IX_olt_3': '172.16.4.103',
 'Bel-OSK-IX_olt_4': '172.16.4.104',
 'Bel-OSK-IX_olt_5': '172.16.4.105',
 'Bel-OSK-IX_olt_6': '172.16.4.106',
 'Bel-OSK-IX_olt_7': '172.16.4.107',
 'Bel-OSK-IX_olt_8': '172.16.4.108',
 'Bel-OSK-IX_olt_9': '172.16.4.109',
 'Bel-OSK-IX_olt_10': '172.16.4.110',
 'Bel-ZAS-IX_olt_1': '172.16.5.101',
 'Bel-ZAS-IX_olt_2': '172.16.5.102',
 'Bel-ZAS-IX_olt_3': '172.16.5.103',
 'Bel-ZAS-IX_olt_4': '172.16.5.104',
 'Bel-ZAS-IX_olt_5': '172.16.5.105',
 'Bel-ZAS-IX_olt_6': '172.16.5.106',
 'Bel-ZAS-IX_olt_7': '172.16.5.107',
 'Bel-ZAS-IX_olt_8': '172.16.5.108',
 'Bel-ZAS-IX_olt_9': '172.16.5.109',
 'Bel-ZAS-IX_olt_10': '172.16.5.110',
 'Bel-NOV-IX_olt_1': '172.16.6.101',
 'Bel-NOV-IX_olt_2': '172.16.6.102',
 'Bel-NOV-IX_olt_3': '172.16.6.103',
 'Bel-NOV-IX_olt_4': '172.16.6.104',
 'Bel-NOV-IX_olt_5': '172.16.6.105',
 'Bel-NOV-IX_olt_6': '172.16.6.106',
 'Bel-NOV-IX_olt_7': '172.16.6.107',
 'Bel-NOV-IX_olt_8': '172.16.6.108',
 'Bel-NOV-IX_olt_9': '172.16.6.109',
 'Bel-NOV-IX_olt_10': '172.16.6.110',
 'Bel-LUN-IX_olt_1': '172.16.7.101',
 'Bel-LUN-IX_olt_2': '172.16.7.102',
 'Bel-LUN-IX_olt_3': '172.16.7.103',
 'Bel-LUN-IX_olt_4': '172.16.7.104',
 'Bel-LUN-IX_olt_5': '172.16.7.105',
 'Bel-LUN-IX_olt_6': '172.16.7.106',
 'Bel-LUN-IX_olt_7': '172.16.7.107',
 'Bel-LUN-IX_olt_8': '172.16.7.108',
 'Bel-LUN-IX_olt_9': '172.16.7.109',
 'Bel-LUN-IX_olt_10': '172.16.7.110',
 'Bel-PUL-IX_olt_1': '172.16.8.101',
 'Bel-PUL-IX_olt_2': '172.16.8.102',
 'Bel-PUL-IX_olt_3': '172.16.8.103',
 'Bel-PUL-IX_olt_4': '172.16.8.104',
 'Bel-PUL-IX_olt_5': '172.16.8.105',
 'Bel-PUL-IX_olt_6': '172.16.8.106',
 'Bel-PUL-IX_olt_7': '172.16.8.107',
 'Bel-PUL-IX_olt_8': '172.16.8.108',
 'Bel-PUL-IX_olt_9': '172.16.8.109',
 'Bel-PUL-IX_olt_10': '172.16.8.110',
 'Bel-STU-IX_olt_1': '172.16.9.101',
 'Bel-STU-IX_olt_2': '172.16.9.102',
 'Bel-STU-IX_olt_3': '172.16.9.103',
 'Bel-STU-IX_olt_4': '172.16.9.104',
 'Bel-STU-IX_olt_5': '172.16.9.105',
 'Bel-STU-IX_olt_6': '172.16.9.106',
 'Bel-STU-IX_olt_7': '172.16.9.107',
 'Bel-STU-IX_olt_8': '172.16.9.108',
 'Bel-STU-IX_olt_9': '172.16.9.109',
 'Bel-STU-IX_olt_10': '172.16.9.110',
 'Bel-SUM-IX_olt_1': '172.16.10.101',
 'Bel-SUM-IX_olt_2': '172.16.10.102',
 'Bel-SUM-IX_olt_3': '172.16.10.103',
 'Bel-SUM-IX_olt_4': '172.16.10.104',
 'Bel-SUM-IX_olt_5': '172.16.10.105',
 'Bel-SUM-IX_olt_6': '172.16.10.106',
 'Bel-SUM-IX_olt_7': '172.16.10.107',
 'Bel-SUM-IX_olt_8': '172.16.10.108',
 'Bel-SUM-IX_olt_9': '172.16.10.109',
 'Bel-SUM-IX_olt_10': '172.16.10.110'
}

def set_temp_path():
    os_type = platform.system()
    if os_type == "Windows":
        path_temp = os.path.join(os.environ["APPDATA"], "Script_ACN_tmp")
    elif os_type == "Linux":
        path_temp = "/var/tmp/Script_ACN_tmp"
    else:
        path_temp = "/temp"
    if not os.path.exists(path_temp):
        os.makedirs(path_temp)

    return path_temp

def initialize_config(filename):
    default_config = {
        'UserLDAP': '',
        'PassLDAP': '',
        'UserOLT': 'root',
        'PassOLT': 'admin',
        'ServerFTP': '172.16.254.13',
        'UserFTP': 'ftpuser',
        'PassFTP': 'Ftp-0815'
    }

    config = configparser.ConfigParser()
    config['DEFAULT'] = default_config

    if not os.path.exists(filename):
        with open(filename, 'w') as configfile:
            config.write(configfile)
            logging.info(f"Файл конфигурации {filename} создан с настройками по умолчанию.")
    else:
        config.read(filename)

    return config

def validate_config(config):
    required_sections = ['DEFAULT']
    required_keys = ['UserLDAP', 'PassLDAP', 'UserOLT', 'PassOLT', 'ServerFTP', 'UserFTP', 'PassFTP']
    is_config_broken = False
    is_config_incomplete = False

    for section in required_sections:
        if section in config:
            for key in required_keys:
                if key not in config[section]:
                    logging.warning(f"Отсутствует ключ '{key}' в разделе '{section}' файла конфигурации.")
                    is_config_incomplete = True
        else:
            logging.error(f"Отсутствует раздел '{section}' в файле конфигурации.")
            is_config_broken = True

    if is_config_broken:
        logging.error("Файл конфига сломан.")
    elif is_config_incomplete:
        logging.warning("Файл конфига загружен, но он не полон.")
    else:
        logging.info("Файл конфига успешно загружен.")

    return not is_config_broken

path_temp = set_temp_path()
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = "Script_ACN.log" 
file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setFormatter(log_formatter)
logging.basicConfig(handlers=[file_handler], level=logging.INFO)

class Tab1(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.create_tab1_ui()
        self.path_temp = set_temp_path()

    def create_tab1_ui(self):
        
        logging.info(f"Путь до папки с временными файлами: {path_temp}")
        self.name_map = NAME_MAP

        self.node_selector = QComboBox(self)
        self.node_selector.addItems(self.name_map.keys())
        self.node_selector.setGeometry(35, 20, 200, 30) 
        self.node_selector.currentIndexChanged.connect(self.update_olt_selector) 
        self.node_selector.currentIndexChanged.connect(self.update_switch_selector)

        ldap_login_label = QLabel("Логин LDAP:", self)
        ldap_login_label.setGeometry(20, 70, 100, 20)
        self.ldap_login = QLineEdit(self.config['UserLDAP'], self) 
        self.ldap_login.setGeometry(110, 60, 130, 30)  
        
        ldap_password_label = QLabel("Пароль LDAP:", self)
        ldap_password_label.setGeometry(20, 110, 100, 20)
        self.ldap_password = QLineEdit(self.config['PassLDAP'], self)
        self.ldap_password.setGeometry(110, 100, 130, 30)

        self.ftth_checkbox = QCheckBox("FTTH", self)
        self.ftth_checkbox.setGeometry(20, 140, 100, 30)  
        self.ftth_checkbox.setChecked(True)
        self.ftth_checkbox.stateChanged.connect(self.update_switch_selector)
        self.ftth_checkbox.toggled.connect(self.update_switch_selector)

        self.olt_checkbox = QCheckBox("OLT", self)
        self.olt_checkbox.setGeometry(130, 140, 100, 30) 

        olt_login_label = QLabel("Логин OLT:", self)
        olt_login_label.setGeometry(250, 70, 100, 20)
        olt_login_label.setVisible(False)
        self.olt_login = QLineEdit(self.config['UserOLT'], self) 
        self.olt_login.setGeometry(340, 60, 130, 30)
        self.olt_login.setVisible(False)

        olt_password_label = QLabel("Пароль OLT:", self)
        olt_password_label.setGeometry(250, 110, 100, 20)
        olt_password_label.setVisible(False)
        self.olt_password = QLineEdit(self.config['PassOLT'], self) 
        self.olt_password.setGeometry(340, 100, 130, 30)
        self.olt_password.setVisible(False)

        self.olt_selector = QComboBox(self)
        self.olt_selector.setGeometry(250, 20, 200, 30)
        self.update_olt_selector(0)
        self.olt_selector.setVisible(False)

        self.connect_button = QPushButton("Подключиться", self)
        self.connect_button.setGeometry(300, 170, 120, 30)
        self.connect_button.clicked.connect(self.button1)

        self.Clear_button = QPushButton("Clear Temp", self)
        self.Clear_button.setGeometry(35, 170, 120, 30)
        self.Clear_button.clicked.connect(self.button2)

        self.olt_checkbox.toggled.connect(lambda checked: self.toggle_olt_fields(checked, olt_login_label, olt_password_label))
        self.ftth_checkbox.toggled.connect(self.on_ftth_toggled)

        self.switch_selector = QComboBox(self)
        self.switch_selector.setGeometry(250, 20, 200, 30)
        self.switch_selector.setVisible(False)
        self.update_switch_selector()

        self.pon_port_selector = QComboBox(self)
        self.pon_port_selector.setGeometry(470, 20, 200, 30) 
        self.pon_port_selector.addItems([f'PON_{i}' for i in range(1, 17)])
        self.pon_port_selector.setVisible(False)

    def update_switch_selector(self):
        selected_node = self.node_selector.currentText()
        if selected_node.startswith('Bel-KAR-IX') and self.ftth_checkbox.isChecked():
            self.switch_selector.clear()
            self.switch_selector.addItems(NAME_MAP_sw.keys())
            self.switch_selector.setVisible(True)
        else:
            self.switch_selector.setVisible(False)

    def update_olt_selector(self, index):
        selected_node = self.node_selector.currentText().split('_')[0]
        self.olt_selector.clear()
        for olt_name in NAME_MAP_olt.keys():
            if olt_name.startswith(f"{selected_node}_"):
                self.olt_selector.addItem(olt_name)

    def on_ftth_toggled(self, checked):
        if checked:
            self.olt_checkbox.setChecked(False)
        if not checked and not self.olt_checkbox.isChecked():
            self.olt_checkbox.setChecked(True)

    def toggle_olt_fields(self, checked, olt_login_label, olt_password_label):
        self.olt_login.setVisible(checked)
        self.olt_password.setVisible(checked)
        olt_login_label.setVisible(checked)
        olt_password_label.setVisible(checked)
        self.olt_selector.setVisible(checked)
        self.pon_port_selector.setVisible(checked)  
        if not checked and not self.ftth_checkbox.isChecked():
            self.ftth_checkbox.setChecked(True)
        if checked:
            self.ftth_checkbox.setChecked(False)

    def button1(self):
        temp_folder_path = set_temp_path()
        selected_node = self.node_selector.currentText()
        selected_switch = self.switch_selector.currentText()
        selected_olt = self.olt_selector.currentText()

        if self.ftth_checkbox.isChecked() and not selected_node.startswith('Bel-KAR-IX'):
            self.create_abon_1(selected_switch)

        elif self.ftth_checkbox.isChecked() and selected_node.startswith('Bel-KAR-IX') and (selected_switch in ['Bel-KAR-IX_sw0_NEW', 'Bel-KAR-IX_sw0_OLD']):
            self.create_abon_1(selected_switch)

        elif self.ftth_checkbox.isChecked() and selected_node.startswith('Bel-KAR-IX') and (selected_switch not in ['Bel-KAR-IX_sw0_NEW', 'Bel-KAR-IX_sw0_OLD']):
            self.create_abon_2(selected_switch)

        elif self.olt_checkbox.isChecked() and selected_node.startswith('Bel-KAR-IX'):
            self.create_abon_3(selected_olt)

        elif self.olt_checkbox.isChecked() and not selected_node.startswith('Bel-KAR-IX'):
            self.create_abon_4(selected_olt)

    def button2(self):
        self.clear_temp_except_logs() 
        QMessageBox.information(self, "Успех", "Временные файлы удалены!")

    def create_abon_1(self, selected_switch): 
        node_name = self.node_selector.currentText()
        node_ip = self.name_map.get(node_name, "Неизвестный IP")
        logging.info(f"Создание абонента на FTTH. Узел сети: {node_name}, IP узла сети: {node_ip}")
        self.ssh_connect_node()
        self.pars_interface_node()

    def create_abon_2(self, selected_switch): 
        node_name = self.node_selector.currentText()
        node_ip = self.name_map.get(node_name, "Неизвестный IP")
        switch_name = self.switch_selector.currentText()
        switch_ip = self.name_map_sw.get(switch_name, "Неизвестный IP")
        logging.info(f"Создание абонента на FTTH. Узел сети: {node_name}, IP узла сети: {node_ip}, Свитч: {switch_name}, IP свитча: {switch_ip}")
        self.ssh_connect_node()
        self.ssh_connect_switch()
        self.pars_interface_node()
        time.sleep(3)
        self.pars_interface_switch()
        self.merge_yaml_node_switch()

    def create_abon_3(self, selected_olt):
        node_name = self.node_selector.currentText()
        node_ip = self.name_map.get(node_name, "Неизвестный IP")
        olt_ip = self.calculate_olt_ip(selected_olt)
        selected_sw0 = self.node_selector.currentText()
        logging.info(f"Создание абонента на OLT: {selected_olt}, IP узла сети: {node_ip}, IP OLT: {olt_ip}")
        self.backup_sw0()
        self.ssh_connect_olt()
        self.download_from_ftp()
        self.ssh_connect_node()
        vlans = self.extract_all_vlans(selected_sw0, self.path_temp)
        vlan_interfaces = self.extract_vlan_interfaces(selected_sw0, self.path_temp)
        pox_data = self.parse_config_for_pox(selected_sw0, self.path_temp)
        self.all_vlan_cisco_for_olt(selected_sw0, self.path_temp, vlans, vlan_interfaces)
        self.vlan_OLT_check(selected_olt, self.path_temp)
        self.parse_olt_to_yaml()
        self.pars_interface_node()
        self.merge_yaml_node_olt()
        self.filter_vlan_interfaces(selected_sw0, selected_olt, self.path_temp)
        QMessageBox.information(self, "Успех", "Данные сохранены и обработаны")

    def create_abon_4(self, selected_olt):
        node_name = self.node_selector.currentText()
        node_ip = self.name_map.get(node_name, "Неизвестный IP")
        olt_ip = self.calculate_olt_ip(selected_olt)
        selected_sw0 = self.node_selector.currentText()
        logging.info(f"Создание абонента на OLT: {selected_olt}, IP узла сети: {node_ip}, IP OLT: {olt_ip}")
        self.backup_sw0()
        self.ssh_connect_olt()
        self.download_from_ftp()
        self.ssh_connect_node()
        vlans = self.extract_all_vlans(selected_sw0, self.path_temp)
        vlan_interfaces = self.extract_vlan_interfaces(selected_sw0, self.path_temp)
        pox_data = self.parse_config_for_pox(selected_sw0, self.path_temp)
        self.all_vlan_cisco_for_olt(selected_sw0, self.path_temp, vlans, vlan_interfaces)
        self.vlan_OLT_check(selected_olt, self.path_temp)
        self.parse_olt_to_yaml()
        self.pars_interface_node()
        self.merge_yaml_node_olt()
        self.filter_vlan_interfaces(selected_sw0, selected_olt, self.path_temp)
        self.delete_temp_files_except(set_temp_path(), 'merge_yaml_node_olt.yaml')
        QMessageBox.information(self, "Успех", "Данные сохранены и обработаны")

    def calculate_olt_ip(self, selected_olt):
        olt_ip = NAME_MAP_olt.get(selected_olt, "Неизвестный IP")
        logging.info(f"Выбранный IP-адрес OLT: {olt_ip}")
        return olt_ip
    
    def ssh_connect_node(self):
        selected_name = self.node_selector.currentText()
        host = NAME_MAP.get(selected_name, None)
        if host is None:
            logging.error(f"Неизвестное имя узла: {selected_name}")
            return

        username = self.ldap_login.text()
        password = self.ldap_password.text()

        logging.info(f'Attempting to connect to {host}')
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            logging.info(f'Successfully connected to {host}')

            stdin, stdout, stderr = ssh.exec_command("show interface status")
            output = stdout.read().decode()

            temp_path = set_temp_path()
            filename = os.path.join(temp_path, f"{host.replace('.', '_')}_interface_status_node.txt")

            with open(filename, "w") as file:
                file.write(output)
            logging.info(f'Data successfully saved to file {filename}')

            ssh.close()

        except Exception as e:
            logging.error(f'Error connecting or running commands on {host}: {e}')

    def ssh_connect_switch(self):
        selected_name = self.node_selector.currentText()
        host = NAME_MAP.get(selected_name, None)
        if host is None:
            logging.error(f"Неизвестное имя узла: {selected_name}")
            return

        username = self.ldap_login.text()
        password = self.ldap_password.text()

        logging.info(f'Attempting to connect to {host}')
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            logging.info(f'Successfully connected to {host}')

            stdin, stdout, stderr = ssh.exec_command("show interface status")
            output = stdout.read().decode()

            temp_path = set_temp_path()
            filename = os.path.join(temp_path, f"{host.replace('.', '_')}_interface_status.txt")

            with open(filename, "w") as file:
                file.write(output)
            logging.info(f'Data successfully saved to file {filename}')

            ssh.close()

        except Exception as e:
            logging.error(f'Error connecting or running commands on {host}: {e}')

    def pars_interface_node(self):
        selected_node = self.node_selector.currentText()
        host = NAME_MAP.get(selected_node, None)
        if host is None:
            logging.error(f"Неизвестное имя узла: {selected_node}")
            return

        file_name = os.path.join(set_temp_path(), f"{host.replace('.', '_')}_interface_status_node.txt")

        eth_pattern = re.compile(r"^Eth1/(\d+)\s+.*\s+(999|1)\s+.*$")
        po_pattern = re.compile(r"^Po10\d+\s+")
        vlan_pattern = re.compile(r"^Vlan(\d+)\s+")
        eth_ports = []
        po_ports = []
        vlan_interfaces = []
        existing_vlans = set()

        try:
            with open(file_name, 'r') as file:
                for line in file:
                    eth_match = eth_pattern.match(line)
                    po_match = po_pattern.match(line)
                    vlan_match = vlan_pattern.match(line)

                    if eth_match and int(eth_match.group(1)) <= 48:
                        eth_port = f"Eth1/{eth_match.group(1)}"
                        if eth_port not in eth_ports:  
                            eth_ports.append(eth_port)
                    elif po_match:
                        po_ports.append(po_match.group(0).split()[0])
                    elif vlan_match:
                        vlan_id = int(vlan_match.group(1))
                        existing_vlans.add(vlan_id)

            for vlan_id in range(1, 3986):
                if vlan_id not in existing_vlans and not (1 <= vlan_id <= 1100 or 1300 <= vlan_id <= 1500):
                    vlan_interfaces.append(f"Vlan{vlan_id}")

            output = {
                'Eth_Ports': eth_ports,
                'PO_Ports': po_ports,
                'VLAN_Interfaces': vlan_interfaces
            }
            output_file = os.path.join(set_temp_path(), f"{selected_node}_node_tmp.yaml")
            with open(output_file, 'w') as file:
                yaml.dump(output, file, default_flow_style=False)
            logging.info(f"Результаты сохранены в файле '{output_file}'")

        except Exception as e:
            logging.error(f"Ошибка при обработке файла: {e}")

    def pars_interface_switch(self):
        selected_switch = self.switch_selector.currentText()
        host = NAME_MAP_sw.get(selected_switch, None)
        if host is None:
            logging.error(f"Неизвестное имя свитча: {selected_switch}")
            return

        username = self.ldap_login.text()
        password = self.ldap_password.text()

        logging.info(f'Attempting to connect to {host}')
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            logging.info(f'Successfully connected to {host}')

            stdin, stdout, stderr = ssh.exec_command("show interface status")
            output = stdout.read().decode()

            temp_path = set_temp_path()
            filename = os.path.join(temp_path, f"{host.replace('.', '_')}_interface_status_switch.txt")

            with open(filename, "w") as file:
                file.write(output)
            logging.info(f'Data successfully saved to file {filename}')

            ssh.close()

        except Exception as e:
            logging.error(f'Error connecting or running commands on {host}: {e}')

    def generate_all_pons(self):
        return {f"Pon_{x}_{y}": None for x in range(1, 17) for y in range(1, 33)}

    def parse_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            text = file.read()

        pattern = r'ont add (1[0-6]|[1-9]) ([1-9]|[12][0-9]|3[0-2]) mac-auth ([\w:]+)'

        used_pons = set()
        for match in re.finditer(pattern, text, re.DOTALL):
            x, y, _ = match.groups()
            pon = f"Pon_{x}_{y}"
            used_pons.add(pon)

        return used_pons

    def find_free_pons(self, all_pons, used_pons):
        return {pon: all_pons[pon] for pon in all_pons if pon not in used_pons}

    def parse_olt_to_yaml(self):
        selected_olt = self.olt_selector.currentText()
        selected_pon_port = self.pon_port_selector.currentText()
        selected_pon_number = selected_pon_port.split('_')[1]
        temp_path = set_temp_path()
        input_file_path = os.path.join(temp_path, f"{selected_olt}_config")
        output_file_path = os.path.join(temp_path, f"{selected_olt}_pon.yaml")
        all_pons = self.generate_all_pons()
        used_pons = self.parse_file(input_file_path)
        free_pons_list = [pon for pon in all_pons if pon.startswith(f"Pon_{selected_pon_number}_") and pon not in used_pons]
        with open(output_file_path, 'w') as yaml_file:
            yaml.dump({'Free_pon': free_pons_list}, yaml_file)
            logging.info(f"Свободные PON порты для PON {selected_pon_number} сохранены в {output_file_path}")

    def merge_yaml_node_switch(self):
        node_file = os.path.join(set_temp_path(), f"{self.node_selector.currentText()}_node_tmp.yaml")
        switch_file = os.path.join(set_temp_path(), f"{self.switch_selector.currentText()}_switch_tmp.yaml")
        output_file = os.path.join(set_temp_path(), "merge_yaml_node_switch.yaml")
        merged_data = {}
        for file in [node_file, switch_file]:
            file_key = os.path.basename(file).split('-IX')[0]
            with open(file, 'r') as f:
                data = yaml.safe_load(f) or {}
                updated_data = {f"{file_key}_{key}": value for key, value in data.items()}
                merged_data.update(updated_data)
        with open(output_file, 'w') as f:
            yaml.dump(merged_data, f)
            logging.info(f"Объединенные данные интерфейсов сохранены в {output_file}")
        for file in [node_file, switch_file]:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Файл {file} удален.")
        QMessageBox.information(self, "Успех", "Данные сохранены и обработаны")

    def merge_yaml_node_olt(self):
        node_file = os.path.join(set_temp_path(), f"{self.node_selector.currentText()}_node_tmp.yaml")
        yaml_file = os.path.join(set_temp_path(), f"{self.olt_selector.currentText()}_pon.yaml")
        output_file = os.path.join(set_temp_path(), "merge_yaml_node_olt.yaml")
        merged_data = {}
        for file in [node_file, yaml_file]:
            file_key = os.path.basename(file).split('.')[0]
            with open(file, 'r') as f:
                data = yaml.safe_load(f) or {}
                updated_data = {f"{file_key}_{key}": value for key, value in data.items()}
                merged_data.update(updated_data)
        with open(output_file, 'w') as f:
            yaml.dump(merged_data, f)
            logging.info(f"Объединенные данные из node и olt сохранены в {output_file}")
        for file in [node_file, yaml_file]:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Файл {file} удален.")

    def clear_temp_except_logs(self):
        temp_folder_path = set_temp_path()
        for filename in os.listdir(temp_folder_path):
            file_path = os.path.join(temp_folder_path, filename)
            try:
                if os.path.isfile(file_path) and not filename.endswith('.log'):
                    os.unlink(file_path)
                    logging.info(f'Временный файл удалён')
            except Exception as e:
                logging.error(f'Failed to delete {file_path}. Reason: {e}')

    def backup_sw0(self):
        selected_sw0 = self.node_selector.currentText()
        host = NAME_MAP.get(selected_sw0)
        if not host:
            logging.error(f"IP адрес для узла {selected_sw0} не найден.")
            return

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=self.config['UserLDAP'], password=self.config['PassLDAP'])
            stdin, stdout, stderr = ssh.exec_command("show running-config")
            output = stdout.read().decode('utf-8')  

            with open(os.path.join(path_temp, f"{selected_sw0}_config"), 'w') as file:
                file.write(output)
            ssh.close()
            logging.info(f"Конфигурация {selected_sw0}_config сохранена.")

        except Exception as e:
            logging.error(f"Ошибка при подключении к {selected_sw0}: {e}")

    def ssh_connect_olt(self):
        selected_olt = self.olt_selector.currentText()
        olt_ip = NAME_MAP_olt.get(selected_olt, None)
        if not olt_ip:
            logging.error(f"IP адрес для OLT {selected_olt} не найден.")
            return

        username = self.config['UserOLT']
        password = self.config['PassOLT']
        server_ftp = self.config['ServerFTP']
        user_ftp = self.config['UserFTP']
        pass_ftp = self.config['PassFTP']

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(olt_ip, username=username, password=password)
            shell = ssh.invoke_shell()

            time.sleep(1)
            shell.send('enable\n')
            time.sleep(1)
            backup_command = f"backup configuration format txt ftp {server_ftp} {user_ftp} {pass_ftp} {selected_olt}_config\n"
            shell.send(backup_command)
            time.sleep(1)  
            ssh.close()
            logging.info("Команда backup успешно отправлена.")
            time.sleep(1.5)

        except Exception as e:
            logging.error(f"Ошибка при SSH-подключении к OLT: {e}")

    def download_from_ftp(self):
        server_ftp = self.config['ServerFTP']
        user_ftp = self.config['UserFTP']
        pass_ftp = self.config['PassFTP']
        selected_olt = self.olt_selector.currentText()
        filename = f"{selected_olt}_config"

        try:
            with ftplib.FTP(server_ftp) as ftp:
                ftp.login(user=user_ftp, passwd=pass_ftp)
                logging.info(f"Успешно подключено к FTP серверу: {server_ftp}")
                local_filename = os.path.join(path_temp, filename)
                with open(local_filename, 'wb') as local_file:
                    ftp.retrbinary(f'RETR {filename}', local_file.write)
                    logging.info(f"Файл {filename} успешно скачан и сохранен в {local_filename}")
                ftp.delete(filename)
                logging.info(f"Файл {filename} удален с FTP сервера.")
        except ftplib.all_errors as e:
            logging.error(f"Ошибка FTP: {e}")

    def extract_all_vlans(self, selected_sw0, path_temp):
        config_file = os.path.join(path_temp, f"{selected_sw0}_config")
        all_vlans = set()

        with open(config_file, 'r') as f:
            for line in f:
                if line.startswith('vlan '):
                    vlan_entries = re.findall(r'(\d+)(?:-(\d+))?', line)
                    for entry in vlan_entries:
                        start = int(entry[0])
                        end = int(entry[1]) if entry[1] else start
                        all_vlans.update(range(start, end + 1))

        filtered_vlans = {vlan for vlan in all_vlans if not (1 <= vlan <= 1100 or 1300 <= vlan <= 1500)}
        return filtered_vlans

    def extract_vlan_interfaces(self, selected_sw0, path_temp):
        config_file = os.path.join(path_temp, f"{selected_sw0}_config")
        vlan_interfaces = set()

        with open(config_file, 'r') as f:
            data = f.read()

        vlan_interfaces_matches = re.findall(r'interface Vlan(\d+)', data)
        vlan_interfaces.update({int(vlan) for vlan in vlan_interfaces_matches})
        filtered_vlan_interfaces = {vlan for vlan in vlan_interfaces if not (1 <= vlan <= 1100 or 1300 <= vlan <= 1500)}
        return filtered_vlan_interfaces

    def parse_config_for_pox(self, selected_sw0, path_temp):
        config_file = os.path.join(path_temp, f"{selected_sw0}_config")

        with open(config_file, 'r') as f:
            data = f.read()

        channel_groups = {}
        interface_sections = re.split(r'(?=interface)', data)

        for section in interface_sections:
            vlan_match = re.search(r'switchport trunk allowed vlan ([\d,-]+)', section)
            group_match = re.search(r'channel-group (\d+)', section)

            if vlan_match and group_match:
                vlans = vlan_match.group(1)
                group_num = int(group_match.group(1))
                vlans_list = []
                for vlan in vlans.split(','):
                    if '-' in vlan:
                        start, end = map(int, vlan.split('-'))
                        vlans_range = list(range(start, end + 1))
                        vlans_list.extend([v for v in vlans_range if not (1 <= v <= 1100 or 1300 <= v <= 1500)])
                    else:
                        single_vlan = int(vlan)
                        if not (1 <= single_vlan <= 1100 or 1300 <= single_vlan <= 1500):
                            vlans_list.append(single_vlan)

                unique_vlans = sorted(set(vlans_list))
                duplicates = [v for v in vlans_list if vlans_list.count(v) > 1]

                if duplicates:
                    logging.info(f"Обнаружены дубликаты VLAN в {selected_sw0} port-channel {group_num}: {duplicates}")
                channel_groups[str(group_num)] = unique_vlans

        pox_yaml_file = os.path.join(path_temp, f"{selected_sw0}_pox.yaml")
        with open(pox_yaml_file, "w") as file:
            yaml.dump(channel_groups, file, default_flow_style=False)
            logging.info(f"Данные о port-channel {selected_sw0} сохранены в {pox_yaml_file}")

    def all_vlan_cisco_for_olt(self, selected_sw0, path_temp, vlans, vlan_interfaces):
        pox_yaml_file = os.path.join(path_temp, f"{selected_sw0}_pox.yaml")
        pox_data = {}
        if os.path.exists(pox_yaml_file):
            with open(pox_yaml_file, 'r') as file:
                pox_data = yaml.safe_load(file) or {}

        combined_vlans = set(vlans) | set(vlan_interfaces)
        for pox_vlans in pox_data.values():
            combined_vlans.update(pox_vlans)

        filtered_vlans = {vlan for vlan in combined_vlans if not (1 <= vlan <= 1100 or 1300 <= vlan <= 1500)}

        final_yaml_file = os.path.join(path_temp, f"{selected_sw0}_all_vlans_cisco.yaml")
        existing_vlans = set()
        if os.path.exists(final_yaml_file):
            with open(final_yaml_file, 'r') as file:
                existing_vlans = set(yaml.safe_load(file) or [])

        final_vlans = sorted(list(filtered_vlans - existing_vlans))
        with open(final_yaml_file, 'w') as yaml_file:
            yaml.dump(final_vlans, yaml_file, default_flow_style=False)
            logging.info(f"Объединенные данные VLAN сохранены в файл {final_yaml_file}")

        if os.path.exists(pox_yaml_file):
            os.remove(pox_yaml_file)
            logging.info(f"Временный файл {pox_yaml_file} удален.")

    def vlan_OLT_check(self, selected_olt, path_temp):
        config_file = os.path.join(path_temp, f"{selected_olt}_config")

        try:
            with open(config_file, "r") as file:
                content = file.read()

            lag_data = re.search(r"interface link-aggregation.*?vlan trunk (\d+) (.*?)(?= exit)", content, re.DOTALL)
            if lag_data:
                vlan_range = lag_data.group(2).replace(' ', '').replace('\n', '')
                if vlan_range:
                    vlans = self.expand_vlan_range(vlan_range)
                    filtered_vlans = [int(vlan) for vlan in vlans if self.is_vlan_valid(vlan)]
                    yaml_file = os.path.join(path_temp, f"{selected_olt}_lag.yaml")
                    with open(yaml_file, "w") as file:
                        yaml.dump(filtered_vlans, file, default_flow_style=False)
                logging.info(f"Данные LAG сохранены в файл {yaml_file}")
        except FileNotFoundError:
            logging.error(f"Файл {config_file} не найден.")

    def expand_vlan_range(self, vlan_range):
        expanded = []
        for part in re.findall(r"\d+-\d+|\d+", vlan_range):
            if '-' in part:
                start, end = map(int, part.split('-'))
                expanded.extend(map(str, range(start, end + 1)))
            else:
                expanded.append(part)
        return expanded

    def is_vlan_valid(self, vlan):
        vlan_number = int(vlan)
        return not (1 <= vlan_number <= 1100 or 1300 <= vlan_number <= 1500 or vlan_number > 3985)

    def filter_vlan_interfaces(self, selected_sw0, selected_olt, path_temp):
        olt_yaml_file = os.path.join(path_temp, f"{selected_olt}_lag.yaml")
        cisco_yaml_file = os.path.join(path_temp, f"{selected_sw0}_all_vlans_cisco.yaml")
        merge_yaml_file = os.path.join(path_temp, "merge_yaml_node_olt.yaml")

        with open(olt_yaml_file, 'r') as file:
            olt_vlans = set(yaml.safe_load(file))
        with open(cisco_yaml_file, 'r') as file:
            cisco_vlans = set(yaml.safe_load(file))
        with open(merge_yaml_file, 'r') as file:
            merge_data = yaml.safe_load(file)

        vlan_interfaces_key = f"{selected_sw0}_node_tmp_VLAN_Interfaces"
        vlan_interfaces = set(merge_data.get(vlan_interfaces_key, []))
        vlan_numbers = {int(vlan.replace('Vlan', '')) for vlan in vlan_interfaces}
        filtered_vlan_numbers = vlan_numbers - olt_vlans - cisco_vlans
        merge_data[vlan_interfaces_key] = [f"Vlan{num}" for num in filtered_vlan_numbers]
        with open(merge_yaml_file, 'w') as file:
            yaml.dump(merge_data, file, default_flow_style=False)

        logging.info(f"Файл {merge_yaml_file} обновлен.")

    def delete_temp_files_except(self, path, except_file):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) and filename != except_file:
                    os.unlink(file_path)
                    logging.info(f"Файл {filename} удален.")
            except Exception as e:
                logging.error(f"Ошибка при удалении файла {filename}: {e}")

class Tab2(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.create_tab2_ui()
        self.selected_vlan = None
        self.selected_ponf = None
        self.selected_eth = None

    def create_label(self, text, x, y, width, height, visible=True):
        label = QLabel(text, self)
        label.setGeometry(x, y, width, height)
        label.setVisible(visible)
        return label
    
    def create_tab2_ui(self):
        self.setWindowTitle("Генератор URL")
        self.setGeometry(100, 100, 600, 400)  

        self.bit_mask_input = QLineEdit("4", self)
        self.bit_mask_input.setGeometry(90, 20, 130, 30)
        self.bit_mask_label = self.create_label("BIT_MASK", 20, 20, 70, 30)

        self.counts_input = QLineEdit("4", self)
        self.counts_input.setGeometry(90, 60, 130, 30)
        self.counts_label = self.create_label("COUNTS", 20, 60, 70, 30)

        self.dns_input = QLineEdit("45.67.195.11,45.67.195.12", self)
        self.dns_input.setGeometry(90, 100, 130, 30)
        self.dns_label = self.create_label("DNS", 20, 100, 70, 30)

        self.name_pool_input = QLineEdit("XXX", self)
        self.name_pool_input.setGeometry(90, 140, 130, 30)
        self.name_pool_label = self.create_label("Name Pool", 20, 140, 70, 30)

        self.ip_subnet_input = QLineEdit("XXX", self)
        self.ip_subnet_input.setGeometry(90, 180, 130, 30)
        self.ip_subnet_label = self.create_label("IP Subnet", 20, 180, 70, 30)

        self.nas_alive_input = QLineEdit("3600", self)
        self.nas_alive_input.setGeometry(300, 20, 130, 30)
        self.nas_alive_label = self.create_label("NAS_ALIVE", 230, 20, 70, 30)

        self.nas_name_input = QLineEdit("XXX", self)
        self.nas_name_input.setGeometry(300, 60, 130, 30)
        self.nas_name_label = self.create_label("NAS_NAME", 230, 60, 70, 30)

        self.mac_input = QLineEdit("XXX", self)
        self.mac_input.setGeometry(300, 100, 130, 30)
        self.mac_label = self.create_label("MAC_cisco", 230, 100, 70, 30)

        self.onu_name_input = QLineEdit("STELS%20FD511G-X", self)
        self.onu_name_input.setGeometry(550, 20, 130, 30)
        self.onu_name_label = self.create_label("ONU_NAME", 450, 20, 100, 30)
        self.onu_name_label.setVisible(False)
        self.onu_name_input.setVisible(False)

        self.abon_name_input = QLineEdit("XXX", self)
        self.abon_name_input.setGeometry(550, 60, 130, 30)
        self.abon_name_label = self.create_label("abon_name", 450, 60, 100, 30)

        self.mac_onu_input = QLineEdit("00:00:00:00:00:00", self)
        self.mac_onu_input.setGeometry(550, 100, 130, 30)
        self.mac_onu_label = self.create_label("MAC_ONU", 450, 100, 100, 30)
        self.mac_onu_label.setVisible(False)
        self.mac_onu_input.setVisible(False)

        self.onu_serial_input = QLineEdit("S000-0000000000", self)
        self.onu_serial_input.setGeometry(550, 140, 130, 30)
        self.onu_serial_label = self.create_label("ONU_SERIAL", 450, 140, 100, 30)
        self.onu_serial_label.setVisible(False)
        self.onu_serial_input.setVisible(False)

        self.sfp_name_input = QLineEdit(self)
        self.sfp_name_input.setGeometry(550, 20, 130, 30)
        self.sfp_name_label = self.create_label("SFP_NAME", 450, 20, 100, 30)
        self.sfp_name_label.setVisible(False)
        self.sfp_name_input.setVisible(False)

        self.mc_name_input = QLineEdit(self)
        self.mc_name_input.setGeometry(550, 140, 130, 30)
        self.mc_name_label = self.create_label("MC_NAME", 450, 140, 100, 30)
        self.mc_name_label.setVisible(False)
        self.mc_name_input.setVisible(False)

        self.sfp_serial_input = QLineEdit(self)
        self.sfp_serial_input.setGeometry(550, 100, 130, 30)
        self.sfp_serial_label = self.create_label("SFP_SERIAL", 450, 100, 100, 30)
        self.sfp_serial_label.setVisible(False)
        self.sfp_serial_input.setVisible(False)

        self.mc_serial_input = QLineEdit(self)
        self.mc_serial_input.setGeometry(550, 180, 130, 30)
        self.mc_serial_label = self.create_label("MC_SERIAL", 450, 180, 100, 30)
        self.mc_serial_label.setVisible(False)
        self.mc_serial_input.setVisible(False)

        self.generate_url_btn_olt = QPushButton("Сгенерировать OLT URL", self)
        self.generate_url_btn_olt.setGeometry(260, 190, 150, 30) 
        self.generate_url_btn_olt.clicked.connect(self.generate_all_olt_urls)
        self.generate_url_btn_olt.setVisible(False)

        self.generate_url_btn_ftth = QPushButton("Сгенерировать FTTH URL", self)
        self.generate_url_btn_ftth.setGeometry(260, 190, 150, 30) 
        self.generate_url_btn_ftth.clicked.connect(self.generate_all_ftth_urls)
        self.generate_url_btn_ftth.setVisible(False)

        self.create_pool_btn = QPushButton("Создать POOL", self)
        self.create_pool_btn.setGeometry(90, 230, 150, 30)
        self.create_pool_btn.clicked.connect(self.open_pool_url)
        self.create_pool_btn.setVisible(False)

        self.open_url2_btn = QPushButton("Создать NAS", self)
        self.open_url2_btn.setGeometry(260, 230, 150, 30)
        self.open_url2_btn.clicked.connect(self.open_nas_url)
        self.open_url2_btn.setVisible(False)

        self.open_url3_btn = QPushButton("Создать olt Юзера", self)
        self.open_url3_btn.setGeometry(430, 230, 150, 30)
        self.open_url3_btn.clicked.connect(self.open_user_olt_url)
        self.open_url3_btn.setVisible(False)
    
        self.open_url4_btn = QPushButton("Создать ftth Юзера", self)
        self.open_url4_btn.setGeometry(430, 230, 150, 30)
        self.open_url4_btn.clicked.connect(self.open_ftth_url)
        self.open_url4_btn.setVisible(False)
        
        self.vlan_label = QLabel("Выбранный VLAN:", self)
        self.vlan_label.setGeometry(20, 270, 120, 30)
        
        self.vlan_display = QLineEdit(self)
        self.vlan_display.setGeometry(130, 270, 100, 30)
        self.vlan_display.setReadOnly(True)  

    def generate_gateway_ip(self):
        try:
            ip_parts = self.ip_subnet_input.text().split('.')
            ip_parts[-1] = str(int(ip_parts[-1]) + 1)
            return '.'.join(ip_parts)
        except ValueError:
            logging.info("Неверный формат IP-адреса.")
            return None

    def generate_first_ip(self):
        try:
            ip_parts = self.ip_subnet_input.text().split('.')
            ip_parts[-1] = str(int(ip_parts[-1]) + 2)
            return '.'.join(ip_parts)
        except ValueError:
            logging.info("Неверный формат IP-адреса.")
            return None

    def generate_pool_url(self):
        gateway_ip = self.generate_gateway_ip()
        fisrt_ip = self.generate_first_ip()
        if gateway_ip:
            self.url = f"https://stat.acn.group/admin/index.cgi?add_form=1&index=63&BIT_MASK={self.bit_mask_input.text()}&COUNTS={self.counts_input.text()}&DNS={self.dns_input.text()}&NAME={self.name_pool_input.text()}&IP={fisrt_ip}&GATEWAY={gateway_ip}"
            logging.info("Сгенерированный POOL URL: " + self.url)
            self.create_pool_btn.setVisible(True)

    def generate_nas_url(self):
        gateway_ip = self.generate_gateway_ip()
        if gateway_ip:
            self.url2 = f"https://stat.acn.group/admin/index.cgi?add_form=1&index=62&NAS_ALIVE={self.nas_alive_input.text()}&fix=true&NAS_NAME={self.nas_name_input.text()}&NAS_IP={gateway_ip}&MAC={self.mac_input.text()}"
            logging.info("Сгенерированный NAS URL: " + self.url2)
            self.open_url2_btn.setVisible(True)

    def generate_user_olt_url(self):
        self.url3 = f"https://stat.acn.group/admin/index.cgi?index=24&GID=10&_ONU_NAME={self.onu_name_input.text()}&LOGIN={self.abon_name_input.text()}&FIO=&_ONU_MAC={self.mac_onu_input.text()}&_ONU_SERIAL={self.onu_serial_input.text()}"
        logging.info("Сгенерированный USER OLT URL: " + self.url3)
        self.open_url3_btn.setVisible(True)

    def generate_user_ftth_url(self):
        self.ftth_url = f"https://stat.acn.group/admin/index.cgi?index=24&GID=10&_MC_NAME={self.mc_name_input.text()}&_SFP_NAME={self.sfp_name_input.text()}&LOGIN={self.abon_name_input.text()}&_SFP_SERIAL={self.sfp_serial_input.text()}&_MC_SERIAL={self.mc_serial_input.text()}"
        logging.info("Сгенерированный USER FTTH URL: " + self.ftth_url)
        self.open_url4_btn.setVisible(True)

    def showEvent(self, event):
        super().showEvent(event)
        if event.isAccepted():
            self.onTabActivated()

    def onTabActivated(self):
        path = set_temp_path()
        files = os.listdir(path)
        logging.info("Вкладка 2 активирована")
        for file_name in files:
            if file_name.endswith('.yaml'):
                if re.match(r'Bel-.*_node_tmp\.yaml', file_name):
                    self.FTTH_SW0()
                elif file_name == 'merge_yaml_node_switch.yaml':
                    self.FTTH_SWX()
                elif file_name == 'merge_yaml_node_olt.yaml':
                    self.OLT()

    def generate_all_olt_urls(self):
        self.generate_pool_url()
        self.generate_nas_url()
        self.generate_user_olt_url()

    def generate_all_ftth_urls(self):
        self.generate_pool_url()
        self.generate_nas_url()
        self.generate_user_ftth_url()

    def FTTH_SW0(self):
        self.generate_url_btn_ftth.setVisible(True)     
        self.sfp_name_input.setVisible(True)
        self.sfp_name_label.setVisible(True)
        self.mc_name_input.setVisible(True)
        self.mc_name_label.setVisible(True)
        self.sfp_serial_input.setVisible(True)
        self.sfp_serial_label.setVisible(True)
        self.mc_serial_input.setVisible(True)
        self.mc_serial_label.setVisible(True)
        self.onu_name_input.setVisible(False)
        self.onu_name_label.setVisible(False)
        self.mac_onu_input.setVisible(False)
        self.mac_onu_label.setVisible(False)
        self.onu_serial_input.setVisible(False)
        self.onu_serial_label.setVisible(False)
        self.bit_mask_input.setText('6')
        self.counts_input.setText('28')
        self.update_gui_from_yaml_ftth_sw0()

    def FTTH_SWX(self):
        self.bit_mask_input.setText('6')
        self.counts_input.setText('28')

    def OLT(self):
        self.generate_url_btn_olt.setVisible(True)
        self.sfp_name_input.setVisible(False)
        self.sfp_name_label.setVisible(False)
        self.mc_name_input.setVisible(False)
        self.mc_name_label.setVisible(False)
        self.sfp_serial_input.setVisible(False)
        self.sfp_serial_label.setVisible(False)
        self.mc_serial_input.setVisible(False)
        self.mc_serial_label.setVisible(False)
        self.onu_name_input.setVisible(True)
        self.onu_name_label.setVisible(True)
        self.mac_onu_input.setVisible(True)
        self.mac_onu_label.setVisible(True)
        self.onu_serial_input.setVisible(True)
        self.onu_serial_label.setVisible(True)
        self.process_olt_data()

    def open_pool_url(self):
        if hasattr(self, 'url') and self.url:
            webbrowser.open(self.url)
        else:
            QMessageBox.warning(self, "Предупреждение", "POOL URL не сгенерирован")

    def open_nas_url(self):
        if hasattr(self, 'url2') and self.url2:
            webbrowser.open(self.url2)
        else:
            QMessageBox.warning(self, "Предупреждение", "NAS URL не сгенерирован")

    def open_user_olt_url(self):
        abon_name_value = self.abon_name_input.text()
        mac_onu_value = self.mac_onu_input.text()
        gw_value = self.generate_gateway_ip()
        selected_vlan_value = self.selected_vlan
        selected_pon_value = self.selected_ponf
        self.save_olt(abon_name_value, mac_onu_value, gw_value, selected_vlan_value, selected_pon_value)
        if hasattr(self, 'url3') and self.url3:
            webbrowser.open(self.url3)
        else:
            QMessageBox.warning(self, "Предупреждение", "OLT пользователя URL не сгенерирован")

    def open_ftth_url(self):  
        abon_name_value = self.abon_name_input.text()
        gw_value = self.generate_gateway_ip()
        selected_vlan_value = self.selected_vlan
        eth_interface_value = self.selected_eth
        self.save_ftth(abon_name_value, gw_value, selected_vlan_value, eth_interface_value)
        if hasattr(self, 'ftth_url') and self.ftth_url:
            webbrowser.open(self.ftth_url)
        else:
            QMessageBox.warning(self, "Предупреждение", "FTTH пользователя URL не сгенерирован")

    def update_gui_from_yaml_ftth_sw0(self):
        path_temp = set_temp_path()
        files = os.listdir(path_temp)
        for file_name in files:
            if re.match(r'Bel-.*_node_tmp\.yaml', file_name):
                with open(os.path.join(path_temp, file_name), 'r') as file:
                    data = yaml.safe_load(file)
                    selected_eth_port = data.get('Eth_Ports', [None])[0]
                    if selected_eth_port:
                        self.selected_eth = selected_eth_port
                        port_number = selected_eth_port.replace('Eth1/', '')
                        node_name_cut = file_name.replace('_node_tmp.yaml', '').replace('-IX', '').replace('Bel-', '').replace('_sw0', '')
                        self.name_pool_input.setText(f"Pool_{node_name_cut}_{port_number}")
                        self.nas_name_input.setText(f"NAS_{node_name_cut}_{port_number}")
                        self.abon_name_input.setText(f"Bel-{node_name_cut}_{port_number}")
                    selected_vlan = data.get('VLAN_Interfaces', [None])[0]
                    if selected_vlan:
                        self.selected_vlan = selected_vlan
                        self.vlan_display.setText(self.selected_vlan)
                        self.update_subnet_and_mac_from_yaml(node_name_cut, selected_eth_port)
                        return

    def update_subnet_and_mac_from_yaml(self, node_name_cut, selected_eth_port):
        sw0_directory = os.path.join(os.path.dirname(__file__), 'sw0')
        subnet_file = os.path.join(sw0_directory, f'Bel-{node_name_cut}-IX_sw0.yaml')
        if os.path.exists(subnet_file):
            with open(subnet_file, 'r') as file:
                data = yaml.safe_load(file)
                for entry in data:
                    if entry['port'] == selected_eth_port:
                        self.ip_subnet_input.setText(entry['subnet'])
                        break

        mac_file = os.path.join(sw0_directory, 'CISCO.yaml')
        if os.path.exists(mac_file):
            with open(mac_file, 'r') as file:
                data = yaml.safe_load(file)
                mac_address_key = f'Bel-{node_name_cut}-IX_sw0'
                mac_address = data.get(mac_address_key, [None])[0]
                if mac_address:
                    self.mac_input.setText(mac_address)

    def process_olt_data(self):
        temp_folder_path = set_temp_path()
        olt_yaml_file = os.path.join(temp_folder_path, 'merge_yaml_node_olt.yaml')
        if os.path.exists(olt_yaml_file):
            with open(olt_yaml_file, 'r') as file:
                data = yaml.safe_load(file)

            self.handle_pon_and_vlan_interfaces(data)

    def handle_pon_and_vlan_interfaces(self, data):
        free_pon_key = next((key for key in data if key.endswith('_pon_Free_pon')), None)
        if free_pon_key:
            free_pons = data[free_pon_key]
            if free_pons:
                selected_pon = free_pons[0]
                self.selected_ponf = selected_pon.replace('Pon_', '').replace('_', ' ')
                olt_name = free_pon_key.split('_pon_Free_pon')[0]
                self.find_subnet_for_pon(olt_name, selected_pon)
                olt_cut = olt_name.replace('Bel-', '').replace('-IX', '')
                pon_interface = selected_pon.replace('Pon_', '')
                self.name_pool_input.setText(f"Pool_{olt_cut}_{pon_interface}")
                self.nas_name_input.setText(f"NAS_{olt_cut}_{pon_interface}")
                self.abon_name_input.setText(f"{olt_cut}_{pon_interface}")

        vlan_key = next((key for key in data if key.endswith('_node_tmp_VLAN_Interfaces')), None)
        if vlan_key:
            node_name = vlan_key.replace('_node_tmp_VLAN_Interfaces', '')
            self.selected_vlan = data[vlan_key][0]
            self.find_mac_for_node(node_name)
            self.vlan_display.setText(self.selected_vlan)

    def find_mac_for_node(self, node_name):
        cisco_yaml_file = os.path.join(os.path.dirname(__file__), 'sw0', 'CISCO.yaml')
        if os.path.exists(cisco_yaml_file):
            with open(cisco_yaml_file, 'r') as file:
                data = yaml.safe_load(file)
            mac_address = data.get(node_name, [None])[0]
            if mac_address:
                self.mac_input.setText(mac_address)

    def find_subnet_for_pon(self, olt_name, selected_pon):
        olt_directory = os.path.join(os.path.dirname(__file__), 'Olt')
        olt_file = os.path.join(olt_directory, f'{olt_name}.yaml')
        if os.path.exists(olt_file):
            with open(olt_file, 'r') as file:
                data = yaml.safe_load(file)
            subnet = data.get(selected_pon)
            if subnet:
                subnet_without_mask = subnet.split('/')[0]
                self.ip_subnet_input.setText(subnet_without_mask)

    def save_olt(self, abon_name, mac_onu, gw, selected_vlan, selected_pon):
        data = {
            'abon_name': abon_name,
            'MAC_ONU': mac_onu,
            'GW': gw,
            'selected_vlan': selected_vlan,
            'selected_pon': selected_pon 
        }
        temp_path = set_temp_path() 
        yaml_file_path = os.path.join(temp_path, "sw0_OLT.yaml")
        with open(yaml_file_path, 'w') as file: 
            yaml.dump([data], file, default_flow_style=False)

        logging.info(f"Данные сохранены в {yaml_file_path}")

    def save_ftth(self, abon_name, gw, selected_vlan, eth_interface):
        data = {
            'abon_name': abon_name,
            'GW': gw,
            'selected_vlan': selected_vlan,
            'eth_interface': eth_interface
        }
        temp_path = set_temp_path() 
        yaml_file_path = os.path.join(temp_path, "sw0.yaml")
        with open(yaml_file_path, 'w') as file: 
            yaml.dump([data], file, default_flow_style=False)

        logging.info(f"Данные сохранены в {yaml_file_path}")
    
class Tab3(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setup_ui()
        self.transliterated_address = ""

    def setup_ui(self):
        self.label_address_ftth = QLabel("Введите полный адрес:", self)
        self.label_address_ftth.setGeometry(55, 45, 180, 20)
        self.label_address_ftth.setVisible(False)  

        self.entry_address_ftth = QLineEdit(self)
        self.entry_address_ftth.setGeometry(200, 40, 300, 30)
        self.entry_address_ftth.setVisible(False)  

        self.process_button_ftth = QPushButton("Обработать", self)
        self.process_button_ftth.setGeometry(200, 80, 100, 30)
        self.process_button_ftth.clicked.connect(self.process_address)
        self.process_button_ftth.setVisible(False) 

        self.additional_button_ftth = QPushButton("Записать!", self)
        self.additional_button_ftth.setGeometry(310, 80, 100, 30)
        self.additional_button_ftth.clicked.connect(self.additional_action)
        self.additional_button_ftth.setVisible(False)  
        self.additional_button_ftth.setEnabled(False)

        self.label_address_olt = QLabel("Введите полный адрес:", self)
        self.label_address_olt.setGeometry(55, 45, 180, 20)
        self.label_address_olt.setVisible(False)  

        self.entry_address_olt = QLineEdit(self)
        self.entry_address_olt.setGeometry(200, 40, 300, 30)
        self.entry_address_olt.setVisible(False)  

        self.process_button_olt = QPushButton("Обработать", self)
        self.process_button_olt.setGeometry(200, 80, 100, 30)
        self.process_button_olt.clicked.connect(self.process_address_olt)
        self.process_button_olt.setVisible(False) 

        self.additional_button_olt = QPushButton("Записать OLT!", self)
        self.additional_button_olt.setGeometry(310, 80, 100, 30)
        self.additional_button_olt.clicked.connect(self.additional_action_olt)
        self.additional_button_olt.setVisible(False)  
        self.additional_button_olt.setEnabled(False)

    def showEvent(self, event):
        super().showEvent(event)
        if event.isAccepted():
            self.onTabActivated()

    def onTabActivated(self):
        path_temp = set_temp_path()
        if os.path.exists(os.path.join(path_temp, 'sw0.yaml')):
            self.ftth()
        elif os.path.exists(os.path.join(path_temp, 'sw0_OLT.yaml')):
            self.olt()

    def ftth(self):
        self.label_address_ftth.setVisible(True)  
        self.entry_address_ftth.setVisible(True)  
        self.process_button_ftth.setVisible(True) 
        self.additional_button_ftth.setVisible(True)  
        pass

    def olt(self):
        self.label_address_olt.setVisible(True)  
        self.entry_address_olt.setVisible(True)  
        self.process_button_olt.setVisible(True) 
        self.additional_button_olt.setVisible(True)  
        pass

    @pyqtSlot()
    def process_address(self):
        full_address = self.entry_address_ftth.text()
        self.transliterated_address = self.transliterate(full_address)
        logging.info(f"Обработанный адрес: {self.transliterated_address}")
        self.additional_button_ftth.setEnabled(True)

    def read_sw0(self):
        yaml_file_path = os.path.join(set_temp_path(), 'sw0.yaml')

        if os.path.exists(yaml_file_path):
            with open(yaml_file_path, 'r') as file:
                logging.info(f"Чтение файла {yaml_file_path}")
                data = yaml.safe_load(file)
                if data:
                    return data[0]  
        else:
            logging.error("Файл 'sw0.yaml' не найден")
            return None

    def render_commands(self, data):
        rendered_commands = []
        vlan_number = data['selected_vlan'].split('Vlan')[1] 
        for cmd in self.command_templates_sw0:
            rendered_cmd = cmd.format(
                vlan=vlan_number,
                abon=self.transliterated_address,  
                gateway_with_mask=data['GW'],
                sw_port=data['eth_interface']
            )
            rendered_commands.append(rendered_cmd)
            logging.info(f"Сгенерированная команда: {rendered_cmd}")
        return rendered_commands

    def execute_commands_ftth(self, ip_address, username, password, commands):
        try:
            logging.info(f"Попытка подключения по SSH к {ip_address} с логином {username}")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=username, password=password)
            logging.info(f"Успешно подключено к {ip_address}")

            shell = ssh.invoke_shell()
            for cmd in commands:
                logging.info(f"Отправка команды: {cmd.strip()}")
                shell.send(cmd + "\n")
                time.sleep(1)  
                while not shell.recv_ready():  
                    time.sleep(3)
                output = shell.recv(10000).decode('utf-8')  
                logging.info(f"Ответ оборудования: {output}")

            ssh.close()
            logging.info("Команды выполнены успешно, соединение закрыто")
            return True
        except Exception as e:
            logging.error(f"Ошибка при выполнении команд: {e}")
            return False

    def additional_action(self):
        data = self.read_sw0()
        if data:
            username = self.config['UserLDAP']
            password = self.config['PassLDAP']
            logging.info("Данные успешно прочитаны из последнего YAML файла")

            rendered_commands = self.render_commands(data)
            abon_name = data.get('abon_name', '')

            ip_address = self.get_ip_address_from_map(abon_name)

            if ip_address:
                success = self.execute_commands_ftth(ip_address, username, password, rendered_commands)
                if success:
                    QMessageBox.information(self, "Успех", "Команды успешно выполнены на оборудовании.")
                else:
                    QMessageBox.critical(self, "Ошибка", "Произошла ошибка при выполнении команд на оборудовании.")
            else:
                logging.error(f"IP адрес для узла '{abon_name}' не найден в NAME_MAP")
                QMessageBox.critical(self, "Ошибка", f"IP адрес для узла '{abon_name}' не найден в NAME_MAP")

    def get_ip_address_from_map(self, abon_name):
        parts = abon_name.split('_')
        if len(parts) > 1:
            node_name = parts[0] + '-IX_sw0'
            ip_address = NAME_MAP.get(node_name)
            if ip_address:
                return ip_address
            else:
                logging.error(f"IP адрес для узла '{node_name}' не найден в NAME_MAP")
                return None
        else:
            logging.error(f"Имя абонента '{abon_name}' не содержит ожидаемых сегментов")
            return None

    def transliterate(self, text):
        mapping = {
            "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
            "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
            "й": "i", "к": "k", "л": "l", "м": "m", "н": "n",
            "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
            "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch",
            "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
            "э": "e", "ю": "yu", "я": "ya",
            "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D",
            "Е": "E", "Ё": "E", "Ж": "Zh", "З": "Z", "И": "I",
            "Й": "I", "К": "K", "Л": "L", "М": "M", "Н": "N",
            "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T",
            "У": "U", "Ф": "F", "Х": "H", "Ц": "Ts", "Ч": "Ch",
            "Ш": "Sh", "Щ": "Shch", "Ъ": "", "Ы": "Y", "Ь": "",
            "Э": "E", "Ю": "Yu", "Я": "Ya"
        }
        transliterated = ''.join(mapping.get(char, char) for char in text)
        return transliterated

    def read_sw0_OLT_yaml(self):
        yaml_file_path = os.path.join(set_temp_path(), 'sw0_OLT.yaml')
        if os.path.exists(yaml_file_path):
            with open(yaml_file_path, 'r') as file:
                logging.info(f"Чтение файла {yaml_file_path}")
                data = yaml.safe_load(file)
                if data:
                    return data[0]
        else:
            logging.error("Файл 'sw0_OLT.yaml' не найден")
            return None

    def generate_commands_for_OLT_and_sw0(self, data):
        vlan_number = data['selected_vlan'].split('Vlan')[1]
        pon_major = data['selected_pon'].split()[0]
        olt_number = data['abon_name'].split('_')[2]
        if len(olt_number) == 1:
            olt_downlink = f"Po10{olt_number}"
        else:
            olt_downlink = f"Po1{olt_number}"

        commands_olt = [
            "enable",
            "config",
            f"vlan {vlan_number}",
            "interface epon 0/0",
            f"vlan trunk {pon_major} {vlan_number}",
            f"ont add {data['selected_pon']} mac-auth {data['MAC_ONU']}",
            f"ont description {data['selected_pon']} \"{self.transliterated_address}\"",
            f"ont port vlan {data['selected_pon']} eth 1 translation {vlan_number} user-vlan {vlan_number}",
            f"ont port native-vlan {data['selected_pon']} eth 1 vlan {vlan_number} priority 0",
            "exit",
            f"interface link-aggregation",
            f"vlan trunk 1 {vlan_number}",
            "exit",
            "save"
        ]

        commands_sw0 = [
            "configure terminal",
            f"vlan {vlan_number}",
            f"name {self.transliterated_address}",
            "no shutdown",
            "exit",
            f"interface vlan {vlan_number}",
            f"ip address {data['GW']}/29",
            "ip dhcp relay address 45.67.195.5",
            "no shutdown",
            "exit",
            f"interface {olt_downlink}",
            "switchport",
            f"switchport trunk allowed vlan add {vlan_number}",
            "exit",
            "exit",
            "copy running-config startup-config",
            "exit"
        ]
        for cmd in commands_olt:
            logging.info(f"Сгенерированная команда для OLT: {cmd}")
        for cmd in commands_sw0:
            logging.info(f"Сгенерированная команда для sw0: {cmd}")
        return commands_olt, commands_sw0

    def execute_commands_OLT_and_sw0(self, ip_address_OLT, ip_address_sw0, commands_OLT, commands_sw0):
        username_OLT = self.config['UserOLT']
        password_OLT = self.config['PassOLT']
        try:
            ssh_OLT = paramiko.SSHClient()
            ssh_OLT.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_OLT.connect(ip_address_OLT, username=username_OLT, password=password_OLT)
            shell_OLT = ssh_OLT.invoke_shell()
            self.wait_for_prompt(shell_OLT) 
            for cmd in commands_OLT:
                shell_OLT.send(cmd + "\n")
                self.wait_for_prompt(shell_OLT)  
                output = shell_OLT.recv(10000).decode('utf-8', errors='ignore')  
                logging.info(f"Ответ OLT на команду '{cmd}': {output}")
            ssh_OLT.close()
            logging.info("Команды успешно выполнены на OLT")
        except Exception as e:
            logging.error(f"Ошибка при выполнении команд на OLT: {e}")
            return False
        username_sw0 = self.config['UserLDAP']
        password_sw0 = self.config['PassLDAP']
        try:
            ssh_sw0 = paramiko.SSHClient()
            ssh_sw0.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_sw0.connect(ip_address_sw0, username=username_sw0, password=password_sw0)
            shell_sw0 = ssh_sw0.invoke_shell()
            ssh_sw0.close()
            logging.info("Команды успешно выполнены на sw0")
        except Exception as e:
            logging.error(f"Ошибка при выполнении команд на sw0: {e}")
            return False

        return True

    def get_sw0_ip_from_abon_name(self, abon_name):
        node_name = abon_name.split('_')[0]  
        sw0_key = f"Bel-{node_name}-IX_sw0"

        ip_address_sw0 = NAME_MAP.get(sw0_key)
        logging.info(f"Поиск IP для sw0: abon_name = {abon_name}, sw0_key = {sw0_key}, найденный IP = {ip_address_sw0}")

        return ip_address_sw0

    @pyqtSlot()
    def process_address_olt(self):
        full_address = self.entry_address_olt.text()
        self.transliterated_address = self.transliterate(full_address)
        logging.info(f"Обработанный адрес для OLT: {self.transliterated_address}")
        self.additional_button_olt.setEnabled(True)

    def read_sw0_olt(self):
        yaml_file_path = os.path.join(set_temp_path(), 'sw0_OLT.yaml')

        if os.path.exists(yaml_file_path):
            with open(yaml_file_path, 'r') as file:
                logging.info(f"Чтение файла {yaml_file_path}")
                data = yaml.safe_load(file)
                if data:
                    return data[0] 
        else:
            logging.error("Файл 'sw0_OLT.yaml' не найден")
            return None

    def additional_action_olt(self):
        data = self.read_sw0_olt()
        if data:
            data['transliterated_address'] = self.transliterated_address
            username = self.config['UserOLT']
            password = self.config['PassOLT']
            logging.info("Данные успешно прочитаны из файла 'sw0_OLT.yaml'")

            commands_olt, commands_sw0 = self.generate_commands_for_OLT_and_sw0(data)
            ip_address_sw0 = self.get_sw0_ip_from_abon_name(data['abon_name'])
            ip_address_olt = self.calculate_ip_address_olt(data['abon_name'])

            if ip_address_sw0 and ip_address_olt:
                success_sw0 = self.execute_commands(ip_address_sw0, self.config['UserLDAP'], self.config['PassLDAP'], commands_sw0)
                success_olt = self.execute_commands_on_olt(ip_address_olt, username, password, commands_olt)
                if success_sw0 and success_olt:
                    QMessageBox.information(self, "Успех", "Команды успешно выполнены на оборудовании.")
                else:
                    QMessageBox.critical(self, "Ошибка", "Произошла ошибка при выполнении команд на оборудовании.")
            else:
                QMessageBox.critical(self, "Ошибка", "Не найден IP адрес для одного из устройств.")

    def calculate_ip_address_olt(self, abon_name):
        olt_number = abon_name.split('_')[2]
        olt_key = f"Bel-{abon_name.split('_')[0]}-IX_olt_{olt_number}"
        ip_address_olt = NAME_MAP_olt.get(olt_key, None)
        logging.info(f"Поиск IP для OLT: Название абона = {abon_name}, Выбранная OLT = {olt_key}, найденный IP = {ip_address_olt}")
        return ip_address_olt

    def execute_commands(self, ip_address, username, password, commands):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=username, password=password)
            shell = ssh.invoke_shell()
            for cmd in commands:
                shell.send(cmd + "\n")
                time.sleep(1)
                while not shell.recv_ready():
                    time.sleep(3)
                output = shell.recv(10000).decode('utf-8')
                logging.info(output)
            ssh.close()
            logging.info("Команды выполнены успешно")
            return True
        except Exception as e:
            logging.error(f"Ошибка при выполнении команд: {e}")
            return False

    def execute_commands_on_olt(self, ip_address, username, password, commands):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=username, password=password, look_for_keys=False, allow_agent=False)
            shell = ssh.invoke_shell()
            time.sleep(1)
            response = shell.recv(9999).decode('utf-8')
            logging.info(f"Ответ после ввода учетных данных: {response}")
            if "invalid" in response.lower():
                logging.error("Неверное имя пользователя или пароль!")
                ssh.close()
                return False
            for cmd in commands:
                shell.send(cmd + '\n')
                time.sleep(1)
                response = shell.recv(9999).decode('utf-8')
                logging.info(f"Ответ OLT на команду '{cmd}': {response}")
            ssh.close()
            logging.info("Команды успешно выполнены на OLT")
            return True
        except Exception as e:
            logging.error(f"Ошибка при выполнении команд на OLT: {e}")
            return False

    def wait_for_prompt(shell, prompts=("#", ">")):
        buffer = ""
        while not buffer.strip().endswith(prompts):
            if shell.recv_ready():
                buffer += shell.recv(1024).decode('utf-8', errors='ignore')
            else:
                time.sleep(0.1)
        return buffer

    command_templates_sw0 = [
        "configure terminal",
        "vlan {vlan}",
        "name {abon}",
        "no shutdown",
        "exit",
        "interface vlan {vlan}",
        "ip address {gateway_with_mask}/27",
        "ip dhcp relay address 45.67.195.5",
        "no shutdown",
        "exit",
        "interface {sw_port}",
        "description {abon}",
        "no shutdown",
        "no cdp enable",
        "switchport",
        "switchport mode access",
        "switchport access vlan {vlan}",
        "exit",
        "exit",
        "copy running-config startup-config",
        "exit"
    ]

class TabbedWindow(QMainWindow):
	def __init__(self, config):
		super().__init__()
		self.config = config
		logging.info("Скрипт был запущен")
		self.setWindowTitle("Приложение для полуавтоматического заведения абонентов")
		self.resize(700, 350)
		self.tab_widget = QTabWidget()
		self.setCentralWidget(self.tab_widget)
		tab1 = Tab1(config)
		tab2 = Tab2(config)
		tab3 = Tab3(config)
		self.tab_widget.addTab(tab1, "Подключение")
		self.tab_widget.addTab(tab2, "Генерация ссылок")
		self.tab_widget.addTab(tab3, "Запись итогового результата")

	def closeEvent(self, event):
		logging.info("Работа скрипта завершена")
		super().closeEvent(event)

if __name__ == "__main__":
    config_file = "ACN_settings.ini"
    config = initialize_config(config_file)
    if validate_config(config):
        app = QApplication(sys.argv)
        window = TabbedWindow(config['DEFAULT'])
        window.show()
        sys.exit(app.exec())
