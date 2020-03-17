#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import base64
import hashlib
import time

class Indx:
    
    def __init__(self, Login,Password,Culture,Wmid):
        self.AuthS = Login + ";" + Password + ";" + Culture
        self.Auth = AuthS + ";" + Wmid
   
    def make_params( self, Auth, ID = '', DateStart = '', 
        DateEnd = '', sOfferID = '', ifS = False, Tick_ID = '', Tick_Kind = '')
        if not ifS:
            if ID: Auth += ';'+ID
            if DateStart: Auth += ';' + DateStart
            if DateEnd: Auth += ';' + DateEnd
            if sOfferID: Auth += ';' + sOfferID
            if Tick_ID: Auth += ';' + Tick_ID
            if Tick_Kind: Auth += ';' + Tick_Kind
        sig = base64.b64encode(hashlib.sha256(Auth.encode('utf-8')).digest())
        return  params = {"ApiContext": {"Login": Login, "Wmid": Wmid, 
       "Culture": "ru-RU", "Signature": sig} }
    
    def api(self, api_name, api_params={}):
        time.sleep(2)
        header = {"Content-type": "application/json; charset=utf-8"}
        response=requests.post('api.indx.ru/api/v2/trade/'+api_name, data = api_params, headers = header )
        return response.text
    
    def Balance(self):
        return self.api('Balance', self.make_params(self.Auth))
    
    def Tools(self):
        return self.api('Tools', self.make_params(self.AuthS,'','','','',True)
    
    def HistoryTrading(self,ID,DateStart,DateEnd):
        params = self.make_params(self.Auth,ID,DateStart,DateEnd)
        params['Trading'] = {"ID":ID,"DateStart":DateStart,
"DateEnd":DateEnd}}
        return self.api('HistoryTrading', params)
    
    def HistoryTransaction(self,ID,DateStart,DateEnd):
        params = self.make_params(self.Auth,ID,DateStart,DateEnd)
        params['Trading'] = {"ID":ID,"DateStart":DateStart,"DateEnd":DateEnd}}
        return self.api('HistoryTransaction', params)
    
    def OfferMy(self):
        return self.api('OfferMy', self.make_params(self.Auth))
    
    def OfferList(self, ID):
        params = self.make_params(self.Auth,ID)
        params['Trading'] = {'ID': ID}
        return self.api('OfferList', params)
    
    def OfferAdd(self, ID, Count, IsBid, Price):
        params = self.make_params(self.Auth,ID)
        params['Offer'] = {"ID": ID, "Count": Count, "IsAnonymous": 'true', "IsBid": IsBid, "Price": Price}
        return self.api('OfferAdd', params)
    
    def OfferDelete(self, OfferID):
        params = self.make_params(self.Auth,'','','',str(OfferID))
        params['OfferId']=OfferID
        return self.api('OfferAdd', params)
    
    def Tick(self, Tick_ID, Tick_Kind):
        params = self.make_params(self.Auth,'','','','',False,Tick_ID,Tick_Kind)
        params['Tick'] = {"ID": Tick_ID, "Kind": Tick_Kind} }
        return self.api('tick', params)
