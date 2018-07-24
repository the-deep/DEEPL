import React from 'react';

import {API_LIMIT_MESSAGE} from '../Messages';


export default class KeywordsExtractionForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: null,
        };
    }

    handleChange = (event) => {
        this.setState({text:event.target.value});
    }

    handleSubmit = (event) => {
        event.preventDefault();
        const data = new URLSearchParams();
        data.append("document", this.state.text);
        fetch('/api/keywords-extraction/', {
            credentials: 'same-origin',
            method: 'POST',
            //headers: {'Content-Type':'application/x-www-form-urlencoded'},
            body: data
        })
        .then(response => {
            if (response.status === 429) {
                console.log('sending empty data');
                const data = {'1grams': [], '2grams':[], message: API_LIMIT_MESSAGE};
                console.log(data);
                return data;
            }
            return response.json();
        })
        .then(data => {return this.props.sendData(data);});
    }

    render () {
        return (
            <div>
                <form>
                    <div className="form-group">
                        <label><b>Extract keywords from: </b></label>
                        <textarea className="form-control" onChange={this.handleChange}></textarea><br/>
                    </div>
                    <div className="form-group">
                        <button className="btn btn-success form-control" type="submit" onClick={this.handleSubmit}> Get Keywords</button>
                    </div>
                </form>
            </div>
        );
    }
};
