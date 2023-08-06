# -*- coding: utf-8 -*-
import os

import django


def create_taiga_account():
    from .models import TaigaAccount

    nhandd3_account, created = TaigaAccount.objects.get_or_create(
        username='nhandd3', password='nhandd3', defaults={'domain': 'http://172.27.228.249:9000'}
    )
    print(f'create taiga account {nhandd3_account}: {created=}')


def create_taiga_api():
    # MUST create taiga account BEFORE running this function
    from .models import TaigaAccount, TaigaApi

    account = TaigaAccount.get_account_nhandd3()

    df_type = TaigaApi.API_TYPE.FETCH
    df_auth = TaigaApi.AUTH_TYPE.BEARER
    for slug, type, auth_type, curl in (
        (
            '/api/v1/auth',
            TaigaApi.API_TYPE.AUTH,
            TaigaApi.AUTH_TYPE.NONE,
            """curl  -X POST 'http://172.27.228.249:9000/api/v1/auth' -H 'Content-Type: application/json' --data '{    "password": "nhandd3@123",    "type": "normal",    "username": "nhandd3"}'""",
        ),
        (
            '/api/v1/users:get_all_users',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/users' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw'""",
        ),
        (
            '/api/v1/projects:get_all_projects',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/projects' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTU3MjM3LCJqdGkiOiIwZmU2Y2NkYmNmNzU0M2U5YTIzYjQ5MmY0ZWQxY2M2YiIsInVzZXJfaWQiOjQwfQ.SohaCnO_aDjsIelWDIA_q5OWi7GGAD7lXKtZWpr9jgM'""",
        ),
        (
            '/api/v1/issues:get_all_issues',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/issues' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTU3MjM3LCJqdGkiOiIwZmU2Y2NkYmNmNzU0M2U5YTIzYjQ5MmY0ZWQxY2M2YiIsInVzZXJfaWQiOjQwfQ.SohaCnO_aDjsIelWDIA_q5OWi7GGAD7lXKtZWpr9jgM' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/issue-statuses:get_all_issue_statuses',
            df_type,
            df_auth,
            """curl -L -X GET 'http://172.27.228.249:9000/api/v1/issue-statuses' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/issues?project=:project_id',
            df_type,
            df_auth,
            """curl -L -X GET 'http://172.27.228.249:9000/api/v1/issues?project=26' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5Mjg0Njc1LCJqdGkiOiIzMmQ0NThlY2ZhMzE0MjgyYTk1MmVkYzFmZTU4Y2ZkYyIsInVzZXJfaWQiOjQwfQ.jFMvKh29HP-BQNALgYlSyJyKd61n2kwsVuql6JkSZjg' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/tasks:get_all_tasks',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/tasks' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/task-statuses:get_all_task_statuses',
            df_type,
            df_auth,
            """curl -L -X GET 'http://172.27.228.249:9000/api/v1/task-statuses' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/tasks?project=:project_id',
            df_type,
            df_auth,
            """curl -L -X GET 'http://172.27.228.249:9000/api/v1/tasks?project=26' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5Mjg0Njc1LCJqdGkiOiIzMmQ0NThlY2ZhMzE0MjgyYTk1MmVkYzFmZTU4Y2ZkYyIsInVzZXJfaWQiOjQwfQ.jFMvKh29HP-BQNALgYlSyJyKd61n2kwsVuql6JkSZjg' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/milestones:get_all_milestones',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/milestones' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/userstories:get_all_userstories',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/userstories' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/userstory-statuses:get_all_userstory_statuses',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/userstory-statuses' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/epics:get_all_epics',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/epics' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
        (
            '/api/v1/epic-statuses:get_all_epic_statuses',
            df_type,
            df_auth,
            """curl  -X GET 'http://172.27.228.249:9000/api/v1/epic-statuses' -H 'Content-Type: application/json' -H 'Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5MTk1OTY4LCJqdGkiOiJjY2Q3MzAyMGJmOWQ0MmQ1YTJmNmRlNmFkYWVmMTZmZCIsInVzZXJfaWQiOjQwfQ.LYJzeyt4NJyy2ItVq5Vy5NzI_fybA9eFyYEQzJR0Skw' -H 'x-disable-pagination: True'""",
        ),
    ):
        new_api, created = TaigaApi.objects.get_or_create(
            account=account,
            slug=slug,
            type=type,
            auth_type=auth_type,
            defaults={
                'curl': curl,
            },
        )
        print(f'create new taiga api {new_api}: {created=}')
