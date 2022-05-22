import React, { useRef, useState } from "react";
import { useHistory } from "react-router-dom";
import { AiOutlineEyeInvisible as Closeeye, AiOutlineEye as Openeye } from "react-icons/ai";
import "./login.css";

const Login = () => {
    let history = useHistory();
    const email = useRef(null);
    const password = useRef(null);
    const [hidden, sethidden] = useState(true);
    const [Doc, setDoc] = useState(false);
    const ChangeVisibility = () => {
        sethidden(!hidden);
    }

    const Eye_Style = {
        "color": "rgba(255,255,255,0.4)",
        "size" : "1.2em",
        "cursor": "pointer",
        "onClick": ChangeVisibility,
    }

    const HandleLogin = () => {
        // Handle Login
    };

    return (
        <>
        <div className="login-form">
            <input type="email" className="input" placeHolder="email" maxLength="30" ref={email}/>
            <div className="login-password">
                <input type={`${!hidden ? "text" : "password"}`} className="input" placeHolder="password" maxLength="30" ref={password}/>
                <div className="login-eye">{
                    hidden===false ? <Openeye {...Eye_Style}/> : <Closeeye {...Eye_Style}/>
                }</div>
            </div>
            <div className="doc-sec">
                <div className={`doc-checkbox ${Doc ? "check-active" : ""}`}
                    onClick={({target}) => {setDoc(!Doc)}}></div>
                <p>Doctor</p>
            </div>
            <div className="login_button" onClick={HandleLogin}>Login</div>
            <div className="login-footer">
                <p>Don't have an account ?&nbsp;</p>
                <div className="link-to" onClick={() => {
                    history.push("/signup");
                    window.location.reload();
                }} 
                style={{ textDecoration: 'none', color: "#10ac79"}} children={"SignUp"}/>
            </div>
        </div>
        </>
    );
};

export default Login;


