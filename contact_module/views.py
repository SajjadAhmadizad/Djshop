from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView

from django.conf import settings

from site_module.models import SiteSetting
from .forms import ContactUsForm, ContactUsModelForm, ProfileForm
from .models import ContactUs, UserProfile


# Create your views here.

def store_file(file):
    with open('temp/image.jpg', mode='wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


def ContactUsView(request):
    if request.method == "GET":
        form = ContactUsForm()
        site_setting = SiteSetting.objects.filter().first()
        return render(request, 'contact_module/contact-us.html', {"form": form, 'site_setting': site_setting})

    if request.method == "POST":
        # print(request.POST)
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            data = ContactUs(full_name=request.POST['full_name'], email=request.POST['email'],message=request.POST['text'], title=request.POST['subject'])
            data.save()
            response = render_to_string('contact_module/success-contact-us.html')
            return JsonResponse({
                'status': 'success',
                'body': response,
                'text': 'فرم تماس با ما با موفقیت ثبت شد!',
                'icon': 'success',
                'confirm_button_text': 'باشه.برو به خانه!'
            })
        else:
            return render(request,'contact_module/contact-us-component.html',{'form':contact_form})


# class CreateProfileView(View):
#     def get(self,request):
#         form = ProfileForm()
#         return render(request,'create-profile.html',{
#             'form':form
#         })
#
#     def post(self,request):
#         submited_form = ProfileForm(request.POST,request.FILES)
#
#         if submited_form.is_valid():
#             # store_file(request.FILES['profile'])
#             # print(request.FILES)
#             profile = UserProfile(image=request.FILES['user_image'])
#             profile.save()
#             return redirect(reverse('create-profile'))
#
#         # print(request.FILES)
#         form = ProfileForm()
#         return render(request, 'create-profile.html', {
#         'form': submited_form
#     })

class CreateProfileView(CreateView):
    template_name = 'create-profile.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile/'


class ProfileListView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list.html'
    context_object_name = 'profiles'

# class ContactUsView(FormView):
#     template_name = 'contact_module/contact-us.html'
#     form_class = ContactUsModelForm
#     # important : dar file html ba name <<form>> be in field ha dastresi darim
#     success_url = '/contact-us/'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         pass


# class ContactUsView(CreateView):
#     template_name = 'contact_module/contact-us.html'
#     # model = ContactUs
#     # fields = ['']
#     form_class = ContactUsModelForm
#     # form class hatman bayad modelform bashad
#     # important : dar file html ba name <<form>> be in field ha dastresi darim
#     success_url = '/contact-us/'
#
#     def get_context_data(self, *args,**kwargs):
#         context = super().get_context_data(*args,**kwargs)
#         context['site_setting']=SiteSetting.objects.filter(is_main_setting=True).first()
#
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         pass
#


# with class base view :

# class ContactUsView(View):
#     def get(self,request):
#         contact_form = ContactUsModelForm()
#         return render(request, 'contact_module/contact-us.html', {'contact_form': contact_form})
#
#     def post(self,request):
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect("home-page")
#
#         return render(request, 'contact_module/contact-us.html', {'contact_form': contact_form})


# with function base view :

# def contact_us(request):
#     # request.POST => returns a dictionary
#     # if request.method == 'POST':
#     #     print(request.POST)
#     #     print(request.POST['fullname'])
#     #     print(request.POST['subject'])
#     #     print(request.POST['message'])
#     #     entered_email = request.POST['email']
#     #
#     #     if entered_email == '':
#     #         return render(request,'contact_module/contact-us.html',{
#     #             'has_error':True
#     #         })
#     #     return redirect(reverse('home-page'))
#
#     # with django forms :
#     if request.method == 'POST':
#         # contact_form = ContactUsForm(request.POST)
#
#         # model forms :
#         contact_form = ContactUsModelForm(request.POST)
#         # -----------------------------------------
#         if contact_form.is_valid():
#             # Process form data
#             # print(contact_form.cleaned_data)
#             # contact = ContactUs(
#             #     title=contact_form.cleaned_data.get('subject'),
#             #     email=contact_form.cleaned_data.get('email'),
#             #     full_name=contact_form.cleaned_data.get('full_name'),
#             #     message=contact_form.cleaned_data.get('text')
#             # )
#             # contact.save()
#
#             # model forms :
#             contact_form.save()
#             # -----------------------------------------
#
#             return redirect('home-page')
#     else:
#         # contact_form = ContactUsForm()
#         contact_form = ContactUsModelForm()
#     return render(request, 'contact_module/contact-us.html', {'contact_form': contact_form})
