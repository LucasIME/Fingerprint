/**
 * Created by lucasime on 17/02/17.
 */
function navBarController($scope) {
    $scope.headerList = [
        {
            text: "Home",
            url: "#!/"
        },
        {
            text: "Register",
            url: "#!/register"
        },
        {
            text: "Authenticate",
            url: "#!/auth"
        }
    ];
}

angular.module('app.navbar', [])

.component('navbar', {
templateUrl: 'static/scripts/navbar/navbar.html',
controller: navBarController
});