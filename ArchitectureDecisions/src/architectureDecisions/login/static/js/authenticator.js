var homePage = "/index";


function login(){
	authenticate(document.getElementById('username').value, document.getElementById('password').value);
}

function authenticate(requestUser,requestPassword){
	$.ajax({
	    url: "/authenticate",
	    headers: {
			'Content-Type':'application/json'
		},
	    method: 'POST',
	    contentType: "application/json; charset=UTF-8",
		data: JSON.stringify({user: requestUser, password:requestPassword}),
	    dataType: "json",
	    success: function(json){
			if(json["authenticated"] == false){
				showAuthenticationError();
			}
			else{
		        window.location.replace(window.location.protocol + "//" + window.location.hostname + ':' + window.location.port + homePage);
			}
		    },
	  });
}

function logAsAnonimo(){
	window.location.replace(window.location.protocol + "//" + window.location.hostname + ':' + window.location.port + homePage);
}

function showModal(){
	//Show modal
	$('#login-modal').modal({  //prevents modal from hiding onclick, on key press
         backdrop: 'static',
        keyboard: false
    });
	$('#login-modal').modal('show');
}

function hideModal(){
	//Hide modal
	$('#login-modal').modal('hide');
}

function showAuthenticationError(){
    $("#AuthenticationErrorAlert").show();
}