import React from 'react';

export default class TopicModelingForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            texts: [null,],
            levels: 1,
            keywordsPerTopic: 3,
            numTopics: 2,
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    addText = (event) => {
        event.preventDefault();
        let texts = [...this.state.texts, null];
        this.setState({texts});
    }

    changeNumTopics = (ev) => {
        this.setState({numTopics:ev.target.value});
    }
    changeKeywordsPerTopic = (ev) => {
        this.setState({keywordsPerTopic:ev.target.value});
    }
    changeLevels = (ev) => {
        this.setState({levels:ev.target.value});
    }

    handleChange(event, index) {
        let texts = [...this.state.texts];
        texts[index] = event.target.value;
        this.setState({texts});
    }
    handleSubmit(event) {
        // make an api call, and pass data to parent
        event.preventDefault();
        let formdata = new FormData();
        const data = new URLSearchParams();
        data.append("keywords_per_topic", this.state.keywordsPerTopic);
        data.append("depth", this.state.levels);
        data.append("number_of_topics", this.state.numTopics);
        for (var x in this.state.texts) {
            data.append("documents", this.state.texts[x]);
        }

        fetch('/api/topic-modeling/', {
            method: 'POST',
            //headers: {'Content-Type':'application/x-www-form-urlencoded'},
            body: data
        })
        .then(response => {window.scrollTo(0,0);return response.json()})
        .then(data => {this.props.sendData(data);});
    }

    render () {
        let v = this.state.renderVal;
        return (
            <div>
            <h3>Find Topics/Subtopics</h3>
            <form>
                <div className="form-group">
                    <label><b>Num topics</b></label>
                    <input className="form-control" type="number" onChange={this.changeNumTopics} value={this.state.numTopics} />
                </div>
                <div className="form-group">
                    <label><b>Keywords per topic</b></label>
                    <input className="form-control" type="number" onChange={this.changeKeywordsPerTopic} value={this.state.keywordsPerTopic} />
                </div>
                <div className="form-group">
                    <label><b>Levels</b></label>
                    <input className="form-control" type="number" onChange={this.changeLevels} value={this.state.levels} />
                </div>
                <div className="form-group">
                    {
                        this.state.texts.map((x,i) => (
                            <div key={i}>
                            <label><b>Document {i+1}</b></label>
                            <textarea
                            className="form-control"
                            onChange={(ev) => this.handleChange(ev, i)}>
                            </textarea>
                            </div>
                    ))}
                </div>
                <div className="form-group">
                    <button
                        className="btn btn-primary form-control"
                        type="button"
                        onClick={this.addText}
                    >
                        Add Document
                    </button>
                    <button
                        className="btn btn-success form-control"
                        type="submit"
                        onClick={this.handleSubmit}
                    >
                        Get Topics composition
                    </button>
                </div>
            </form>
            </div>
        );
    }
};
