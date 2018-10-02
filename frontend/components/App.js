import React from 'react';
import Link from 'next/link';

export default ({children}) => (
	<>
		<header>
			<nav className="wrapper">
				<Link href="/">
					<a>Home</a>
				</Link>
				<Link href="/question">
					<a>Vragen</a>
				</Link>
			</nav>
		</header>
		<main>
			<div className="wrapper main-content">
				{children}
			</div>
		</main>
	</>
);
