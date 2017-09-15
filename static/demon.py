from db_workers.db_sqlite3 import DbWorker, ApiFM3
import time
import os

while True:
    l = time.localtime()
    if l.tm_hour == 00 and 0 < l.tm_min < 2:
        db = os.curdir
        read_test = DbWorker(r'..\\test_db.sqlite3', 1, 1)
        read_test.db_reader()
        d = l.tm_mday - 3
        srt ='{0}-{1}-{2} 21:00:00'.format(l.tm_year, l.tm_mon, d)
        #time.strptime(srt, '%Y-%m-%d %H:%M:%s')
        #time.strftime(srt,'%Y-%m-%d %H:%M:%s')
        date1 = srt
        date2 = '{0}-{1}-{2} 20:59:59'.format(l.tm_year, l.tm_mon, l.tm_mday - 2)
        lsi = ApiFM3(read_test.cust_config[5], read_test.cust_config[6], read_test.cust_config[4], read_test.cust_config[3], read_test.trk_config[1], read_test.trk_config[2], date1, date2)
        #('petri_k', '123123', '4g.exzotron.ru', 'http', 1875, ['ТРК','RFID метка'], '2017-09-10 21:00:00', '2017-09-11 20:59:59')
        if 'Ok' in lsi.login_serv().text :
            a = lsi.params_val()
            read_test.db_writer(a)
            lsi.close_session()
    else:
        time.sleep(60)