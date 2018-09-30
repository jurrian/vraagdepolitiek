// Const withESLint = require('next-eslint')
const withSass = require('@zeit/next-sass');

module.exports = {
	exportPathMap: function () {
		return {
			'/': {page: '/'}
		};
	}
};

module.exports = withSass();
// Module.exports = withESLint()
