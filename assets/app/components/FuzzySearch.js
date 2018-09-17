import React from 'react';

import {API_LIMIT_MESSAGE} from './Messages';


export default class FuzzySearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            query: null,
            result: null,
            message: null,
        };
    }
    
    handleTextChange = (event) => {
        this.setState({query:event.target.value, result: null});
    }
    
    handleSubmit = (event) => {
        event.preventDefault();

        fetch('/api/fuzzy-search/country/?query='+this.state.query, {
            credentials: 'same-origin',
            method: 'GET',
        })
        .then(response => {
            if (response.status === 429) {
                const data = {summary: null, message: API_LIMIT_MESSAGE};
                return data;
            }
            else if (response.status === 400) {
                response.json().then(data => {
                    const key = Object.keys(data)[0];
                    this.setState({summary: null, message: data[key]});
                });
                return {};
            }
            return response.json();
        })
        .then(data => {this.setState({result: data})});
    }

    render() {
        return (
            <div className="row">
                <div className="col-md-6">
                    <h3> Country </h3>
                    <form>
                        <div className="form-group">
                            <input
                                className="form-control"
                                onChange={this.handleTextChange}
                                value={this.state.query}
                            />
                            <br/>
                        </div>
                        <div className="form-group">
                            <button
                                className="btn btn-success form-control"
                                type="submit"
                                onClick={this.handleSubmit}
                            > Search Matching Countries
                            </button>
                        </div>
                    </form>
                </div>
                {
                    this.state.message ? (
                        <div>
                            <div className="col-md-6">
                                <h4 className="text-danger text-center">
                                    {this.state.message} 
                                </h4>
                            </div>
                        </div>
                    ) : ( 
                        <div className="col-md-6">
                            {this.state.summary?(<h3> Summary </h3>): ''}
                            <div className="text-justified">
                                {
                                    this.state.result ? (
                                        <div>
                                            <h3>Country matches for '{this.state.query}'</h3>
                                            <ul>
                                                {
                                                    this.state.result.matches.map((x) => (
                                                        <li>
                                                            <b>{x.label}</b> -> {parseInt(x.similarity*10000)/100}%
                                                        </li>
                                                    ))
                                                }
                                            </ul>
                                        </div>
                                    ) : ''
                                }
                            </div>
                        </div>
                    )
                }               
            </div>
        );
    }
}
