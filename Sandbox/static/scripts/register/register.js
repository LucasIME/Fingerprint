angular.module('app.register', ['ngRoute'])

.controller('RegisterCtrl', function($scope, $http){
    var self = this;
    $scope.training_paragraph = "This is our training paragraph. It has UPPERCASE and lowercase \
                                characters to better learn your typing pattern. It also has all the \
                                letters in the alphabet like in the sentence: The quick brown fox jumps \
                                over the lazy dog";
    $scope.keystrokes_analyzer = new Fingerprint(10000);
    $scope.email = "";

    $scope.send_typing_data = function(){
        $http.post(
            '/save/' + $scope.email,
            $scope.keystrokes_analyzer.get()
        );
    };
});