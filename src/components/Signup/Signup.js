import React, { useRef, useState } from "react";
import { useHistory } from "react-router-dom";
import { AiOutlineEyeInvisible as Closeeye, AiOutlineEye as Openeye } from "react-icons/ai";

const Signup = () => {
    let history = useHistory();
    const name = useRef(null);
    const email = useRef(null);
    const phone = useRef(null);
    const locality = useRef(null);
    const address = useRef(null);
    const pin = useRef(null);
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

    const HandleSignup = () => {
        // Handle Signup
    };

    return (
        <div className="login-form">
            <input type="text" className="input" placeHolder="name" maxLength="40" ref={name}/>
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
            {Doc && <input type="tel" className="input" placeHolder="phone" ref={phone}/>}
            {Doc && <input type="text" className="input" placeHolder="locality" ref={locality}/>}
            {Doc && <input type="text" className="input" placeHolder="address" ref={address}/>}
            {Doc && <input type="number" className="input" placeHolder="pin" ref={pin}/>}
            <div className="login_button" onClick={HandleSignup}>SignUp</div>
            <div className="login-footer">
                <p>Already have an account ?&nbsp;</p>
                <div onClick={() => {
                    history.push("/login");
                    window.location.reload();
                }} to="/login" style={{ textDecoration: 'none', color: "#10ac79"}} children={" Login"}/>
            </div>
        </div>
    );
};

export default Signup;


