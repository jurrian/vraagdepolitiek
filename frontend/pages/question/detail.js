import App from '../../components/App';
import {Query} from 'react-apollo';
import gql from 'graphql-tag';
import React, {Component} from 'react';
import Question from '../../components/Question';
import Answer from "../../components/Answer";

class QuestionDetail extends Component {
	static async getInitialProps({query: {id}}) {
		return {id};
	}

	render() {
		const QUESTION_QUERY = gql`
		query {
		  questions(id: ${this.props.id}) {
			id,
			summary,
			fullText,
			user {
			  id,
			  firstName,
			  lastName,
				email
			},
			themes {
			  name
			},
			requests,
			answers {
			  summary,
			  fullText,
			  user {
			  	id,
			  	firstName,
			  	lastName,
			  	picture
			  }
			},
			publicationDatetime,
			userSupport {
			  email,
			}
			fbSupportCount,
			twitterSupportCount,
			userSupportCount,
			totalSupportCount,
		  }
		}
		`;

		return (
			<App>
				<h2>Vraag</h2>
				<Query query={QUESTION_QUERY}>
					{({loading, error, data}) => {
						if (loading) {
							return <div>Fetching</div>;
						}
						if (error) {
							return <div>Error</div>;
						}

						const question = data.questions[0];

						return (
							<Question key={question.id} id={question.id} summary={question.summary}
									  fullText={question.fullText}
									  user={question.user} themes={question.themes} answers={question.answers}>
								<Answer/>
							</Question>

						);
					}}
				</Query>
			</App>
		);
	}
}

export default QuestionDetail
