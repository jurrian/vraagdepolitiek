import React, {Component} from 'react';
import Link from 'next/link';

class Answer extends Component {
	render() {
		return (
			<article className="answer">
				<div className="content">
					<p>{this.props.summary}</p>
					<p>{this.props.fullText}</p>
				</div>
				<div className="user">
					<img src={this.props.user.picture} width="100" height="100" />
					{this.props.user ? (
						<p>{this.props.user.firstName} {this.props.user.lastName}</p>
					) : (
						<p>Gebruiker verwijderd</p>
					)}
				</div>
			</article>
		);
	}
}

export default Answer;
