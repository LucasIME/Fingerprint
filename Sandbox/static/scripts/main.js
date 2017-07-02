var angular = require('angular');

angular.module('app', [
    'app.navbar',
    'app.home',
    'app.auth',
    'app.register'
])

.config(function($routeProvider) {
   $routeProvider
   .when('/', {
      templateUrl: 'static/scripts/home/home.html',
      controller : 'HomeCtrl',
   })
   .when('/register', {
      templateUrl: 'static/scripts/register/register.html',
      controller : 'RegisterCtrl',
   })
   .when('/auth', {
      templateUrl: 'static/scripts/auth/auth.html',
      controller : 'AuthCtrl',
   });
});

//Requires to allow webpack to bundle whole application
require('./home/home.js');
require('./navbar/navbar.js');
require('./register/register.js');
require('./auth/auth.js');