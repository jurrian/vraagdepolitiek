import React, {Component} from 'react';
import Link from "next/link";
import Moment from 'react-moment';

class QuestionListItem extends Component {
	render() {
		const themes = this.props.themes && this.props.themes.map((theme) => {
			return (
				<a className="theme" key={theme.id} href="">{theme.name}</a>
			)
		})
		return (
			<div className="question__list">
				<Link as={`/q/${this.props.id}/upvote/`} href={`/question/upvote?id=${this.props.id}`}>
					<a className="upvote">&#9650;<br/>{this.props.totalSupportCount}</a>
				</Link>
				<article>
					{themes}
					<Link as={`/q/${this.props.id}/`} href={`/question/detail?id=${this.props.id}`}>
						<a className="summary">{this.props.summary}</a>
					</Link>
				</article>
				<div className="user">
					{this.props.user ? (
						<Link as={`/u/${this.props.user.id}/`} href={`/user/detail?id=${this.props.user.id}`}>
							<a>{this.props.user.firstName} {this.props.user.lastName}</a>
						</Link>
					) : (
						<span>Gebruiker verwijderd</span>
					)}
				</div>
				<p>
					<Moment fromNow withTitle>
						{this.props.publicationDatetime}
					</Moment>
				</p>
			</div>
		);
	}
}

export default QuestionListItem;
