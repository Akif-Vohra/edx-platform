"""
A management command to calculate grade based on progress of student in particular course using courseware summary in
sections,subsections and chapters
"""

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_with_access
from django.contrib.auth.models import User
from courseware import grades
from util.db import outer_atomic


def get_score_section_wise(request,course_id):
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    with modulestore().bulk_operations(course_key):
        course = get_course_with_access(request.user, 'load', course_key, depth=None, check_if_enrolled=True)
        student = User.objects.prefetch_related("groups").get(id=student.id)

        with outer_atomic():
            field_data_cache = grades.field_data_cache_for_grading(course, student)
            scores_client = ScoresClient.from_field_data_cache(field_data_cache)

        courseware_summary = grades.progress_summary(
            student, request, course, field_data_cache=field_data_cache, scores_client=scores_client
        )
        print "Courseware summary is {0}".format(courseware_summary)
    print "out of modulestore"
