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
});

trapApp.controller('trapDetailController', function($scope) {
    $scope.status = 'Online';
    $scope.name="x";
    // save trap serial in cookie to use in trap special pages 
    $scope.serial = document.cookie;
    $scope.location = "x";

    // TODO: change activeTrapSerial variable
    $scope.setDoor = function(nextState){

        sendData = {"serial":activeTrapSerial, "nextState":nextState}
        
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

    $scope.takePhoto = function(){

        sendData = {"serial":activeTrapSerial}


        $.ajax({
            url: "takePhoto",
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json",
            // data has status variable
            success: function(data,status){
                retVal = assembleStatus(data["status"]);
                if(retVal==true){
                    alert("take photo completed.");
                }else{
                    alert(retVal);
                }
            }
        });
    };
});


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
                item = {src:photoPath,desc:i};
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


