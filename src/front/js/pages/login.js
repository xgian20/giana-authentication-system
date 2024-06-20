import React, { useState, useContext, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";


export const Login = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const { store, actions } = useContext(Context);
    const navigate = useNavigate();

    const handleClick = () => {
        actions.login(email, password)
    }

    useEffect(() => {
        if (store.isLoginSuccessful) {
            navigate("/private")
        }

    }, [store.isLoginSuccessful])

    return (
        <>
            <div className="login-page">
                {(store.token && store.token !== "" && store.token != undefined) ? (
                    <>
                        <h1>You are logged in</h1>
                        <Link to="/private">
                            <button>Go to your Invoices</button>
                        </Link>
                    </>
                ) : (
                    <>
                        <div>
                            <h1>Log In</h1>
                        </div>
                        <div>
                            {store.signupMessage || ""}
                        </div>
                        <div>
                            <input type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} required /><br />
                            <input type="password" placeholder="Enter password" value={password} onChange={e => setPassword(e.target.value)} required />
                        </div>
                        <div>
                            <button onClick={handleClick}>Login</button>
                        </div>
                    </>
                )
                }
            </div>
        </>
    );
}