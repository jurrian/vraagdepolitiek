import React, {Component} from 'react';
import Link from "next/link";

class Answer extends Component {
	render() {
		return (
			<div className="question">
				<article>
					<p>{this.props.summary}</p>
					<p>{this.props.fullText}</p>
				</article>
				<div className="user">
					{this.props.user ? (
						<p>
							<span>{this.props.user.firstName} {this.props.user.lastName}</span>
							<img src={this.props.user.picture} width="100" height="100" />
						</p>
					) : (
						<span>Gebruiker verwijderd</span>
					)}
				</div>
			</div>
		);
	}
}

export default Answer;
