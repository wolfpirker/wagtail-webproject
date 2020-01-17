const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    mode: 'development',
    context: __dirname,
    entry: './siemreap/static/js/index',
    output: {
        path: path.resolve('./siemreap/static/bundles/'),
        filename: 'app.js'
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new VueLoaderPlugin(),
    ],

    module: {
        rules:  [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
           {
			  test: /\.vue$/,
			  loader: 'vue-loader',
			  options: {
				loaders: {
					'scss': 'vue-style-loader!css-loader!sass-loader',
					'sass': 'vue-style-loader!css-loader!sass-loader?indentedSyntax'
				}
			  }
		   },
		         {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      }
        ],
    },
    resolve: {
        alias: {vue: 'vue/dist/vue.js'}
    },

};
