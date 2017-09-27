

class ParserFM3:

    def __init__(self, lst, num):
        self.lst = lst
        self.sens_num = num


    def update_to_one_out(self):
        for l in lst:
            if l['sid'] == self.sid_d['ТРК']:
                sens1 = l['vals']
            elif l['sid'] == self.sid_d['RFID метка']:
                sens2 = l['vals']




    def parser(self, result):
        lst = result['lparams']
        result = {}

        for l in lst:
            if l['sid'] == self.sid_d['ТРК']:
                sens1 = l['vals']
            elif l['sid'] == self.sid_d['RFID метка']:
                sens2 = l['vals']

        for i in range(0, len(sens1)):
            sens2[i].update({'val1': sens2[i]['val']})
            sens2[i].pop('val')
            #print(sens2[i])
            sens1[i].update(sens2[i])
        #print(sens1)
        sens2 = []
        lst = []
        f = 0
        start_d = ''
        stop_d = ''
        lst1 = []
        lst2 = []
        fuel1 = 0
        # print(i)
        # print(sens1)
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
                        resp = {'start_d': start_d, 'stop_d': stop_d, 'fuel': fuel, 'rfid': i['val1']}
                    else:
                        resp = {'start_d': start_d, 'stop_d': stop_d, 'fuel': fuel - fuel1, 'rfid': i['val1']}
                    fuel1 = fuel
                    lst.append(resp)
                    resp = ()
                    start_d = ''

        '''for i in sens2:
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

        for i in range(0, len(lst)):
            lst[i].update(lst1[i])
        '''
        return lst