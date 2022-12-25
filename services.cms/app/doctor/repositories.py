from doctor.models import Doctor, WorkingShift
from shared.utils import WEEK_DAYS
from django.db import connection
from django.db.models.query import RawQuerySet

def get_doctors_with_name(name: str) -> RawQuerySet:
    name = f'%{name}%'
    stmt = f'''
        SELECT d.*, s.id AS 'specialist_id', s.name AS 'specialist_name', s.description AS 'specialist_desc'
        FROM doctor d
        INNER JOIN doctor_specialist ds ON d.id = ds.doctor_id
        INNER JOIN specialist s ON ds.specialist_id = s.id
        WHERE (LOWER(d.firstName) LIKE %s OR LOWER(d.lastName) LIKE %s) AND d.isApproved = 1
        GROUP BY d.id;
    '''
    # with connection.cursor() as cursor:
    #     cursor.execute(stmt, [name, name])
    #     rows = cursor.fetchall()
    #     results = [  ]
    #     return results
    queryset = Doctor.objects.raw(stmt, [name, name])
    return queryset

def manager_get_doctors_with_name(name: str) -> RawQuerySet:
    name = f'%{name}%'
    stmt = f'''
        SELECT d.*, s.id AS 'specialist_id', s.name AS 'specialist_name', s.description AS 'specialist_desc'
        FROM doctor d
        INNER JOIN doctor_specialist ds ON d.id = ds.doctor_id
        INNER JOIN specialist s ON ds.specialist_id = s.id
        WHERE (LOWER(d.firstName) LIKE %s OR LOWER(d.lastName) LIKE %s)
        GROUP BY d.id;
    '''
    queryset = Doctor.objects.raw(stmt, [name, name])
    return queryset

def generate_shifts(doctor: Doctor):
    shifts = []
    for k, v in WEEK_DAYS.items():
        shifts.append(WorkingShift(
            doctor = doctor,
            weekday = v,
            isActive = True,
        ))
    return shifts