var angular = require('angular');

angular.module('app', [
    'app.navbar',
    'app.home',
    'app.auth',
    'app.register'
])

.config(routesConfig);

require('./constants.js');

routesConfig.$inject = ['$routeProvider', 'constants'];

function routesConfig($routeProvider, c){
    console.log(c);
   $routeProvider
   .when('/', {
      templateUrl: c.routes.home.view,
      controller : 'HomeCtrl',
   })
   .when('/register', {
      templateUrl: c.routes.register.view,
      controller : 'RegisterCtrl',
   })
   .when('/auth', {
      templateUrl: c.routes.auth.view,
      controller : 'AuthCtrl',
   });
}

//Requires to allow webpack to bundle whole application
require('./home/home.js');
require('./navbar/navbar.js');
require('./register/register.js');
require('./auth/auth.js');

