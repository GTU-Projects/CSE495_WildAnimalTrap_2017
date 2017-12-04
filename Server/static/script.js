//'use strict';

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
});

trapApp.controller('aboutController', function($scope) {
    $scope.message = 'About Hasan Men ...';
});

trapApp.controller('trapsController', function($scope) {
    $scope.message = 'Trap1 trap2 ...';
});

trapApp.controller('trapDetailController', function($scope) {
    $scope.location = 'GTU';
    $scope.status = 'Offline';
});


