from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import Group
from base.forms import LoginForm, UserCreateForm, GroupCreateForm
from userprofile.models import UserProfile

class BaseView(TemplateView):
  template_name = "base/base.html"
  context_object_name = "base"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(BaseView, self).get_context_data(**kwargs)
    if self.request.user.is_authenticated():
      context['user'] = self.request.user
      context['displayname'] = UserProfile.objects.get(user=self.request.user).displayname
      context['isLoggedin'] = True
    return context

    
class HomeView(BaseView):
  template_name = "base/index.html"
  context_object_name = "homepage"
  
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super(HomeView, self).get_context_data(**kwargs)
    context['homesection'] = True
    return context
        
def register(request):
  def errorHandle(error):
    form = UserCreateForm()
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    return render_to_response('base/register.html', context)
    
  if request.method == 'POST': # If the form has been submitted...
    form = UserCreateForm(request.POST) # A form bound to the POST data
    if form.is_valid():
      form.save()
      context = RequestContext(request)
      context['registered'] = True
      return render_to_response('base/register.html', context)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  else:
    form = UserCreateForm() # An unbound form
    context = RequestContext(request)
    context['form'] = form
    return render_to_response('base/register.html', context)
    
def newGroup(request):
  def errorHandle(error):
    form = GroupCreateForm()
    context = RequestContext(request)
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
    context['error'] = error
    context['form'] = form
    context['groupssection'] = True
    return render_to_response('base/newgroup.html', context)
  
  if request.method == 'POST': # If the form has been submitted...
    form = GroupCreateForm(request.POST) # A form bound to the POST data
    if form.is_valid():
      form.save()
      group = Group.objects.get(name=form.data['name'])
      group.user_set.add(request.user)
      context = RequestContext(request)
      if request.user.is_authenticated():
        context['user'] = request.user
        context['isLoggedin'] = True
      context['registered'] = True
      context['groupssection'] = True
      return render_to_response('base/newgroup.html', context)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  else:
    form = GroupCreateForm() # An unbound form
    context = RequestContext(request)
    if request.user.is_authenticated():
      context['user'] = request.user
      context['isLoggedin'] = True
    context['form'] = form
    context['groupssection'] = True
    return render_to_response('base/newgroup.html', context)
        
def login(request):
  def errorHandle(error):
    form = LoginForm()
    context = RequestContext(request)
    context['error'] = error
    context['form'] = form
    return render_to_response('base/login.html', context)
        
  if request.method == 'POST': # If the form has been submitted...
    form = LoginForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      username = request.POST['username']
      password = request.POST['password']
      user = auth.authenticate(username=username, password=password)
      if user is not None:
        if user.is_active:
          # Redirect to a success page.
          auth.login(request, user)
          context = RequestContext(request)
          context['user'] = user
          context['isLoggedin'] = True
          return render_to_response('base/index.html', context)
        else:
          # Return a 'disabled account' error message
          error = u'account disabled'
          return errorHandle(error)
      else:
        # Return an 'invalid login' error message.
        error = u'invalid login'
        return errorHandle(error)
    else:
      error = u'form is invalid'
      return errorHandle(error)
  else:
    form = LoginForm() # An unbound form
    context = RequestContext(request)
    context['form'] = form
    return render_to_response('base/login.html', context)

    
def logout(request):
  auth.logout(request)
  context = RequestContext(request)
  return render_to_response('base/index.html', context)