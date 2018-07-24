import React from 'react';

import {API_LIMIT_MESSAGE} from './Messages';


export default class Summarization extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            text: null,
            summary: null,
            message: null,
        };
    }

    handleTextChange = (event) => {
        this.setState({text:event.target.value});
    }
    
    handleSubmit = (event) => {
        event.preventDefault();

        const data = new URLSearchParams();
        data.append("text", this.state.text);

        fetch('/api/summarization/', {
            credentials: 'same-origin',
            method: 'POST',
            body: data
        })
        .then(response => {
            if (response.status === 429) {
                const data = {summary: null, message: API_LIMIT_MESSAGE};
                return data;
            }
            else if (response.status !== 200) {
                const data = {summary: null, message: response.text}
                return data;
            }
            return response.json();
        })
        .then(data => {this.setState({...data})});
    }

    render() {
        return (
            <div className="row">
                <div className="col-md-6">
                    <h3> Text to Summarize: </h3>
                    <form>
                        <div className="form-group">
                            <textarea
                                className="form-control"
                                onChange={this.handleTextChange}
                            >
                            </textarea><br/>
                        </div>
                        <div className="form-group">
                            <button
                                className="btn btn-success form-control"
                                type="submit"
                                onClick={this.handleSubmit}
                            > Get Summary
                            </button>
                        </div>
                    </form>
                </div>
                {
                    this.state.message ? (
                        <div>
                            <div className="col-md-6">
                                <h4 className="text-danger text-center">
                                    {this.state.data.message} 
                                </h4>
                            </div>
                        </div>
                    ) : ( 
                        <div className="col-md-6">
                            {this.state.summary?(<h3> Summary </h3>): ''}
                            <div className="text-justified">
                                {this.state.summary}
                            </div>
                        </div>
                    )
                }               
            </div>
        );
    }
}
