//'use strict';
function assembleStatus(status){
    if(status==0){
        return true;
    }else if(status==-1){
        return "Unknown Server Error!";
    }else if(status==1){
        return "Empty E-Mail or Password!";
    }else if(status==2){
        return "Invalid E-Mail or Password!";
    }else if(status==3){
        return "E-Mail Already Used!";
    }else if(status==4){
        return "Trap Already Initialized!";
    }else if(status==5){
        return "Invalid Serial Number!";
    }else if(status==6){
        return "Trap Connection Error!";
    }
}

var trapApp = angular.module('trapApp', ['ngRoute']);

// configure our routes
trapApp.config(function($routeProvider) {
    $routeProvider
        // route for the home page
        .when('/', {
            templateUrl : '/static/partials/traps.html',
            controller  : 'trapsController'
        })

        // route for the about page
        .when('/about', {
            templateUrl : '/static/partials/about.html',
            controller  : 'aboutController'
        })

        // route for the traps page
        .when('/traps', {
            templateUrl : '/static/partials/traps.html',
            controller  : 'trapsController'
        })

        // route for the traps page
        .when('/trap-detail', {
            templateUrl : '/static/partials/trap-detail.html',
            controller  : 'trapDetailController'
        })

        .when('/photos', {
            templateUrl : '/static/partials/photos.html',
            controller  : 'photosController'
        })

});

trapApp.controller('aboutController', function($scope) {
    $scope.message = 'About Hasan Men ...';
});

trapApp.controller('trapsController', function($scope,$http) {

    // get traps from backend-db
    $http.post('/getTraps').then(function(response){
        $scope.traps =response.data;
    });

    $scope.showTrapDetail = function(serial){
        document.cookie=serial;
        $(location).attr('href',"/#!/trap-detail");
    };

    $scope.addNewTrap = function(){
        newTrapSerial = $("#newTrapSerial").val()
        newTrapName = $("#newTrapName").val()
        newTrapLocation = $("#newTrapLocation").val()

        if(newTrapSerial=="" || newTrapName=="" || newTrapLocation==""){
            $("#addNewTrapMessage").text("Please fill all blanks.");
            return;
        }

        sendData = {
            "serial":newTrapSerial,
            "name":newTrapName,
            "location":newTrapLocation
        };

        $.ajax({
            url: "addNewTrap",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    $("#addNewTrapMessage").text("Trap successfully was added.");
                    // update trap list
                    $http.post('/getTraps').then(function(response){
                        $scope.traps =response.data;
                        $scope.$apply(); // update angular
                    });
                }else{
                    $("#addNewTrapMessage").text(retVal);
                }
            }
        });

    }
});

trapApp.controller('trapDetailController', function($scope) {

    currTrapSerial = document.cookie

    loadTrapDetails($scope,currTrapSerial);

    // TODO: change activeTrapSerial variable
    $scope.setDoor = function(nextState){

        sendData = {"serial":currTrapSerial, "nextState":nextState}
        
        $.ajax({
            url: "takePhoto",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    if(data["nextState"]==1){
                        alert("Door Closed.");
                    }else if(data["nextState"]==0){
                        alert("Door Opened.");
                    }else{
                        alert("Unknown door next state!");
                    }
                }else{
                    alert("Door State Changing Error!");
                }
            }
        });
    };

    $scope.setTrapDetail = function(){
        
        newTrapName = $("#newTrapName").val()
        newTrapLocation = $("#newTrapLocation").val()

        if(newTrapName=="" || newTrapLocation==""){
            $("#editTrapMessage").text("Please fill all blanks!");
            return;
        }

        sendData = {
            "serial":currTrapSerial,
            "name":newTrapName,
            "location":newTrapLocation
        };

        $.ajax({
            url: "setTrapDetail",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    $("#editTrapMessage").text("Details were chaned."); 
                    $scope.name = newTrapName;
                    $scope.location = newTrapLocation;
                    $scope.$apply();
                }else{
                    $("#editTrapMessage").text("Error:"+retVal); 
                }
            }
        });
    };// end of set trap detail function

    $scope.takePhoto = function(){

        sendData = {"serial":currTrapSerial}

        $.ajax({
            url: "takePhoto",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    updateLastPhoto($scope,currTrapSerial);
                }else{
                    alert("Error:"+retVal);
                }
            }// end of takephoto success func
        });
    };// end of take photo function

    //loadLastPhoto($scope,currTrapSerial);
});

function loadLastPhoto($scope,serial){

    sendData = {"serial":serial};

    // now, get last saved photo name
    $.ajax({
        url: "getLastPhotoName",
        type: "POST",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        // data has status variable
        success: function(data,status){
            retVal = assembleStatus(data["status"]);
            if(retVal==true){
                name = data["name"];
                item = {src:"/static/.trapData/"+serial+"/"+name,desc:name};

                $scope.lastPhotoSrc = item["src"];
                $scope.lastPhotoDesc = item["desc"];

                $scope.$apply(); // update angular
            }else{
                alert(retVal);
            }
        }// end of getlastphotoname succes func
    });
}

function loadTrapDetails($scope,serial){

    sendData = {"serial":serial};

    $.ajax({
        url: "getTrapDetails",
        type: "POST",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        // data has status variable
        success: function(data,status){
            retVal = assembleStatus(data["status"]);
            if(retVal==true){
                $scope.serial = serial;
                $scope.name = data["name"];
                $scope.location = data["location"];
                $scope.ap = data["ap"];
                $scope.$apply();
            }else{
                alert("Server Error!");
            }
        }// end of getlastphotoname succes func
    });
}

trapApp.controller('photosController', function($scope) {

    serial = document.cookie
    sendData = {"serial":serial};

    $scope.photos = [];

    $.ajax({
        url: "getPhotoPaths",
        type: "POST",
        data: JSON.stringify(sendData),
        contentType: "application/json",
        // data has status variable
        success: function(data,status){
            for(i=0;i<data["paths"].length;i++){
                photoPath = "/static/.trapData/"+serial+"/"+data["paths"][i];
                //alert(photoPath);
                item = {src:photoPath,desc:data["paths"][i]};
                $scope.photos.push(item);
                //alert($scope.photos[i]["src"]);
            }
            $scope.$apply();
        }
    });

    $scope.photoIndex = 0;

    $scope.isActive = function (index) {
        return $scope.photoIndex === index;
    };
    // show prev image
    $scope.showPrev = function () {
        $scope.photoIndex = ($scope.photoIndex > 0) ? --$scope.photoIndex : $scope.photos.length - 1;
    };
    // show next image
    $scope.showNext = function () {
        $scope.photoIndex = ($scope.photoIndex < $scope.photos.length - 1) ? ++$scope.photoIndex : 0;
    };
    // show a certain image
    $scope.showPhoto = function (index) {
        $scope.photoIndex = index;
    };
});