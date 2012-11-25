# Create your views here.
from rapidsms.contrib.messagelog.models import Message
from ox.django.shortcuts import render_to_json_response

def messages_json(request):
    phone_no = request.GET.get("phone_no", None)
    #TODO: validate phone no
    if not phone_no:
        return render_to_json_response({'error': 'no phone number provided'})
    messages = Message.objects.filter(connection__identity__endswith=phone_no)
    ret = []
    for m in messages:
        ret.append({
            'text': m.text,
            'direction': m.direction,
            'datetime': m.date.isoformat()
        })
    return render_to_json_response(ret)
