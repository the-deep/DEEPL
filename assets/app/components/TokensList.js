import React from 'react';


export class TokensList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            test_token: '', 
            api_token: ''
        };
    }

    componentWillMount() {
        const test_token = localStorage.getItem('test_token') || 'Please Login.';
        const api_token = localStorage.getItem('api_token') || 'Please Login.';
        this.setState({test_token, api_token});
    }

    render() {
        return (
            <div className="row">
                <div className="col-md-6">
                    <h3>My tokens</h3>
                    <label> Test Token : </label> {this.state.test_token} <br/> <br/>
                    <label> Api Token : </label> {this.state.api_token} <br/> <br/>
                </div>
                <div className="col-md-6">
                    <h3> About tokens </h3>
                    <p>
                        <b>Test Token: </b> You can use this token for testing the apis and sample success/failure responses.
                    </p>
                    <p>
                        <b> API Token: </b> Use this token for actual usage of the NLP algorithms and functionalities.
                    </p>
                    <p>
                        Use the token in API Request header as,<br/> <code>Authorization: Token [your token] </code>
                    </p>
                    <p>
                        <b>NOTE: You will have limited number of api calls allowed for a token.</b>
                    </p>
                </div>
            </div>
        );
    }
}

export default TokensList;
