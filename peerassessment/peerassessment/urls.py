from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
import app

urlpatterns = patterns('',
    # Common Ajax Endpoints
    url(r'^register$', 'app.views.ajax.register'),
    url(r'^login$', 'app.views.ajax.login_user'),
    url(r'^logout$', 'app.views.ajax.logout_user'),

    # Assignments Endpoints
    url(r'^assignment/create$', 'app.views.assignments.create'),
    url(r'^assignment/edit$', 'app.views.assignments.edit'),
    url(r'^assignment/submit$', 'app.views.assignments.submit'),
    url(r'^assignment/message$', 'app.views.assignments.send_messages'),

    # HTML Endpoints
    url(r'^signup/$', 'app.views.html.signup'),
    url(r'^student/$', 'app.views.html.student_dashboard'),
    url(r'^student/assignment/(?P<assignment_id>\d+)/discussion$','app.views.html.discussion_page'),
    url(r'^student/assignment/(?P<assignment_id>\d+)/submit$', 'app.views.html.submit_assignment_page'),
    url(r'^professor/$', 'app.views.html.professor_dashboard'),
    url(r'^professor/assignment/create$', 'app.views.html.create_assignment_page'),
    url(r'^professor/assignment/(?P<assignment_id>\d+)/edit$', 'app.views.html.edit_assignment_page'),
    url(r'^professor/course/create$', 'app.views.html.create_course_page'),
    url(r'^$', 'app.views.html.index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
