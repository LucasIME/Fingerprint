angular.module('app.home', ['ngRoute'])

.controller('HomeCtrl', function($scope, $http){
    var self = this;
    $scope.welcome_message = "Fingerprint sandbox";
});