import Link from 'next/link';

export default () =>
	<div className="wrapper">
		<div>
            Click{' '}
			{/* <Question as={`/q/${props.id}`} href="/questions?id=${props.id}"> */}
			{/* <a>Questions</a> */}
			{/* </Question>{' '} */}
			<Link href="/q/">
				<a>Questions</a>
			</Link>{' '}
            to read more
		</div>
	</div>;

