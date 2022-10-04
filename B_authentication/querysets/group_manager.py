from django.db.models import Value, Count, When,F,Manager,Func,Subquery,CharField,TextField,Exists,OuterRef
from django.db.models.functions import Concat,Substr,Cast
from django.db.models.query import QuerySet
from B_authentication.models import *


class FillialQueryset(QuerySet):
    def get_info(self):
        datas = None
        if  not self.exists():
            datas = self.all()
        else:    
            datas = self.values(
                'education_name',
                'id',
                'payment_date',
                'id_education'
            )
            for item in datas:
                item['days'] = 'as'   
        return datas
    def all_fillils(self):
        if  not self.exists():
            return self.all()
        return self.get_info().values(
                'education_name',
                'id',
                'payment_date',
                'id_education'
            )
    def get_fillials(self):
        return self.get_info().values(
                'education_name',
                'id',
                'payment_date',
                'id_education'
        ).filter(id=id)
        
class FillialManager(Manager):
    def get_query_set(self):
        return FillialQueryset(self.model)
    def all_fillils(self):
        return self.get_query_set().all_fillils()

    def get_fillials(self):
        return self.get_query_set().get_fillials(id)