import React, { useState, useContext, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

export const SignUp = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const {store, actions} = useContext(Context);
    const navigate = useNavigate();

    const handleClick = () => {
        actions.signUp(email, password)
    } 

    useEffect(() => {
        if(store.isSignUpSuccessful) {
            navigate("/login")
        }
        
    }, [store.isSignUpSuccessful])


    return (
        <>
            <div className="signup-page">
                <div>
                    <h1>Sign Up</h1>
                </div> 
                <div>
                    {store.signupMessage || ""}
                </div>
                <div>
                    <input type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} required /><br/>
                    <input type="password" placeholder="Enter password" value={password} onChange={e => setPassword(e.target.value)} required />
                </div>
                <div>
                    <button onClick={handleClick}>Sign Up</button>
                </div>
            </div>
        </>
    );
}