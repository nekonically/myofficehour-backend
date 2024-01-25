from django.shortcuts import render
from Myofficehour.models import Officehour,Status,Location,Participant
from datetime import date
from django.http import HttpRequest
from .forms import ParticipantForm
from django.db.models import Max, Count
from django.views.generic.list import ListView
from django.db.models import OuterRef, Subquery
from django.views.generic.detail import DetailView
def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get the first IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')  # Get the direct IP address
    return ip

def index(request: HttpRequest):
    form = ParticipantForm()

    today = date.today()

    payload = {
        "date": today,
        "id": None,
        "time": None,
        "isTodayOfficeHourExist": False,
        "location": None,
        "status": None,
        "last":{
            "time": None,
            "isLastOfficeHourExist": False,
            "location": None,
            "status": None,
        },
        "next": {
            "time": None,
            "isNextOfficeHourExist": False,
            "location": None,
            "status": None,
        }
    }

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ParticipantForm(request.POST)
        try:
            ip_address = get_client_ip(request)
        except Exception as e:
            raise Exception('IP acquisition failed')

        try:
            form.ip = ip_address
        except Exception:
            raise Exception('form IP insertion failed')


        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            email = form.cleaned_data["email"]
            officehourID = int(form.data["id"])
            ip = ip_address

            Participant.objects.create(officehour_id=officehourID,email=email,ip=ip)


            # redirect to a new URL:
            return render(request, 'success.html')
        if not form.is_valid():
            raise Exception("form validation failed "+form.errors)
        else:
            raise Exception('user form not valid')

    # if a GET (or any other method) we'll create a blank form
    elif request.method == "GET":
        # Current
        try:
            current = Officehour.objects.filter(when__date=today).latest('when')
            payload["id"] = current.id
            payload["isTodayOfficeHourExist"] = True
            payload["time"] = current.when
            payload["location"] = Location.objects.filter(officehour=current.id).latest("created_at").location
            payload["status"] = Status.objects.filter(officehour=current).latest("created_at").get_status_display

        except Officehour.DoesNotExist:
            pass

        except Status.DoesNotExist:
            pass

        except Location.DoesNotExist:
            pass

        # Last
        try:
            last = Officehour.objects.filter(when__date__lt=today).latest('when')
            payload["last"]["isLastOfficeHourExist"] = True
            payload["last"]["time"] = last.when
            payload["last"]["location"] = Location.objects.filter(officehour=last.id).latest("created_at").location
            payload["last"]["status"] = Status.objects.filter(officehour=last).latest("created_at").get_status_display

        except Officehour.DoesNotExist:
            pass

        except Status.DoesNotExist:
            pass

        except Location.DoesNotExist:
            pass

        # Last
        try:
            next = Officehour.objects.filter(when__date__gt=today).latest('when')
            payload["next"]["isLastOfficeHourExist"] = True
            payload["next"]["time"] = next.when
            payload["next"]["location"] = Location.objects.filter(officehour=next.id).latest("created_at").location
            payload["next"]["status"] = Status.objects.filter(officehour=next).latest("created_at").get_status_display

        except Officehour.DoesNotExist:
            pass

        except Status.DoesNotExist:
            pass

        except Location.DoesNotExist:
            pass

        return render(request, 'index.html', {'payload': payload, 'form': form})



    raise NotImplementedError('user requested non implemented request.')

class OfficehourListView(ListView):
    paginate_by = 30
    template_name = 'listview.html'
    context_object_name = 'officehour_list'



    def get_queryset(self):
        latest_location = Subquery(Location.objects.filter(
            officehour=OuterRef("pk"),
        ).order_by("-created_at").values('location')[:1])

        latest_status = Subquery(
            Status.objects.filter(
                officehour=OuterRef("pk")
            ).order_by("-created_at").values('status')[:1]
        )

        count_participant = Subquery(
            Participant.objects.filter(
                officehour=OuterRef("pk")
                    ).values('officehour').annotate(count=Count('pk')).values('count')[:1])

        # Annotate each user with the date of their latest update
        return Officehour.objects.annotate(latestLocation=latest_location,latestStatus=latest_status,countParticipant=count_participant)


class OfficehourDetailView(DetailView):
    model = Officehour
    template_name = "detailview.html"

