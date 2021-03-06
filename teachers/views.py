from django.db.models import Q
from django.urls import reverse_lazy
from django.forms.utils import ErrorList

from teachers.models import Teacher
from courses.models import Course

from django.views.generic import (CreateView, ListView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class GetTeachers(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = Teacher
    template_name = 'show_teachers.html'

    def get_context_data(self, **kwargs):
        # method must return a dict like 'extra_context' was
        course_id = self.request.GET.get('course')
        teachers = self.model.objects.all()
        courses = Course.objects.all()

        if course_id:
            teachers = teachers.filter(course__id__contains=course_id)
        return {
            'teachers_list': teachers,
            'courses_list': courses
        }


class SearchTeacher(ListView):
    model = Teacher
    template_name = 'show_teachers.html'

    def get_context_data(self, **kwargs):
        search_text = self.request.GET.get('search')
        teachers = self.model.objects.all()
        text_fields = ["first_name", "last_name", "email", 'course__name']

        if search_text:
            or_filter = Q()
            for field in text_fields:
                or_filter |= Q(**{f"{field}__icontains": search_text})
            teachers = Teacher.objects.filter(or_filter)

        return {
            'teachers_list': teachers
        }


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
            form._errors["first_name"] = ErrorList(
                ["First and last name cannot be equal, bro!"]
            )
            form._errors["last_name"] = ErrorList(
                ["First and last name cannot be equal, bro!"]
            )
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
            form._errors["first_name"] = ErrorList(
                ["First and last name cannot be equal, bro!"]
            )
            form._errors["last_name"] = ErrorList(
                ["First and last name cannot be equal, bro!"]
            )
            return super().form_invalid(form)
        return super().form_valid(form)


class DeleteTeacher(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign_in')
    model = Teacher
    success_url = reverse_lazy('teachers:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
