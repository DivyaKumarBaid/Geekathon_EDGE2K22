import React from "react";
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import "./App.css";
import Home from "./components/Home/Home";
import Login from "./components/Login/Login";
import Signup from "./components/Signup/Signup";
import Navbar from "./components/Navbar/Navbar";

function App() {
    return (
        <Router>
            <Navbar />
            <Switch>
                <Route exact path="/"><Home/></Route>
                <Route path="/login"><Login/></Route>
                <Route path="/signup"><Signup/></Route>
            </Switch>
        </Router>
    );
}

export default App;
