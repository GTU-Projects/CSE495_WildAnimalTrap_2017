//'use strict';

var trapApp = angular.module('trapApp', ['ngRoute']);

// configure our routes
trapApp.config(function($routeProvider) {
    $routeProvider
        // route for the home page
        .when('/', {
            templateUrl : '/static/partials/home.html',
            controller  : 'mainController'
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
});


// create the controller and inject Angular's $scope
trapApp.controller('mainController', function($scope) {
    // create a message to display in our view
    $scope.message = 'Home2 Page';
});

trapApp.controller('aboutController', function($scope) {
    $scope.message = 'About Hasan Men ...';
});

trapApp.controller('trapsController', function($scope) {
    $scope.message = 'Trap1 trap2 ...';
});


