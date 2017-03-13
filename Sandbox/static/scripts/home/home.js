angular.module('app.home', ['ngRoute'])

.config(function($routeProvider) {
   $routeProvider
   .when('/', {
      templateUrl: 'static/scripts/home/home.html',
      controller : 'HomeCtrl',
   });
})

.controller('HomeCtrl', function($scope, $http){
    var self = this;
    $scope.welcome_message = "Fingerprint sandbox";
    $scope.training_paragraph = "This is our training paragraph. It has UPPERCASE and lowercase \
                                characters to better learn your typing pattern. It also has all the \
                                letters in the alphabet like in the sentence: The quick brown fox jumps \
                                over the lazy dog";
    $scope.keystrokes_analyzer = new Fingerprint(10000);

    $scope.send_typing_data = function(){
        $http.post(
            '/fingerprint',
            $scope.keystrokes_analyzer.data
        );
    };
});