import React from 'react';
import './Footer.css'
import logo from '../assets/Logo.png'

function Footer() {
    return (
        <div className="footer">
            <div className="footer__content">
                <div className="image__container">
                    <img src={logo} style={{maxWidth: "200%"}}/>
                </div>
                <div className="vertical__line">

                </div>
                
                <div className="info__container">
                    
                    <h2 style={{color: "white"}}>Developed By</h2>
                    <p className="developer">Hamza Bin Khalid  - i170022@nu.edu.pk</p>
                    <p className="developer">Mariam Khalid     - i170165@nu.edu.pk</p>
                    <p className="developer">Zahra Akhtar Aziz - i170316@nu.edu.pk</p>
                </div>
            </div>
        </div>
    );
}

export default Footer;