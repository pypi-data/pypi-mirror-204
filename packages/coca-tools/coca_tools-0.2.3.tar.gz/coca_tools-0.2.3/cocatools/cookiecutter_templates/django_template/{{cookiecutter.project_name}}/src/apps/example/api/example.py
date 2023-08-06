# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
@csrf_exempt
def get_example_unauthenticated_api(request):
    rdata = parse_pydantic_obj(ProjectWeeklyReportRequest, request.data)
    try:
        project = TaigaProject.objects.get(taiga_pid=rdata.project_id)
    except ObjectDoesNotExist:
        return error_api_resp(f'project {rdata.project_id} is not exist')
    data = get_taiga_project_weekly_report(project, rdata.at_datetime)
    return success_api_resp(data=data)



@api_view(('POST',))
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_example_authenticated_api(request):
    rdata = parse_pydantic_obj(ProjectWeeklyReportRequest, request.data)
    try:
        project = TaigaProject.objects.get(taiga_pid=rdata.project_id)
    except ObjectDoesNotExist:
        return error_api_resp(f'project {rdata.project_id} is not exist')
    data = get_taiga_project_weekly_report(project, rdata.at_datetime)
    return success_api_resp(data=data)
