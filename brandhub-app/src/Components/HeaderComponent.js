import React, { useEffect, useState } from 'react';
import './HeaderComponent.css'
import logo from "../assets/Logo.png"
import {Link} from "react-router-dom";



function HeaderComponent() {

    const [show, handleShow] = useState(false);
    useEffect(()=>{
        window.addEventListener("scroll",()=>{
            if (window.scrollY > 50){
                handleShow(true);
            }
            else handleShow(false);
        });
       
    },[]);


    return (
        <div className="header__solid">
            <Link to="/"><img className="logo" src={logo}/></Link>
            
            <div className="navbtn__cont">
                <p className="nav__btn">About</p>
                <p style={{right: "130px"}} className="nav__btn">Contact</p>
            </div>
        
        </div>
    );
}

export default HeaderComponent;