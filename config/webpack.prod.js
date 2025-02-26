const merge = require('webpack-merge');
var webpack = require("webpack");
const config = require('./webpack.base');
var {PATHS, PROJECT_NAME} = require('./paths');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require('terser-webpack-plugin');
const autoprefixer = require('autoprefixer');

module.exports = merge(config, {
  mode: 'production',
  module: {
    rules: [{
      test: /\.scss$/,
      use:  [
        'style-loader',
        MiniCssExtractPlugin.loader,
        'css-loader',
        {
          loader: 'postcss-loader',
          options: {
            postcssOptions: {
              plugins: [
                autoprefixer()
              ]
            }
          }
        },
        'sass-loader'
      ],
      include: PATHS.sass
      }],
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          parse: {
            ecma: 8,
          },
          compress: {
            ecma: 5,
            warnings: false,
            comparisons: false,
            inline: 2,
          },
          output: {
            ecma: 5,
            comments: false,
            ascii_only: true,
          },
        },
        parallel: true,
      }),
    ],
  }
});
