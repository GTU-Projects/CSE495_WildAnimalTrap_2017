


$( document ).ready(function() {
    $("#signup-area").hide();

    $(".btnToggleSign").click(function(){
        $("#signup-area").fadeToggle();
        $("#login-area").fadeToggle();
    });
    
    $("#btnSignIn").click(function(){

        email = $("#loginEmail").val()
        password = $("#loginPassword").val()

        if (email=="" || password==""){
            $("#msgArea").removeClass("alert-success").addClass("alert-danger");
            $("#msgArea").text("Empty E-Mail or Password!");
            return False
        }

        sendData = {"email":email, "password":password}
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
                    $("#msgArea").removeClass("alert-success").addClass("alert-danger");
                    $("#msgArea").text(retVal);
                }
            }
        });

    });
    
    
    $("#btnSignUp").click(function(){
       serial = $("#upSerial").val();
       email = $("#upEmail").val();
       password = $("#upPassword").val();
       password2 = $("#upPassword2").val();


        if(serial=="" || email=="" || password=="" || password2==""){
            $("#msgArea").addClass("alert-danger").text("Please Fill All Blanks!");
            return false
        }

        if(password!=password2){
            $("#msgArea").addClass("alert-danger").text("Passwords not same!");
            return false
        }


        sendData = {"email":email, 
                    "password":password,
                    "serial":serial}
        $.ajax({
            url: "signup",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    $("#msgArea").removeClass("alert-danger").addClass("alert-success");
                    $("#msgArea").text("Account created. Now you can login");
                }else{
                    $("#msgArea").removeClass("alert-success").addClass("alert-danger");
                    $("#msgArea").text(retVal);
                }
            }
        });
    });

});



