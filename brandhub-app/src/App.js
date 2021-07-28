import './App.css';
import f1 from "./assets/f1.PNG";
import f2 from "./assets/f3flip.png";
import wishlist from "./assets/wishlist.png";
import HeaderComponent from "./Components/HeaderComponent";
import {Route , Switch, Link} from "react-router-dom";
import Aos from "aos";
import "aos/dist/aos.css";
import { useEffect } from 'react';
import Footer from './Components/Footer';
function App() {

  useEffect(()=>{
    Aos.init({duration: 500});
  },[]);

  return (
    <div className="App">

<HeaderComponent/>

      {/* ----------TOP BANNER------------- */}
      {/* <div className="app__topbar">
       
        <h1 className="app__title">BrandHub</h1>
        <div className="desc__container">
          <p className="app__desc">Welcome to BrandHub! Want to go to a mall but don't feel like? Wanna find that one outfit you can't seem to find? Or do you want suggestions for your new outfit? BrandHub is the way to go!</p>
        </div>
        <div className="app__featureCont">
              <div className="app__featureCard">
                <a href="#search" className="feature__name">Search By Image</a>
                <hr className="line"/> 
                <img src={sbi__img} style={{maxWidth: "100%"}}/>
              </div>
      
              <div className="app__featureCard">
                <h3 className="feature__name">Search By Text</h3>
                <hr className="line"/> 
                <img src={sbt__img} style={{maxWidth: "100%"}}/>

              </div>  
              <div className="app__featureCard">
                <h3 className="feature__name">Make a match</h3>
                <hr className="line"/> 
                <img src={mam__img} style={{maxWidth: "100%"}}/>

              </div>
        </div>
        
      </div> */}

      <div data-aos="fade-down" className="app__titleCont">
          <h1 className="app__title">Brandhub</h1>
          <p className="app__desc">Welcome to BrandHub! Want to go to a mall but don't feel like? Wanna find that one outfit you can't seem to find? Or do you want suggestions for your new outfit? BrandHub is the way to go!</p>

      </div>

      <br/>

      {/* ----------FEATURES------------- */}
      <div className="feature__titleCont">
        <h1 className="feature__title">Features</h1>
      </div>

      {/* ----------SEARCH BY IMAGE/TEXT------------- */}
      <div id="search" className="search__cont">
        <div data-aos="fade-right" className="search__left">
          <p className="title-feature">Search By Image/Text</p>
          <p className="para-feature-left">Have something in mind? want to explore new options and items? You're at the right place. Search by text\image allows you to search your desired product using simple keywords or any image, taken from the camera or from your gallery. </p>
          <Link to="/Search"><button className="search__btn">Search Away!</button></Link>
        </div>
        <div  className="search__right">
          <img data-aos="fade-left" className="img__right" src={f1}/>
        </div>
      </div>

      <br/>
      <br/>
      <br/>
      <br/>
      <br/>

      <div id="search" className="search__cont">
        <div data-aos="fade-right" className="makeamatch__left">
          <img className="img__left" src={f2} />
        </div>

        <div data-aos="fade-left" className="makeamatch__right">
        <h1 className="title-feature">Make a Match</h1>
            <p className="para-feature-right">Can't figure out what to match with a specific clothing item? We have you covered! Just upload an image of item you want matching with. Specify what you want matched with it and voila! We'll give you the best combinations. </p>
            <Link to ="/MAM"><button className="makeamatch__btn">Make a match!</button></Link>
        </div>
        
        
      </div>

      <div id="search" className="search__cont">
      <div data-aos="fade-right" className="search__left">
          <p className="title-feature">Wishlist</p>
          <p className="para-feature-left">Have your eyes on something and don't want to lose track of it? Don't worry, put it into your wishlist when you see it! Click below to check out your wishlist!</p>
          <Link to="/Wishlist"><button className="wishlist__btn">Wishlist!</button></Link>
        </div>
        <div  className="search__right">
          <img data-aos="fade-left" className="img__right" src={wishlist}/>
        </div>
      </div>

      <div data-aos="fade-up">
      <Footer />
      </div>
    </div>
  );
}

export default App;
