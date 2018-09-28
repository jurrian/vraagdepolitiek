import Link from 'next/link'

export default () =>
    <div>
        Click{' '}
        {/*<Link as={`/q/${props.id}`} href="/questions?id=${props.id}">*/}
            {/*<a>Questions</a>*/}
        {/*</Link>{' '}*/}
        <Link as={`/q/1`} href="/questions?id=1">
            <a>Questions</a>
        </Link>{' '}
        to read more
    </div>
