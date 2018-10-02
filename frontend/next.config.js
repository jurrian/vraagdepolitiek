// Const withESLint = require('next-eslint')
const withSass = require('@zeit/next-sass');
const withSourceMaps = require('@zeit/next-source-maps');

module.exports = {
	exportPathMap: function () {
		return {
			'/': {page: '/'}
		};
	}
};

module.exports = withSourceMaps(
	{
		webpack(config, options) {
			return config;
		}
	}
);

module.exports = withSass();

// Module.exports = withESLint()
