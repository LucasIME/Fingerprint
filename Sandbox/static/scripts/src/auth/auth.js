var angular = require('angular');
var Fingerprint = require('fingerprint-js').Fingerprint;

angular.module('app.auth', ['ngRoute'])

.controller('AuthCtrl', function($scope, $http){
    var self = this;
    $scope.authentication_paragraph = `This is our authentication paragraph. It is a bit different \ 
                                        from our registration paragraph. It still has UPPERCASE and lowercase \
                                        characters, but changes a little bit to make sure we don't overfit. \
                                        Nonetheless it still has all the \
                                        letters in the alphabet just like in the sentence: The quick brown fox jumps \
                                        over the lazy dog`;
    $scope.keystrokes_analyzer = new Fingerprint(10000);
    $scope.email = "";

    $scope.send_typing_data = function(){
        $http.post(
            '/user/' + $scope.email,
            $scope.keystrokes_analyzer.get()
        ).then(function(response){
            console.log(response);
            if(response.data.confidenceLevel === 1)
                alert("User verified successfully");
            else
                alert("Sorry! Your typing pattern did not match that one that is in our database");
        }, function(response){
            alert("There was an error processing your request");
        });
    };
});