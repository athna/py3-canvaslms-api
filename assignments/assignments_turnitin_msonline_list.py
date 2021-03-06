# https://canvas.instructure.com/doc/api/assignments.html
from datetime import datetime

from canvas.core.courses import get_courses, get_courses_whitelisted, get_course_people, get_courses_by_account_id
from canvas.core.io import write_xlsx_file, tada

from canvas.core.assignments import get_assignments


def assignments_turnitin_msonline_list():
    terms = ['2017-1SP']
    programs = ['NFNPO', 'NCMO']
    synergis = True
    course_whitelist = get_courses_whitelisted([])
    header = ['term', 'program', 'SIS ID', 'course name', 'assignment name', 'assignment URL', 'due date', 'points',
              'group assignment', 'faculty of record']
    rows = []

    for course in course_whitelist or get_courses(terms, programs, synergis):
        course_id = course['id']
        if not get_course_people(course_id, 'student'):
            continue
        course_sis_id = course['sis_course_id']
        program = course['course_sis_info']['program']
        for assignment in get_assignments(course_id):
            if 'external_tool' in assignment['submission_types']:
                row = [terms[0],
                       program,
                       course_sis_id,
                       course['name'],
                       assignment['name'],
                       assignment['html_url'],
                       assignment['due_at'][0:10] if assignment['due_at'] else '',
                       assignment['points_possible'] if assignment['points_possible'] else '',
                       'X' if 'group_category_id' in assignment and assignment['group_category_id'] else '',
                       ', '.join([p['name'] for p in get_course_people(course_id, 'Faculty of record')])]
                rows.append(row)
                print(row)

    write_xlsx_file('turnitin_assignments_spring_{}'
                    .format(datetime.now().strftime('%Y.%m.%d.%H.%M.%S')), header, rows)


def assignments_turnitin_msonline_list_dev():
    accounts = {'DEV FNPO': '168920', 'DEV CMO': '168922'}
    header = ['program', 'course name', 'assignment name', 'assignment URL', 'points']
    rows = []
    for account in accounts:
        for course in get_courses_by_account_id(accounts[account], 'DEFAULT'):
            course_id = course['id']
            for assignment in get_assignments(course_id):
                if 'external_tool' in assignment['submission_types']:
                    row = [
                           account,
                           course['name'],
                           assignment['name'],
                           assignment['html_url'],
                           assignment['points_possible'] if assignment['points_possible'] else '']
                    rows.append(row)
                    print(row)

    write_xlsx_file('turnitin_assignments_spring_dev_{}'
                    .format(datetime.now().strftime('%Y.%m.%d.%H.%M.%S')), header, rows)

if __name__ == '__main__':
    # assignments_turnitin_msonline_list()
    assignments_turnitin_msonline_list_dev()
    tada()
