from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

import teachers
from teachers.models import Teacher
from courses.models import Course

from django.shortcuts import render
from django.template import RequestContext
from teachers.forms import TeacherCreateForm

from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class GetTeachers(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = Teacher
    template_name = 'show_teachers.html'

    def get_context_data(self, **kwargs):
        # method must return a dict like 'extra_context' was
        course_id = self.kwargs.get('course')
        teachers = self.model.objects.all()
        courses = Course.objects.all()

        if course_id:
            teachers = teachers.filter(course__id__contains=course_id)
        return {
            'teachers_list': teachers,
            'courses_list': courses
        }


def search_teachers(request):
    search_text = request.GET.get('search')
    text_fields = ["first_name", "last_name", "email", 'course__name']

    if search_text:
        or_filter = Q()
        for field in text_fields:
            or_filter |= Q(**{f"{field}__icontains": search_text})
        teachers = Teacher.objects.filter(or_filter)
    else:
        teachers = Teacher.objects.all()

    return render(
        request=request,
        template_name="show_teachers.html",
        context={"teachers_list": teachers},
    )


class CreateTeacher(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('sign_in')
    template_name = 'create_teacher.html'
    fields = "__all__"
    model = Teacher
    success_url = reverse_lazy('teachers:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # TODO: add validation to the model 'validator' list!!
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            return super().form_invalid(form)
        return super().form_valid(form)


class UpdateTeacher(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('sign_in')
    template_name = 'edit_teacher.html'
    fields = "__all__"
    model = Teacher
    success_url = reverse_lazy('teachers:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            return super().form_invalid(form)
        return super().form_valid(form)


class DeleteTeacher(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign_in')
    model = Teacher
    success_url = reverse_lazy('teachers:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
