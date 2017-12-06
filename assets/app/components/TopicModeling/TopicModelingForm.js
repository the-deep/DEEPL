import React from 'react';

export default class TopicModelingForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: null
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({text:event.target.value});
    }
    handleSubmit(event) {
        // make an api call, and pass data to parent
        event.preventDefault();
        let formdata = new FormData();
        const data = new URLSearchParams();
        data.append("keywords_per_topic", 5);
        data.append("documents", this.state.text);
        data.append("depth", 2);
        data.append("number_of_topics", 3);

        fetch('/api/topic-modeling/', {
            method: 'POST',
            //headers: {'Content-Type':'application/x-www-form-urlencoded'},
            body: data
        })
        .then(response => {return response.json()})
        .then(data => {this.props.sendData(data);});
    }

    render () {
        let v = this.state.renderVal;
        return (
            <form>
                <div className="form-group">
                    <label htmlFor="email"><b>Find Topics/Subtopics for:</b></label>
                    <textarea className="form-control" onChange={this.handleChange}></textarea><br/>
                </div>
                <div className="form-group">
                    <button className="btn btn-success form-control" type="submit" onClick={this.handleSubmit}> Get Topics composition</button>
                </div>
            </form>
        );
    }
};
