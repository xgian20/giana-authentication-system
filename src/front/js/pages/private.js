import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export const Private = () => {
    const { store, actions } = useContext(Context);
    const [authStatus, setAuthStatus] = useState("Pending");
    const navigate = useNavigate();

    useEffect(() => {
        const checkAuthentication = async () => {
            const isAuthenticated = await actions.getInvoices();
            setAuthStatus(isAuthenticated ? "granted" : "denied");
        };
        checkAuthentication();
    }, [actions])

    const logoutHandler = () => {
        actions.logout();
        navigate("/login");
    }

    return (
        <div className="private-page">
            <h1>Private Page</h1>
            {authStatus === "Pending" ? (
                <p>Loading...</p>
            ) : authStatus === "denied" ? (
                <p>Access Denied</p>
            ) : authStatus === "granted" ? (
                <div className="table-container">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Invoice #</th>
                                <th>Amount</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {store.invoices.map((invoice, index) => (
                                <tr key={index}>
                                    <th>{invoice.invoice_number}</th>
                                    <td>{invoice.invoice_amount}</td>
                                    <td>{invoice.invoice_date}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <p>Something went wrong, please try again later.</p>
            )}
            <button className="logout-button" onClick={logoutHandler}>Logout</button>
        </div>
    );
};