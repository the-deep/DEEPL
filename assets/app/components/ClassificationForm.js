import React from 'react';

import {API_LIMIT_MESSAGE} from './Messages';

export class ClassificationForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: null,
            versions: [],
            version: null,
            message: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.versionSelect= this.versionSelect.bind(this);
    }

    versionSelect(e) {
        console.log(e.target.value);
        this.setState({version:e.target.value});
    }

    componentDidMount() {
        fetch('/api/versions/', {
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.status === 429) {
                this.setState({message: API_LIMIT_MESSAGE});
                return {versions: []};
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            const versions = data.versions.map(x=>x.version);
            const version = versions[0] || 1;
            this.setState({versions, version})})
    }

    handleChange(event) {
        this.setState({text:event.target.value});
    }
    handleSubmit(event) {
        // make an api call, and pass data to parent
        let headers = new Headers();
        headers.append('accept', 'application/json');
        let formdata = new FormData();
        formdata.append('text', this.state.text);
        formdata.append('deeper', '1');
        fetch('/api/v'+this.state.version+'/classify/', {
            credentials: 'same-origin',
            method: 'POST',
            headers: headers,
            body: formdata
        })
        .then(response => {
            if (response.status === 429) {
                this.setState({message: API_LIMIT_MESSAGE});
                return;
            }
            return response.json();
        })
        .then(data => {this.props.sendData(data);});
        event.preventDefault();
    }

    render () {
        let v = this.state.renderVal;
        return (
            <div>
                <h4 className="text-center text-danger">{this.state.message}</h4>
                <form>
                    <div className="form-group">
                        <label htmlFor=""><b>Enter Text To Classify</b></label>
                        <textarea className="form-control" onChange={this.handleChange}></textarea><br/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="version"><b>Select Version</b></label>
                        <select onChange={this.versionSelect}>
                            {
                                this.state.versions.map((x, i) => <option key={i} value={x}>{x}</option>)
                            }
                        </select>
                    </div>
                    <div className="form-group">
                        <button className="btn btn-success form-control" type="submit" onClick={this.handleSubmit}> Classify </button>
                    </div>
                </form>
            </div>
        );
    }
}

export default ClassificationForm;
