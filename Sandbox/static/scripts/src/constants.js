'use strict'

var angular = require('angular')

angular
    .module('app')
    .constant('constants', {
        routes: {
            home: { 
                view: 'static/scripts/src/home/home.html'
            },
            register: { 
                view: 'static/scripts/src/register/register.html'
            },
            auth: { 
                view: 'static/scripts/src/auth/auth.html'
            },
            navbar: { 
                view: 'static/scripts/src/navbar/navbar.html'
            },
        }
    });

