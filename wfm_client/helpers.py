from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse , HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from django.core import serializers
from django.db.models import Q
from django.contrib import messages
from django.template.context import RequestContext
from django.db.models import Count
from django import template
from itertools import chain

import re
import hashlib
import random, datetime
import urllib
import time
import json
# import stripe
import string

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from wfm_general.models import *
from wfm_client.models import *
from wfm_client.forms import itemForm, requestOrderForm, requestItemForm
from WFM_INV.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY


def getRandom(stringLength):
    return "".join([random.choice(string.ascii_letters + string.digits + string.punctuation[3:7])for n in range(stringLength)])



    


# function start here
