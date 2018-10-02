import Link from 'next/link';
import App from '../components/App';

export default () =>
	<App>
		Klik{' '}
		<Link href="/q/">
			<a>hier</a>
		</Link>{' '}
		voor alle vragen.
	</App>
