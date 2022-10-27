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
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.user = request.user
            incident.save()
            return redirect('dashboard')
        else:
            messages.warning(request, form.errors)

    context = {
        'incidents': Incident.objects.filter(user=request.user),
        'counties': [{'key': x[0], 'value': x[1]} for x in Counties.choices]
    }
    return render(request, 'core/dashboard.html', context)
