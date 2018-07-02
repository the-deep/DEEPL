import React from 'react';

export default class KeywordsExtractionForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: null
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
        .then(response => {return response.json()})
        .then(data => {this.props.sendData(data);});
    }

    render () {
        return (
            <form>
                <div className="form-group">
                    <label htmlFor="email"><b>Extract keywords from: </b></label>
                    <textarea className="form-control" onChange={this.handleChange}></textarea><br/>
                </div>
                <div className="form-group">
                    <button className="btn btn-success form-control" type="submit" onClick={this.handleSubmit}> Get Keywords</button>
                </div>
            </form>
        );
    }
};
