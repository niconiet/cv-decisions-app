var currentURL = window.location.href,
    d = new Date(),
    today = d.getFullYear() + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2),
    decisionIdForComment,
    homePage = '/index',
    decisionPage = '/decision';

function showConfirmModal(){
    $("#confirmModal").modal("show");
}

function showCancelSubmitModal(){
    $("#cancelSubmitModal").modal("show");
}

function showSubmitOkModal(){
    $("#confirmModal").modal("hide");
    $("#submitOkModal").modal("show");
}

function showSubmitCanceledModal(){
    $("#confirmModal").modal("hide");
    $("#submitCanceledModal").modal("show");
}

function showEmptyFieldModal(field){
    document.getElementById('emptyFieldMessage').innerHTML = 'Error: el campo <b>'+field+'</b> es requerido';
    $("#emptyFieldModal").modal("show");
}

$( function() {
    $("#datepickerNotificacion").datepicker({dateFormat: "yy-mm-dd"});
    $("#datepickerNotificacion").datepicker('disable',true);
    $("#datepickerNotificacion").datepicker('setDate', today);
    $("#datepickerAplicacionEfectiva").datepicker({dateFormat: "yy-mm-dd", minDate: 0});
} );


function checkEmptyFields(){
    required = ['-','PROYECTO','FECHA DE NOTIFICACIÓN','-','DEFINICIÓN']
    for(var i=0;i<5;i++){
        if(i==3)
            continue;
        if($('.decision')[i].value == ''){
            showEmptyFieldModal(required[i]);
            return true;
        }
    }
    return false;
}

function newLine2br(value){
    return value.replace(/\n/g,"<br>");
}

function postDecision(){
    $('#submitButton').prop('disabled', true);
    var body_decision = {'affected_project_id':$('.decision')[1].value,
               'effective_date':$('.decision')[3].value, 'decision_details':$('.decision')[4].value,
               'basis':$('.decision')[5].value, 'scope':$('.decision')[6].value,
               'impact':$('.decision')[7].value, 'alternatives':$('.decision')[8].value,
               'domain':$('.decision')[9].value, 'decision_state':$('.decision')[10].value,
               'decision_id':localStorage.getItem('decision_for_edit'),'bot':false,
               'related_decision_id':$('#select-related').multipleSelect('getSelects').join()};
    $.ajax({
        type: 'POST',
        contentType: 'application/json; charset=UTF-8',
        url: '/decision',
        data: JSON.stringify(body_decision),
        async: false,
        dataType: 'json',
        success: function(json){
            if(json['error']){
                alert('No ha iniciado sesión o la misma ha expirado');
                window.location.replace('/login');
            }else{
                showSubmitOkModal();
            }
        }
    });
    window.location.replace(homePage);
    localStorage.setItem('decision_for_edit',-1);
}

function submitDecision(){
    if(checkEmptyFields()){
        return;
    }
    showConfirmModal();
}

function saveComment(comment){
    var confirmation = confirm('Su comentario será guardado, está seguro?');
    if (!confirmation) return;
    $.ajax({
        type: 'POST',
        contentType: 'application/json; charset=UTF-8',
        url: '/writeComment/',
        data: JSON.stringify({'decision_id':decisionIdForComment,'date':today,'comment':comment.replace(/\n/g,"<br>"),'reply_to':null}),
        async: false,
        dataType: 'json',
        success: function(reply){
            showSubmitOkModal();
            $('#decisionComment').val('');
            username = reply['username'];
            if(!username){
                alert('No ha iniciado sesión o la misma ha expirado');
                window.location.replace('/login');
            }
        }
    });
}

function showComments(decision_id){
    decisionIdForComment = decision_id;
    $.ajax({
    	type:"GET",
    	url: "/getComments/?decision_id="+decision_id,
    	async: false,
    	dataType : 'json',
        success: function(json){
            document.getElementById("commentsDecisions").innerHTML  = json['comments'];
        }
    });
}

function toggleSendReply(commentId){
    var idLabel = 'spaceToAddComment'+commentId;
    $('#addCommentButton'+commentId).hide();
    document.getElementById(idLabel).innerHTML = "<textarea id='cuadroComentario"+commentId+"' cols='50' rows='3'></textarea><br><button onclick='sendReply("+commentId+")' type='button'>Enviar</button><button type='button' onclick='cancelReply("+commentId+")'>Cancelar</button>"
}

function sendReply(comment_id){
    var confirmation = confirm('Su comentario será guardado, está seguro?');
    if (!confirmation) return;
    var username= '',
        replys = document.getElementById('well'+comment_id).innerHTML,
        new_comment = $('#cuadroComentario'+comment_id).val();
    new_comment = new_comment.replace(/\n/g,"<br>");
    $.ajax({
        type: 'POST',
        contentType: 'application/json; charset=UTF-8',
        url: '/writeComment/',
        data: JSON.stringify({'decision_id':decisionIdForComment,'date':today,'comment':new_comment,'reply_to':comment_id}),
        async: false,
        dataType: 'json',
        success: function(reply){
            username = reply['username'];
            if(!username){
                alert('No ha iniciado sesión o la misma ha expirado');
                window.location.replace('/login');
            }
        }
    });
    new_comment = '<br>'+username+' - '+today+'<br>'+new_comment;
    if(replys == 'No hay respuestas a este comentario'){
        document.getElementById('well'+comment_id).innerHTML = new_comment;
    }else{
        document.getElementById('well'+comment_id).innerHTML = replys+new_comment;
    }
    cancelReply(comment_id);
}

function cancelReply(comment_id){
    $('#addCommentButton'+comment_id).show();
    var id_label = 'spaceToAddComment'+comment_id;
    document.getElementById(id_label).innerHTML = '';
}

function edit_decision(decision_id){
    localStorage.setItem('decision_for_edit',decision_id);
    window.location.replace(decisionPage+'?decision_id='+decision_id);
}

function showFullDecision(decision_id){
    $.ajax({
    	type:"GET",
    	url: "/getFullDecision/?decision_id="+decision_id,
    	async: false,
    	dataType : 'json',
        success: function(json){
            document.getElementById("pfulldetail").innerHTML = (json['error']) ? json['mensaje'] : json['decision'];
        }
    });
}