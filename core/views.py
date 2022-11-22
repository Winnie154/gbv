from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.shortcuts import render, redirect
from django.utils import timezone
from djqscsv import render_to_csv_response

from accounts.models import UserRoles
from core.forms import IncidentForm
from core.models import Counties, Incident, IncidentEventType, IncidentEvent, PoliceStation


def empty(request):
    return redirect('dashboard')


@login_required
def report_case(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)

        if form.is_valid():

            try:
                victim = User.objects.get(pk=form.cleaned_data['victim_id'])
            except User.DoesNotExist:
                messages.warning(request, 'Victim not found')
                return redirect('report')

            incident = form.save(commit=False)
            incident.user = victim
            incident.save()
            return redirect('cases')
        else:
            pass
            # messages.warning(request, form.errors)

    return render(request, 'core/dashboard.html', {
        'counties': [{'key': x[0], 'value': x[1]} for x in Counties.choices],
        'victims': User.objects.filter(profile__role='User')
    })


@login_required
def dashboard(request):
    if request.user.profile.role.lower() != 'user':
        messages.warning(request,
                         'You are not authorized to view this page. Use alternative login to login with your role')
        return redirect('logout')
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
    context = {
        'counties': [{'key': x[0], 'value': x[1]} for x in Counties.choices]
    }
    return render(request, 'core/report case.html', context)


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
        'incidents': Incident.objects.filter(station=PoliceStation.objects.filter(ocs=request.user).first()).order_by('-pk'),
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
        'other_police': [x for x in case.station.police.all() if x not in case.police.all()]
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
    station = PoliceStation.objects.filter(ocs=request.user)
    if not station.exists():
        messages.warning(request, 'You are not allowed to view this page')
        return redirect('dashboard')
    station = station.first()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.role = UserRoles.POLICE
            profile.save()
            station.police.add(user)
            messages.success(request, 'Police Created Successfully')
            return redirect("create-police")
        messages.warning(request, form.errors)

    context = {
        'police': station.police.all()
    }
    return render(request, 'core/admin_add_police.html', context)


@login_required
def ipoa_dashboard_view(request):
    if request.method == 'POST':
        pending_event = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.PENDING)
        police_added_event = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.POLICE_ADDED)
        police_removed_event = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.POLICE_REMOVED)
        investigation_started = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.INVESTIGATION_STARTED)
        case_in_court_event = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.CASE_IN_COURT)
        case_closed_event = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.CASE_CLOSED)
        station_assigned_event = IncidentEvent.objects.filter(incident=OuterRef('pk')) \
            .filter(type=IncidentEventType.STATION_ASSIGNED)
        case_status = IncidentEvent.objects.filter(incident=OuterRef('pk')).order_by('-pk')

        qs = Incident.objects.annotate(case_reported_at=Subquery(pending_event.values('date_created')[:1])) \
            .annotate(station_assigned_at=Subquery(station_assigned_event.values('date_created')[:1])) \
            .annotate(police_added_at=Subquery(police_added_event.values('date_created')[:1])) \
            .annotate(investigation_at=Subquery(investigation_started.values('date_created')[:1])) \
            .annotate(case_in_court_at=Subquery(case_in_court_event.values('date_created')[:1])) \
            .annotate(case_closed_at=Subquery(case_closed_event.values('date_created')[:1])) \
            .annotate(police_removed_at=Subquery(police_removed_event.values('date_created')[:1])) \
            .annotate(case_status=Subquery(case_status.values('type')[:1])) \
            .values('user__username', 'offence_category', 'date_of_incident', 'county_of_incident',
                    'location_of_incident', 'reported_by',
                    'perpetrator_name', 'relationship_to_perpetrator', 'station__name',
                    'user__profile__id_number', 'station__ocs__profile__id_number', 'case_reported_at',
                    'investigation_at', 'police_added_at', 'police_removed_at', 'case_in_court_at', 'case_closed_at',
                    'station_assigned_at', 'case_status'
                    )
        print(f"QS :: {qs}")
        fields_map = {
            'user__username': 'Victim Name',
            'user__profile__id_number': 'Victim ID Number',
            'offence_category': 'Offence Category',
            'date_of_incident': 'Date of Incident',
            'county_of_incident': 'County of Incident',
            'location_of_incident': 'Location of Incident',
            'perpetrator_name': 'Perpetrator Name',
            'case_status': 'Case Status',
            'relationship_to_perpetrator': 'Relationship to Perpetrator',
            'station__name': 'Station Name',
            'station__ocs__profile__id_number': 'OCS ID',
            'case_reported_at': 'Reported At',
            'station_assigned_at': 'Station Assigned At',
            'police_added_at': 'Police Added At',
            'investigation_at': 'Investigation Started At',
            'case_in_court_at': 'Case Taken To Court At',
            'police_removed_at': 'Police Removed At',
            'case_closed_at': 'Case Closed At',
            'reported_by': 'Reported By'
        }

        field_modifier = {
            'case_reported_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
            'investigation_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
            'police_added_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
            'police_removed_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
            'case_in_court_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
            'case_closed_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
            'station_assigned_at': (lambda x: x.strftime('%Y/%m/%d %H:%M:%S') if isinstance(x, datetime) else None),
        }

        return render_to_csv_response(
            qs, field_header_map=fields_map, append_datestamp=True, field_serializer_map=field_modifier)

    return render(request, 'core/ipol-dashboard.html', {'incidents': Incident.objects.all().order_by('-pk')})


@login_required
def ipoa_case_details_view(request, incident_id):
    try:
        case = Incident.objects.get(pk=incident_id)
    except Incident.DoesNotExist:
        messages.warning(request, 'The incident does not exist')
        return redirect('ipoa-dashboard')

    if request.method == 'POST':
        pass
        return redirect('ipoa-case-details', incident_id)

    context = {
        'case': case,
        'stations': PoliceStation.objects.filter(county=case.county_of_incident)
    }

    return render(request, 'core/ipoa-case-details.html', context)


@login_required
def ipoa_case_assign_view(request, incident_id):
    if request.method == 'POST':
        station_id = request.POST.get('station')
        try:
            station_ = PoliceStation.objects.get(pk=station_id)
        except PoliceStation.DoesNotExist:
            messages.warning(request, f'Station with id {station_id} does not exist')
            return redirect('ipoa-dashboard')

        try:
            incident_ = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            messages.warning(request, 'Incident does not exist. Refresh and try again')
            return redirect('ipoa-dashboard')

        station_.incident_set.add(incident_)
        IncidentEvent.objects.create(incident=incident_, type=IncidentEventType.STATION_ASSIGNED, event_by=request.user, desc='Station assigned')
        station_.save()
        messages.success(request, f'Incident has been assigned to Station {station_.pk} [ {station_.name} ]')
        return redirect('ipoa-case-details', incident_id=incident_id)


@login_required
def cases_report_view(request):
    pass