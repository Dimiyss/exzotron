import requests
import sqlite3


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
        self.sensor_name = sens_name#[r'ТРК',r'ТРК1']
        #self.sensor_list = '17632;17633;'
        self.date1 = date1 #'2017-08-14 21:00:00'
        self.date2 = date2 #'2017-08-15 20:59:59'



    def login_serv(self):
        """Function open connection to server FM3
        Input arg: con_type - connection type(http or https)
                   serv - server address
                   log - login
                   passw - password
        Return: Typle: (Server response,Cookies)"""
        s = requests.Session()
        url = '{0}://{1}/api/Api.svc/connect?login={2}&password={3}&lang=en-en&timezone=2'.format(self.con_type,self.fort_address, self.login, self.password)
        self.resp = s.get(url)
        self.cook = s.cookies
        return self.resp



    def object_inf_func (self):
        """Function ask objectinfo from FM3
        Input arg: con_type - connection type(http or https)
                   serv - server address
                   cook - cookies
                   oid - object id
        Return: Dict: """

        url = '{0}://{1}/api/Api.svc/objectinfo?oid={2}'.format(self.con_type, self.fort_address, self.oid)
        s = requests.Session()
        resp = s.get(url, cookies= self.cook)
        return resp.json()

    def parser(self, result):
        lst = result['lparams']
        result = {}

        for l in lst:
            if l['sid'] == self.sid_d['ТРК']:
                sens1 = l['vals']
            elif l['sid'] == self.sid_d['RFID метка']:
                sens2 = l['vals']

        lst = []
        f = 0
        start_d = ''
        stop_d = ''
        lst1 = []
        lst2 = []
        fuel1 = 0
        for i in sens1:
            # print(i)
            if not start_d and i['val'] > f:
                start_d = i['tm']
                f = i['val']
                # print(1)
                # print(i['val'], start_d)
            elif start_d:
                fuel = i['val']
                if fuel > f:
                    f = fuel
                elif fuel == f:
                    stop_d = i['tm']
                    if fuel1 == 0:
                        resp = {'start_d': start_d, 'stop_d': stop_d, 'fuel': fuel}
                    else:
                        resp = {'start_d': start_d, 'stop_d': stop_d, 'fuel': fuel - fuel1}
                    fuel1 = fuel
                    lst.append(resp)
                    resp = ()
                    start_d = ''


        for i in sens2:
            if not start_d and i['val'] != 0:
                start_d = i['tm']
                f = i['val']
                # print(1)
                # print(i['val'], start_d)
            elif start_d and i['val'] == 0:

                stop_d = i['tm']
                resp = {'start_d': start_d, 'stop_d': stop_d, 'rfid': f}
                lst1.append(resp)
                resp = ()
                start_d = ''

        for i in range(0, len(lst) ):
            lst[i].update(lst1[i])
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
        sid=''
        lsid = self.object_inf_func()

        self.sid_d = {}
        for l in self.sensor_name:

            for li in lsid['sensors']:

                if li['name'] == l:
                    self.sid_d.update({l: li['sid']})
                    sid = sid + str(li['sid']) + ';'

        url='{0}://{1}/api/Api.svc/paramsvals?oid={2}&sids={3}&from={4}&to={5}'.format(self.con_type, self.fort_address, self.oid, sid, self.date1, self.date2)
        s = requests.Session()
        resp = s.get(url, cookies=self.cook)
        res = self.parser(resp.json())
        return res, self.oid

    def close_session(self):
        s = requests.Session()
        url = '{0}://{1}/api/Api.svc/disconnect?login={2}&password={3}&lang=en-en'.format(self.con_type, self.fort_address, self.login, self.password)
        self.resp = s.get(url, cookies=self.cook)
        return self.resp.text







lsiss = ApiFM3('petri_k', '123123', '4g.exzotron.ru', 'http', 1875, ['ТРК','RFID метка'], '2017-09-10 21:00:00', '2017-09-11 20:59:59')

if 'Ok' in lsiss.login_serv().text :

    a =lsiss.params_val()
    print(a)
    print(lsiss.close_session())
    write = DbWorker(r'..\\..\\test_db.sqlite3')
    write.db_writer(a)


