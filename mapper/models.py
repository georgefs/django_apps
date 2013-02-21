# -*- coding: utf-8 -*
import abc

from django.db import models
from settings import API
import urllib, urllib2

# Create your models here.

STATUS_LIST = (
                ('init', 'init'),
                ('changed', 'changed'),
                ('success', 'success'),
            )

class MapperModel(models.Model):
    '''
    簡易的mapping model format

    定義簡單的 api 與 django db的簡單存取介面
    '''
    
    __status = models.CharField( max_length = 100,
                                choices = STATUS_LIST,
                                default = "unsend")
    @property
    def __api(self):
        raise NotImplementedError("uncreate this function")



    def save(self, *args, **kwargv):
        '''
        定義 model 寫入時動作
        status = unsend & changed 則 不動作
        status = sended 則 修改狀態為 changed
        '''
        if self.__status == "success":
            self.__status = "changed"

        super(Model, self).save()
        pass
#-----------------------------------------------

    def format(self):
        '''
        model 轉 api data 格式
        '''
        raise NotImplementedError("uncreate this function")

    def unformat(self):
        '''
        api 資料 轉model 格式
        '''
        raise NotImplementedError("uncreate this function")

    def sync(self):
        '''
        資料同步處理, 可選..
        '''
        raise NotImplementedError("uncreate this function")
#------------------------------------------------

    def send(api, data):

        data = urllib.urlencode(data)
        req = urllib2.Request(
                    url = api,
                    data = data,
                )
        return urllib2.urlopen(req)


    def update(self):
        '''
        更新當前model 對應到的資料
        '''
        update_api = self.__api.get('UPDATE')

        data = self.format()
        
        result = self.send(update_api, data)

        self.__status = "success"

        self.save()

        

    def insert(self):
        '''
        將當前model 資料 新增到 api server
        '''

        insert_api = self.__api.get('INSERT')

        data = self.format()
        
        result = self.send(insert_api, data)

        self.__status = "success"

        return result

    
    def remove(self):
        '''
        刪除當前model 對應到的資料
        '''
        remove_api = self.__api.get('REMOVE')

        data = self.format()
        
        result = self.send(remove_api, data)
        
        self.__status = "init"
            
        
        

    



        



