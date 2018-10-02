import App, {Container} from 'next/app';
import React from 'react';
import withApolloClient from '../lib/withApolloClient';
import {ApolloProvider} from 'react-apollo';
import '../scss/app.scss';
import Head from 'next/head'

class MyApp extends App {
	render() {
		const {Component, pageProps, apolloClient} = this.props;
		return <Container>
			<Head>
				<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,700,800" rel="stylesheet" />
			</Head>
			<ApolloProvider client={apolloClient}>
				<Component {...pageProps} />
			</ApolloProvider>
		</Container>;
	}
}

export default withApolloClient(MyApp);
