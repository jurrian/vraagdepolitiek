import React, {Component} from 'react';
import {Query, Mutation} from 'react-apollo';
import gql from 'graphql-tag';
import App from '../../components/App';

const THEMES_QUERY = gql`
query {
  themes {
  	id,
    name
  }
}
`;

const CREATE_QUESTION_MUTATION = gql`
mutation CreateQuestion($input: CreateUserInput!){
	createQuestion(input: $input){
		errors {
			field,
			messages
		}
	}
}
`;

class QuestionForm extends Component {
	constructor(props) {
		super(props);
		this.state = {
			value: 'Please write an essay about your favorite DOM element.'
		};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		this.setState({value: event.target.value});
	}

	handleSubmit(event) {
		alert('An essay was submitted: ' + this.state.value);
		event.preventDefault();
	}

	render() {
		return (
			<App>
				<Mutation mutation={CREATE_QUESTION_MUTATION}>
					{(createQuestion, {data}) => (
						<form onSubmit={this.handleSubmit}>
							<p>
								<label>
							Summary:
									<textarea name="summary" onChange={this.handleChange} />
								</label>
							</p>
							<p>
								<label>
							Full text:
									<textarea name="fullText" onChange={this.handleChange} />
								</label>
							</p>
							<p>
								<label>
							Theme's:
									<Query query={THEMES_QUERY}>
										{({loading, error, data}) => {
											if (loading) {
												return <div>Thema's laden...</div>;
											}
											if (error) {
												return <div>Thema's kunnen niet geladen worden.</div>;
											}

											const options = data.themes.map(
												theme => <option value={theme.id}>{theme.name}</option>
											);

											return (
												<select onChange={this.handleChange} multiple={true}>
													{options}
												</select>
											);
										}}
									</Query>
								</label>
							</p>
							<input type="submit" value="Submit" />
						</form>
					)}
				</Mutation>
			</App>
		);
	}
}

export default QuestionForm;
