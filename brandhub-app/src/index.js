import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import SearchComponent from './Screens/Search';
import SBTRes from './Features/SBTRes';
import SBIRes from './Features/SBIRes';
import MAM from './Screens/MAM';
import MAMRes from './Features/MAMRes';
import Wishlist from './Features/Wishlist';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter, Route, Switch} from "react-router-dom";


ReactDOM.render(

<BrowserRouter>
  <Switch>
    <Route exact path="/" component={App}/>
    <Route exact path="/Search" component={SearchComponent}/>
    <Route exact path="/MAM" component={MAM}/>
    <Route exact path="/Search/SBTRes" component={SBTRes}/>
    <Route exact path="/Search/SBIRes" component={SBIRes}/>
    <Route exact path="/MAM/MAMRes" component={MAMRes}/>
    <Route exact path="/Wishlist" component={Wishlist}/>
  </Switch>
</BrowserRouter>,
document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
