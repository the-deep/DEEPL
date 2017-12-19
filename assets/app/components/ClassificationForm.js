import React from 'react';

export class ClassificationForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: null,
            versions: [],
            version: null
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
        fetch('/api/versions/')
        .then(response => response.json())
        .then(data => {
            const versions = data.versions.map(x=>x.version);
            const version = versions[0] | 1;
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
        formdata.append('text', this.state.text)
        fetch('/api/v'+this.state.version+'/classify/', {
            method: 'POST',
            headers: headers,
            body: formdata
        })
        .then(response => {return response.json()})
        .then(data => {this.props.sendData(data);});
        event.preventDefault();
    }

    render () {
        let v = this.state.renderVal;
        return (
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
        );
    }
}

export default ClassificationForm;
