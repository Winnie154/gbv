from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.forms import IncidentForm
from core.models import Counties, Incident


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
            messages.warning(request, form.errors)

    return render(request, 'core/dashboard.html')


@login_required
def cases_views(request):

    context = {
        'incidents': Incident.objects.filter(user=request.user).order_by('-p'),
        'counties': [{'key': x[0], 'value': x[1]} for x in Counties.choices]
    }
    return render(request, 'core/report case.html', context)
