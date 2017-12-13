from django import template
import json
from django.contrib.auth.models import Group
from wfm_client.models import item, requestOrder, requestItem
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


register = template.Library()

@register.filter(name = 'get_requestOrderItems')
def get_requestOrderItems(user):
    requested =  requestOrder.objects.filter(requestee=user,deleted=False).count()
    return requested
   

def jsondump(response_list):
	return json.dumps(list(response_list), cls=DjangoJSONEncoder) 


@register.simple_tag(name = 'fetch_signers')
def fetch_signers():
	all_items  = item.objects.values_list('item_name', flat = True)
	return jsondump(all_items)


@register.simple_tag
def get_order_type_count(status):
    return requestOrder.objects.filter(status=status,deleted=False).count()


@register.filter(name = 'trunc')
def trunc(word):
	new_word = str(word)
	if len(new_word) > 10:
		return new_word[0:10] + "..."
	else:
		return new_word
    
    
@register.filter(name = 'removeduplicates')
def removeduplicates(values):
    new_list = list(set(values))
    print "new_list:",new_list
    return new_list


    
