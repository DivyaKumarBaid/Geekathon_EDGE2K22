import React from "react";
import { useHistory } from "react-router-dom";
import { RiCommunityLine as Community} from "react-icons/ri";
import { HiLogin as Login } from "react-icons/hi";
import { BiBell as Notification } from "react-icons/bi";
import "./navbar.css";

const Navbar = () => {
    let history = useHistory();
    const Icon_Config = {
        size: "1.8em",
        color: "#10ac79",
    };

    return (
        <>
        <div className="navbar">
            <div className="web-title link-to">
                <div to="/" onClick={() => {
                        history.push("/");
                        window.location.reload();
                    }}  style={{ textDecoration: 'none', color: "#fff"}}>
                    Well <b>Being</b>
                </div>
            </div>
            <div className="nav-link-section">
                <div className="nav-link link-to" onClick={() => {
                        history.push("/community");
                        window.location.reload();
                    }} children={
                    <Community className="nav-icon" {...Icon_Config}/>
                }/>
                <div className="nav-link link-to" onClick={() => {
                        history.push("/community");
                        window.location.reload();
                    }} children={
                    <Notification className="nav-icon" {...Icon_Config}/>
                }/>
                <div className="nav-link link-to" onClick={() => {
                        history.push("/login");
                        window.location.reload();
                    }} children={
                    <Login className="nav-icon" {...Icon_Config}/>
                }/>
            </div>
        </div>
        </>
    );
};

export default Navbar;
