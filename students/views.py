from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from webargs.djangoparser import use_args, DjangoParser
from django.core.exceptions import BadRequest
from webargs import fields
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from students.forms import StudentCreateForm, TeacherCreateForm
from students.models import Student, Teacher, Course

from django.shortcuts import render
from django.template import RequestContext


parser = DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def handle_error_404(request, exception):
    context = RequestContext(request)
    response = render('404.html', context)
    response.status_code = 404
    return response


def index(request):
    return render(
        request=request,
        template_name='index.html',
        context={
            'param1': ' some output '
        }
    )


@use_args({
    "course": fields.Str(
        required=False
    )},
    location="query"
)
def get_students(request, params):
    students_rec = Student.objects.all()
    courses_rec = Course.objects.all()

    text_fields = ['first_name', 'last_name', 'email', 'course__name']

    if request.method == 'GET':
        search_text = request.GET.get('search_box', None)
        if search_text:
            or_filter = Q()
            for field in text_fields:
                or_filter |= Q(**{f'{field}__contains': search_text})
            students_rec = students_rec.filter(or_filter)

    if params:
        students_rec = students_rec.filter(course__id__contains=params['course'])

    return render(
        request=request,
        template_name='show_students.html',
        context={'students_list': students_rec,
                 'courses_list': courses_rec}
    )


# misses url defining and 'name' specification in 'Search' form element
# plus! redirect via form 'action' on specific search-view
# def search_view(request):
#     search_text = request.GET.get('search')
#     text_fields = ["first_name", "last_name", "email"]
#     print(request.GET)
#
#     if search_text:
#         or_filter = Q()
#         for field in text_fields:
#             or_filter |= Q(**{f"{field}__icontains": search_text})
#         students = Student.objects.filter(or_filter)
#     else:
#         students = Student.objects.all().order_by("-id")
#
#     return render(
#         request=request,
#         template_name="students_table.html",
#         context={"students_list": students},
#     )


@csrf_exempt
def create_student(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # here can be added invitation check and creation of an Invitation instance
            return HttpResponseRedirect(reverse('students:list'))

    form = StudentCreateForm()

    return render(
        request=request,
        template_name='create-student.html',
        context={'create_form': form}
    )


@csrf_exempt
def update_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        form = StudentCreateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    form = StudentCreateForm(instance=student)

    return render(
        request=request,
        template_name='edit.html',
        context={'edit_form': form}
    )


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))



@use_args({
    "course": fields.Str(
        required=False
    )},
    location="query"
)
def get_teachers(request, params):
    teachers_rec = Teacher.objects.all()
    courses_rec = Course.objects.all()

    text_fields = ['first_name', 'last_name', 'email', 'course__name']

    if request.method == 'GET':
        search_text = request.GET.get('search_box', None)
        if search_text:
            or_filter = Q()
            for field in text_fields:
                or_filter |= Q(**{f'{field}__contains': search_text})
            teachers_rec = teachers_rec.filter(or_filter)

    if params:
        teachers_rec = teachers_rec.filter(course__id__contains=params['course'])

    return render(
        request=request,
        template_name='show_teachers.html',
        context={'teachers_list': teachers_rec,
                 'courses_list': courses_rec}
    )


@csrf_exempt
def create_teacher(request):

    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:teachers'))

    form = TeacherCreateForm()

    return render(
        request=request,
        template_name='create_teacher.html',
        context={'create_teacher': form}
    )
