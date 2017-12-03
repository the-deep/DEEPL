import React from 'react';

export class ClassificationForm extends React.Component {
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
        fetch('/api/v1/classify/?text='+this.state.text)
        .then(response => {return response.json()})
        .then(data => {this.props.sendData(data);});
        event.preventDefault();
    }

    render () {
        let v = this.state.renderVal;
        return (
            <form>
                <div className="form-group">
                    <label htmlFor="email"><b>Enter Text To Classify</b></label>
                    <textarea className="form-control" onChange={this.handleChange}></textarea><br/>
                </div>
                <div className="form-group">
                    <button className="btn btn-success form-control" type="submit" onClick={this.handleSubmit}> Classify </button>
                </div>
            </form>
        );
    }
}

export default ClassificationForm;
