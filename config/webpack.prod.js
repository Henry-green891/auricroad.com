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
            plugins: () => [
              autoprefixer()
            ]
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
        cache: true,
        parallel: true,
        sourceMap: true,
        terserOptions: {
          compress: {
            warnings: false,
            comparisons: false,
            inline: 2
          },
          output: {
            comments: false,
            ascii_only: true
          }
        }
      })
    ]
  }
});
