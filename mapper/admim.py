from django.contrib import admin
from django.conf import setting 
from django.template.response import TemplateResponse

import abc

def MapperAdmin(admin.ModelAdmin):
    __metaclass__ = abc.ABCMeta
    
    __error_template = "mapping/error.html"
    __insert_template = "mapping/insert.html"
    __update_template = "mapping/update.html"
    __remove_template = "mapping/remove.html"
    change_form_template = "mapping/mapping_change_from.html"

    def __init__(self):
        self.readonly_fields += "__status"
        super(Admin, self).__init__()

    def get_urls(self):
        '''
            add page action for admin change api server
        '''
        urls = super(ActivityAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(\d+)/update/$', self.update_view),
            url(r'^(\d+)/insert/$', self.insert_view),
            url(r'^(\d+)/remove/$', self.remove_view),
        )
        return my_urls + urls 
    
    def base_view(view):

        def base(self, request, *args)
            try:
                return view(self, request, *args)
            except Exception, e:
                return TemplateResponse(request, self.__error_view, , e)

        return base

    @base_view
    def update_view(self, request, pk):
        data = self.get_date(pk)
        assert data.__status == "changed", 'not changed'
        result = self.model.update(pk)

        return TemplateResponse(request, self.__update_template, result)

    @base_view
    def insert_view(self, request, pk):
        assert data.__status == "init", "inserted"
        result = self.model.insert(pk)

        return TemplateResponse(request, self.__insert_template, result)

    @base_view
    def remove_view(self, request, pk):
        assert data.__status != "init", "can't remove"
        result = self.model.remove(pk)

        return TemplateResponse(request, self.__remove_template, result)
       

