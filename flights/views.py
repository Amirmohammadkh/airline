from django.shortcuts import render
from .models import Flight, Airport, Passenger
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# Create your views here.


def index(request):
    return render(request, 'flights/index.html', {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    try:
        f = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found!")
    p = f.passengers.all()
    non_p = Passenger.objects.exclude(flights=f).all()
    return render(request, 'flights/flight.html', {
        "flight": f,
        "passengers": p,
        "non_passenger": non_p
    })


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger_id = int(request.POST['passenger'])
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args=(flight.id,)))
