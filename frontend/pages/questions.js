import App from '../components/App';
import {Query} from 'react-apollo';
import gql from 'graphql-tag';
import React, {Component} from 'react';
import Question from '../components/Question';

const QUESTIONS_QUERY = gql`
query {
  questions {
    id,
    summary,
    user {
      id,
      firstName,
      lastName
    }
  }
}
`;

class QuestionOverview extends Component {
	render() {
		return (
			<App>
				<h1>Overzicht van de vragen</h1>
				<Query query={QUESTIONS_QUERY}>
					{({loading, error, data}) => {
						if (loading) {
							return <div>Fetching</div>;
						}
						if (error) {
							return <div>Error</div>;
						}

						return (
							<div>
								{data.questions.map(
									link => <Question key={link.id} id={link.id} summary={link.summary}
													  fullText={link.fullText} user={link.user}/>
								)}
							</div>
						);
					}}
				</Query>
			</App>
		);
	}
}

export default QuestionOverview;
