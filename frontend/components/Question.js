import React, {Component} from 'react';
import Link from "next/link";
import Answer from './Answer';

class Question extends Component {
	render() {
		const themes = this.props.themes.map((theme) => {
			return (
				<a className="theme" href="">{theme.name}</a>
			)
		})
		const answers = this.props.answers.map((answer) => {
			return (
				<Answer key={answer.id} id={answer.id} summary={answer.summary} fullText={answer.fullText}
						user={answer.user} />
			)
		})
		return (
			<div className="question">
				<article>
					<Link as={`/q/${this.props.id}/`} href={`/questions?id=${this.props.key}`}>
						<a><h1>{this.props.summary}</h1></a>
					</Link>
					{themes}
					<p>{this.props.fullText}</p>
					<hr />
					{answers}
				</article>
				<div className="user">
					{this.props.user ? (
						<span>{this.props.user.firstName} {this.props.user.lastName}</span>
					) : (
						<span>Gebruiker verwijderd</span>
					)}
				</div>
			</div>
		);
	}
}

export default Question;
