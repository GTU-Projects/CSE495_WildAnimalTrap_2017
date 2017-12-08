function assembleStatus(status){
    if(status==0){
        return true;
    }else if(status==1){
        return "Empty E-Mail or Password";
    }else if(status==2){
        return "Invalid E-Mail or Password";
    }
}


$( document ).ready(function() {
    $("#signup-area").hide();

    $("#btnToggleSign").click(function(){
        $("#signup-area").fadeToggle();
        $("#login-area").fadeToggle();
    });
    
    $("#btnSignIn").click(function(){
        
        sendData = {"email":"hmen.56@gmail.com", "password":"Hasan5669"}
        $.ajax({
            url: "login",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    $(location).attr('href','./');
                }else{
                    $("#msg-area").removeClass("alert-primary").addClass("alert-danger");
                    $("#msg-area").text(retVal);
                }
            }
        });

    });
    
    
    $("#btnSignUp").click(function(){
        alert("Signup");
    });

});



