import { Query } from 'react-apollo'
import gql from 'graphql-tag'
import React, { Component } from 'react'
import Link from './Link'

const FEED_QUERY = gql`
query {
  sites(id: 1) {
    id,
    domain,
    organizationSet {
      name,
      questionSet {
        summary
      }
    }
  }
}
`

class LinkList extends Component {
    render() {
        return (
            <Query query={FEED_QUERY}>
                {({ loading, error, data }) => {
                    if (loading) return <div>Fetching</div>
                    if (error) return <div>Error</div>

                    const linksToRender = data.sites

                    return (
                        <div>
                            {linksToRender.map(link => <Link key={link.id} link={link.domain} />)}
                        </div>
                    )
                }}
            </Query>
        )
    }
}

export default LinkList
