const express = require('express');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const app = next({dev});
const handle = app.getRequestHandler();

app.prepare()
	.then(() => {
		const server = express();

		server.get('/q/', (req, res) => {
			const actualPage = '/questions';
			app.render(req, res, actualPage);
		});

		server.get('/q/:id([0-9]+)/', (req, res) => {
			const actualPage = '/question/detail';
			const queryParams = {id: req.params.id};
			app.render(req, res, actualPage, queryParams);
		});

		server.get('*', (req, res) => {
			return handle(req, res);
		});

		server.listen(3000, err => {
			if (err) {
				throw err;
			}
			console.log('> Ready on http://localhost:3000');
		});
	})
	.catch(ex => {
		console.error(ex.stack);
		process.exit(1);
	});
