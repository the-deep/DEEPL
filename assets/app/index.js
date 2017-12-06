import React from 'react';
import ReactDOM from 'react-dom';
import '../css/index.css';
import Main from './components/Main';
import { BrowserRouter, browserHistory } from 'react-router-dom'

// ========================================

ReactDOM.render(
    (
    <BrowserRouter history={browserHistory}>
        <Main />
    </BrowserRouter>),

  document.getElementById('main')
);
