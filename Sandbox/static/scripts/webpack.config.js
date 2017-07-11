var path = require('path')

module.exports = {
    entry: './src/main.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    },

    devtool: "source-map",

    resolve: {
        // Add '.ts' and '.tsx' as resolvable extensions.
        extensions: [".webpack.js", ".web.js", ".ts", ".tsx", ".js"]
    },

    module: {
        rules: [
            {
                // All output '.js' files will have any sourcemaps re-processed by 'source-map-loader'.
                enforce: 'pre',
                test: /\.js$/, 
                loader: "source-map-loader"
            }
        ]
    }
};
