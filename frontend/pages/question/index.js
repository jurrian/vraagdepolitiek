import App from '../../components/App';
import {Query} from 'react-apollo';
import gql from 'graphql-tag';
import React, {Component} from 'react';
import QuestionListItem from '../../components/QuestionListItem';

const QUESTIONS_QUERY = gql`
query {
  questions {
    id,
    summary,
    themes {
      name
    },
    publicationDatetime,
    totalSupportCount,
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
									link => <QuestionListItem key={link.id} id={link.id} summary={link.summary}
													  themes={link.themes} user={link.user} totalSupportCount={link.totalSupportCount}
									publicationDatetime={link.publicationDatetime}/>
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
