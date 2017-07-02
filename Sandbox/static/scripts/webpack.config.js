var path = require('path')

module.exports = {
    entry: './main.js',
    //{
    //     main: './main.js',
    //     register: './register/register.js',
    //     auth: './auth/auth.js',
    //     home: './home/home.js',
    //     navbar: './navbar/navbar.js',
    //     fingerprint: './fingerprint.js',
    // },
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    }
};
