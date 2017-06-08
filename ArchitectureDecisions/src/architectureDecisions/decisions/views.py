from django.conf import settings
from django.shortcuts import render
from .models import Decision
from login.authenticator import *
from projects.models import *
from .models import Comment
import logging
import logging.handlers
import sqlite3
import json
from utils.smtp import *
from django.contrib.auth.models import User
import datetime



if not settings.DEBUG:
    #Logging
    log_path = "/volume/log"
    LOG_FILENAME = log_path + "/" + "architecture-decisions.log"
    logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=7)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)



def render_index(request):
    decision_id = request.GET.get('decision_id')
    user_is_authenticated = authenticated(request)
    decisions_list = Decision.objects.order_by('-notice_date','-id')
    for decision in decisions_list:
        try:
            decision.q_comments = Comment.objects.filter(affected_decision_id=decision.id, reply_to=None).count()
        except Exception:
            pass
    context = {
        'decisions_list': decisions_list,
        'user_authenticated': user_is_authenticated,
    }
    if user_is_authenticated:
        context['username'] = request.session['username']
    context['decision_for_modal'] = str(decision_id) if decision_id not in (None, '') else '-1'
    return render(request, 'decisions/index.html', context)


def decision(request):
    if request.method == 'GET':
        project_list = Project.objects.all()
        user_is_authenticated = authenticated(request)
        if not user_is_authenticated:
            return render(request, 'login.html', {})
        context = {
            'username': request.session["username"],
            'project_list': project_list
        }
        try:
            context['decision'] = Decision.objects.get(id=request.GET['decision_id'])
            context['decision'].effective_date = str(context['decision'].effective_date)
        except:
            pass
        return render(request, 'decisions/decision.html', context)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
        except Exception:
            body = json.loads(request.body)
        if body['bot']:
            usuario = body['usuario']
        else:
            try:
                usuario = request.session['username']
                if not body['effective_date']:
                    body['effective_date'] = None
            except Exception:
                return JsonResponse({"error": True}, safe=False)

        try:
            obj = Decision.objects.get(id=body['decision_id'])
            for key, value in body.items():
                setattr(obj, key, value)
            obj.save()
        except Exception:
            if body['bot']:
                del body['usuario']
            else:
                del body['decision_id']
            user = User.objects.get(username=usuario)
            now = datetime.datetime.now()
            user_and_date = {'decisor_id': user.id, 'notice_date': now}
            body.update(user_and_date)
            del body['bot']
            obj = Decision(**body)
            obj.save()
            if not settings.DEBUG:
                msg = usuario + " decidió:\n\n" + body['decision_details'] + "\n\n" + "Para mas informacion visita http://sisarqdec.corp.cablevision.com.ar/index?decision_id=" + str(obj.id)
                subject = "Nueva decisión registrada"
                email_sender = EmailSender(msg, subject, "sisarq", "sisarq")
                email_sender.send()
        return JsonResponse({"error": False}, safe=False)


def writeComment(request):
    try:
        username = request.session['username']
    except Exception:
        return JsonResponse({'username': False}, safe=False)
    body = json.loads(request.body.decode('utf-8'))
    Comment.objects.create(affected_decision_id=body['decision_id'], comment_date=body['date'],
                           commenter=username, comment=body['comment'],
                           reply_to=body['reply_to'])
    return JsonResponse({'username': username}, safe=False)


def getComments(request):
    decision_id = request.GET.get('decision_id')
    final_comments = ''
    comments = Comment.objects.filter(affected_decision_id=decision_id,reply_to__isnull=True)
    for comment in comments:
        there_is_replys = False
        final_comments += comment.commenter+' - '+str(comment.comment_date)+'<br><b>'+comment.comment+'</b><br>'
        final_comments += "<div class='well well-sm'><p id='well" + str(comment.id) + "'>"
        replys = Comment.objects.filter(affected_decision_id=decision_id, reply_to=comment.id)
        for reply in replys:
            if there_is_replys:
                final_comments += '<br>'
            there_is_replys = True
            final_comments += reply.commenter+' - '+str(reply.comment_date)+'<br>'+reply.comment+'<br>'
        if not there_is_replys:
            final_comments += 'No hay respuestas a este comentario'
        final_comments += "</p></div>"
        if authenticated(request):
            final_comments += "<button id='addCommentButton"+str(comment.id)+"' type='button' style='margin-top: -20px;' onclick='toggleSendReply("+str(comment.id)+")' title='Agregar respuesta' class='btn btn-default'><span class='glyphicon glyphicon-plus' aria-hidden='true'></span></button><br><label id='spaceToAddComment"+str(comment.id)+"'></label><br>"
    if final_comments == '':
        final_comments = 'No se han realizado comentarios para esta decision'
    return JsonResponse({'comments': final_comments}, safe=False)


def getFullDecision(request):
    try:
        decision = Decision.objects.get(id=request.GET['decision_id'])
    except Decision.DoesNotExist:
        return JsonResponse({'error': True, 'mensaje': 'El ID no pertenece a una decisión existente'}, safe=False)
    dict_decision = {}
    text_decision = ''
    array_db_header = ['id', 'affected_project_id', 'decisor', 'domain', 'notice_date', 'effective_date', 'decision_details', 'basis', 'scope', 'impact', 'alternatives', 'related_decision_id', 'decision_state']
    array_show_header = ['ID', 'Proyecto', 'Decisor', 'Dominio', 'Fecha de notificación', 'Fecha de aplicación efectiva', 'Definición', 'Racionales', 'Alcance', 'Impacto', 'Alternativas', 'ID de decisión relacionada', 'Estado de la decisión']
    for attr, value in decision.__dict__.items():
        dict_decision[attr] = str(value)
    dict_decision['domain'] = decision.get_domain_display()
    dict_decision['affected_project_id'] = decision.affected_project.name
    dict_decision['decisor'] = decision.decisor.username
    if dict_decision['effective_date'] == 'None':
        dict_decision['effective_date'] = ''
    if dict_decision['related_decision_id'] == 'None':
        dict_decision['related_decision_id'] = ''
    for i in range(len(array_db_header)):
        if array_show_header[i] in ['Definición', 'Racionales', 'Alcance', 'Impacto', 'Alternativas']:
            text_decision += '<b>'+array_show_header[i]+'</b><br>'+dict_decision[array_db_header[i]]+'<br>'
        else:
            text_decision += '<b>'+array_show_header[i]+':</b> '+dict_decision[array_db_header[i]]+'<br>'
    return JsonResponse({'decision': text_decision, 'error': False}, safe=False)


def projects(request):
    response_json = {}
    projects = Project.objects.all()
    for project in projects:
        response_json[project.name] = project.id
    return JsonResponse(response_json, safe=False)


def users(request):
    response_json = {}
    users = User.objects.all()
    for user in users:
        response_json[user.username] = user.id
    return JsonResponse(response_json, safe=False)

