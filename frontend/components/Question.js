import React, {Component} from 'react';
import Link from "next/link";
import Answer from './Answer';
import Moment from 'react-moment';

class Question extends Component {
	render() {
		const themes = this.props.themes && this.props.themes.map((theme) => {
			return (
				<a className="theme" key={theme.id} href="">{theme.name}</a>
			)
		})
		const answers = this.props.answers && this.props.answers.map((answer) => {
			return (
				<Answer key={answer.id} id={answer.id} summary={answer.summary} fullText={answer.fullText}
						user={answer.user} />
			)
		})
		return (
			<div className="question">
				<article>
					<section>
						<div className="content">
							<h1>{this.props.summary}</h1>
							{themes}
							<p>Gesteld op{` `}
								<Moment format="DD-MM-YYYY HH:MM">
									{this.props.publicationDatetime}
								</Moment>
							</p>
							<p>{this.props.fullText}</p>
						</div>
						<div className="user">
							<img className="empty" src="" width="120" height="120" />
							{this.props.user ? (
								<p>{this.props.user.firstName} {this.props.user.lastName}</p>
							) : (
								<p>Gebruiker verwijderd</p>
							)}
						</div>
					</section>
					{answers}
				</article>
			</div>
		);
	}
}

export default Question;
