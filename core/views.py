from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.forms import IncidentForm
from core.models import Counties, Incident, IncidentEventType, IncidentEvent


def empty(request):
    return redirect('dashboard')


@login_required
def dashboard(request):

    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.user = request.user
            incident.save()
            return redirect('cases')
        else:
            pass
            # messages.warning(request, form.errors)

    return render(request, 'core/dashboard.html')


@login_required
def cases_views(request):

    context = {
        'incidents': Incident.objects.filter(user=request.user).order_by('-pk'),
        'counties': [{'key': x[0], 'value': x[1]} for x in Counties.choices]
    }
    return render(request, 'core/report case.html', context)


@login_required
def police_dashboard(request):
    _incidents = Incident.objects.filter(police=request.user).order_by('-pk')
    context = {
        'incidents': _incidents,
    }
    return render(request, 'core/police-dashboard.html', context)


@login_required
def case_details(request, incident_id):
    try:
        case = Incident.objects.get(pk=incident_id)
    except Incident.DoesNotExist:
        # messages.warning(request, 'The incident does not exist')
        return redirect('police-dashboard')

    if not case.police.all().contains(request.user):
        # messages.warning(request, 'You are not authorized to view this case')
        return redirect('police-dashboard')

    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            status_ = IncidentEventType(status)
        except ValueError:
            # messages.warning(request, f'Invalid status ({status}) selected. Refresh and try again')
            return redirect('case-details', incident_id)
        event = IncidentEvent()
        event.type = status_
        event.incident = case
        event.event_by = request.user
        event.save()
        # messages.success(request, 'Case Status Updated Successfully')
        return redirect('case-details', incident_id)

    context = {
        'events': [{'key': x[0], 'value': x[1]} for x in IncidentEventType.choices],
        'case': case
    }

    return render(request, 'core/police-case-details.html', context)
