import sqlite3
import time
import datetime
import os
# import sys
# sys.path.append()

import requests


class ApiFM3:
    def __init__(self, log, passw, adress, con_type, oid, sens_name, date1, date2):
        '''
        Переменные получаемые из конфигурации
        '''
        self.login = log
        self.password = passw
        self.fort_address = adress
        self.con_type = con_type
        self.oid = oid
        '''Имена датчиков в системе'''
        self.sensor_name = sens_name  # [r'ТРК',r'ТРК1']
        # self.sensor_list = '17632;17633;'
        self.date1 = date1  # '2017-08-14 21:00:00'
        self.date2 = date2  # '2017-08-15 20:59:59'

    def login_serv(self):
        """Function open connection to server FM3
        Input arg: con_type - connection type(http or https)
                   serv - server address
                   log - login
                   passw - password
        Return: Typle: (Server response,Cookies)"""
        s = requests.Session()
        url = '{0}://{1}/api/Api.svc/connect?login={2}&password={3}&lang=en-en&timezone=2'.format(self.con_type,
                                                                                                  self.fort_address,
                                                                                                  self.login,
                                                                                                  self.password)
        self.resp = s.get(url)
        self.cook = s.cookies
        return self.resp

    def object_inf_func(self):
        """Function ask objectinfo from FM3
        Input arg: con_type - connection type(http or https)
                   serv - server address
                   cook - cookies
                   oid - object id
        Return: Dict: """

        url = '{0}://{1}/api/Api.svc/objectinfo?oid={2}'.format(self.con_type, self.fort_address, self.oid)
        s = requests.Session()
        resp = s.get(url, cookies=self.cook)
        return resp.json()

    def parser(self, lst):
        for l in lst:
            if l['sid'] == self.sid_d['ТРК']:
                sens1 = l['vals']
            elif l['sid'] == self.sid_d['RFID метка']:
                sens2 = l['vals']
        for i in range(0, len(sens1)):
            sens2[i].update({'val1': sens2[i]['val']})
            sens2[i].pop('val')
            sens1[i].update(sens2[i])
        sens2 = []
        lst = []
        f = 0
        start_d = ''
        stop_d = ''
        lst1 = []
        lst2 = []
        fuel1 = 0
        for i in sens1:
            if not start_d and i['val'] > f:
                start_d = i['tm']
                f = i['val']
                rfid = i['val1']
            elif start_d:
                fuel = i['val']
                if fuel > f:
                    f = fuel
                elif fuel == f:
                    stop_d = i['tm']
                    if rfid == i['val1'] and rfid == 0:
                        with open('log.txt','a') as file:
                            file.writelines('ERROR no rfid {0}-{1}'.format(start_d, stop_d))
                    if fuel1 == 0:
                        resp = {'start_d': datetime.datetime.strptime(start_d, "%Y-%m-%d %H:%M:%S"),
                                'stop_d': datetime.datetime.strptime(stop_d, "%Y-%m-%d %H:%M:%S"), 'fuel': fuel,
                                'rfid': rfid}
                    else:
                        resp = {'start_d': datetime.datetime.strptime(start_d, "%Y-%m-%d %H:%M:%S"),
                                'stop_d': datetime.datetime.strptime(stop_d, "%Y-%m-%d %H:%M:%S"), 'fuel': fuel - fuel1,
                                'rfid': rfid}
                    fuel1 = fuel
                    lst.append(resp)
                    resp = ()
                    start_d = ''
        return lst

    def params_val(self):
        """Function return values of sid from period
        Input arg: con_type - connection type(http or https)
                   serv - server address
                   cook - cookies
                   oid - object id
                   sid_list = 'sid1;sid2;sid3;...sidN' - sensors id
                   start_d - start period, format '2017-08-15 20:59:59'
                   stop_d - end period,format '2017-08-15 20:59:59'
        Return: Dict: """
        sid = ''
        lsid = self.object_inf_func()

        self.sid_d = {}
        for l in self.sensor_name.split(';'):

            for li in lsid['sensors']:

                if li['name'] == l:
                    self.sid_d.update({l: li['sid']})
                    sid = sid + str(li['sid']) + ';'

        url = '{0}://{1}/api/Api.svc/paramsvals?oid={2}&sids={3}&from={4}&to={5}'.format(self.con_type,
                                                                                         self.fort_address, self.oid,
                                                                                         sid, self.date1, self.date2)
        s = requests.Session()
        resp = s.get(url, cookies=self.cook)
        res = self.parser(resp.json()['lparams'])
        return res, self.oid

    def close_session(self):
        s = requests.Session()
        url = '{0}://{1}/api/Api.svc/disconnect?login={2}&password={3}&lang=en-en'.format(self.con_type,
                                                                                          self.fort_address, self.login,
                                                                                          self.password)
        self.resp = s.get(url, cookies=self.cook)
        return self.resp.text


class DbWorker:
    def __init__(self, db_name, trk_id, customer_id):
        self.db_name = db_name
        self.trk_id = trk_id
        self.customer_id = customer_id

    def db_reader(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM Customer_config")
        for row in c.fetchall():
            if row[1] == self.customer_id:
                self.cust_config = row
        c.execute("SELECT * FROM trk_config")
        for row in c.fetchall():
            if row[-2] == self.trk_id:
                self.trk_config = row
        c.close()
        conn.close()

    def db_writer(self, result):
        sum_out = 0
        conn = sqlite3.connect(self.db_name)
        oid = result[1]
        for l in result[0]:
            c = conn.cursor()
            sum_out += l['fuel']
            c.execute(
                "INSERT INTO out_fuel (fuel_id, fuel_out_start, fuel_out_end, fuel_out_quantity, fuel_out_rfid, fuel_in_quantity, fuel_out_name,fuel_out_wh, fuel_trk_id,fuel_customer_id) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (oid, l['start_d'], l['stop_d'], l['fuel'], l['rfid'], 0, '', '', 1, 1))
        conn.commit()
        delta = 3
        dt_obj = result[0][0]['stop_d']
        dita = dt_obj.replace(hour=23 - delta, minute=59, second=59)
        sum_out = round(sum_out, 0)
        c.execute(
            "INSERT INTO report_days (fuel_data, fuel_number, fuel_trk_name, fuel_summary_out, fuel_summary_in, fuel_customer_id) VALUES (?,?,?,?,?,?)",
            (dita, self.trk_id, self.trk_config[4], sum_out, 1, 1))
        conn.commit()
        c.close()
        conn.close()


if __name__ == '__main__':
    l = time.localtime()
    db = os.curdir
    read_test = DbWorker(r'..\\..\\test_db.sqlite3', 1, 1)
    read_test.db_reader()
    d = l.tm_mday - 2
    date1 = '{0}-{1}-{2} 21:00:00'.format(l.tm_year, l.tm_mon, d)
    date2 = '{0}-{1}-{2} 20:59:59'.format(l.tm_year, l.tm_mon, l.tm_mday - 1)
    lsi = ApiFM3(read_test.cust_config[5], read_test.cust_config[6], read_test.cust_config[4],
                 read_test.cust_config[3], read_test.trk_config[1], read_test.trk_config[2], date1, date2)
    if 'Ok' in lsi.login_serv().text:
        a = lsi.params_val()
        read_test.db_writer(a)
        lsi.close_session()
