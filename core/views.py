from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.models import UserRoles
from core.forms import IncidentForm
from core.models import Counties, Incident, IncidentEventType, IncidentEvent


def empty(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin-dashboard')
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
        messages.warning(request, 'The incident does not exist')
        return redirect('police-dashboard')

    if not case.police.all().contains(request.user):
        messages.warning(request, 'You are not authorized to view this case')
        return redirect('police-dashboard')

    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            status_ = IncidentEventType(status)
        except ValueError:
            messages.warning(request, f'Invalid status ({status}) selected. Refresh and try again')
            return redirect('case-details', incident_id)
        event = IncidentEvent()
        event.type = status_
        event.incident = case
        event.event_by = request.user
        event.save()
        messages.success(request, 'Case Status Updated Successfully')
        return redirect('case-details', incident_id)

    context = {
        'events': [{'key': x[0], 'value': x[1]} for x in IncidentEventType.choices],
        'case': case
    }

    return render(request, 'core/police-case-details.html', context)


@login_required
def admin_dashboard(request):
    context = {
        'incidents': Incident.objects.order_by('-pk'),
    }
    return render(request, 'core/admin-dashboard.html', context)


@login_required
def admin_case_details(request, incident_id):
    try:
        case = Incident.objects.get(pk=incident_id)
    except Incident.DoesNotExist:
        messages.warning(request, 'The incident does not exist')
        return redirect('admin-dashboard')

    if request.method == 'POST':
        pass
        return redirect('admin-case-details', incident_id)

    context = {
        'case': case,
        'other_police': [x for x in User.objects.filter(profile__role='Police') if x not in case.police.all()]
    }

    return render(request, 'core/admin-case-details.html', context)


@login_required
def add_police_to_case(request, incident_id):
    if request.method == 'POST':
        print("adding police")
        try:
            case = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            messages.warning(request, 'The incident does not exist')
            print('The incident does not exist')
            return redirect('admin-dashboard')

        police_id = request.POST.get('police_id')
        try:
            police = User.objects.get(pk=police_id)
        except User.DoesNotExist:
            messages.warning(request, 'Police does not exist')
            print('Police does not exist')
            return redirect('admin-dashboard')

        if police.profile.role != UserRoles.POLICE:
            messages.warning(request, 'Selected user is not a police')
            print('Selected user is not a police')
            return redirect('admin-dashboard')

        case.police.add(police)
        case.incidentevent_set.add(IncidentEvent.objects.create(incident=case, event_by=request.user, type=IncidentEventType.POLICE_ADDED))
        case.save()
        messages.success(request, 'Police added to case')
        print('Police added to case')
        return redirect('admin-case-details', incident_id=incident_id)


@login_required
def remove_police(request, incident_id):
    if request.method == 'POST':
        try:
            case = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            messages.warning(request, 'The incident does not exist')
            print('The incident does not exist')
            return redirect('admin-dashboard')

        police_id = request.POST.get('police_id')
        try:
            police = User.objects.get(pk=police_id)
        except User.DoesNotExist:
            messages.warning(request, 'Police does not exist')
            print('Police does not exist')
            return redirect('admin-dashboard')

        if police.profile.role != UserRoles.POLICE:
            messages.warning(request, 'Selected user is not a police')
            print('Selected user is not a police')
            return redirect('admin-dashboard')

        if police not in case.police.all():
            messages.warning(request, 'Police is not in this case')
            print('Police is not in this case')
            return redirect('admin-dashboard')

        case.police.remove(police)
        case.incidentevent_set.add(
            IncidentEvent.objects.create(incident=case, event_by=request.user, type=IncidentEventType.POLICE_REMOVED))
        case.save()
        messages.success(request, 'Police Removed From Case')
        print("Police Removed From Case")
        return redirect('admin-case-details', incident_id=incident_id)


@login_required
def create_police(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.role = UserRoles.POLICE
            profile.save()
            messages.success(request, 'Police Created Successfully')
            return redirect("create-police")
        messages.warning(request, form.errors)

    context = {
        'police': User.objects.filter(profile__role=UserRoles.POLICE)
    }
    return render(request, 'core/admin_add_police.html', context)
