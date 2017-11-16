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
        // make an api call
        fetch('/api/classify/?text='+this.state.text)
        .then(response => {alert();return response.json()})
    }

    render () {
        let v = this.state.renderVal;
        return (
            <form>
            {v}
                <textarea onChange={this.handleChange}></textarea><br/>
                <input type="submit" value="Submit" onClick={this.handleSubmit}></input>
            </form>
        );
    }
}

export default ClassificationForm;
