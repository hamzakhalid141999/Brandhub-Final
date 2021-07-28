import React, { useEffect, useState } from 'react';
import HeaderComponent from '../Components/HeaderComponent';
import { Breadcrumb } from 'antd';
import { UserOutlined, HomeOutlined, SearchOutlined } from '@ant-design/icons';
import { Row, Col } from 'antd';
import { Link } from "react-router-dom";
import "./Wishlist.css";
import Aos from "aos";


function Wishlist() {

  useEffect(()=>{
    Aos.init({duration: 500});
  },[]);

  const [products, setProducts] = useState([]);

  useEffect(()=>{
    setProducts(JSON.parse(localStorage.getItem("wishlistItems")));
  },[])
  console.log("Array: ",products);

  function Delete (product){
      setProducts(products.filter(prod=> prod.PId !== product.PId));
  }


    return (
        <div className="wishlist">
            <HeaderComponent/>
            <div className="container-breadcrumbs">
              <Breadcrumb separator=">">
                <Breadcrumb.Item>
                  <HomeOutlined />
                  <span><Link to="/"><a>Dashboard</a></Link></span>
                </Breadcrumb.Item>
                <Breadcrumb.Item>Wishlist</Breadcrumb.Item>
              </Breadcrumb>
            </div>

            <h1 style={{fontSize: "60px", color: "gray"}} >Wishlist</h1>

              <Row className="product__row">

                {products?.length>0 ? products.map(prods=>                  
                  <Col span={8}>

                  <div data-aos="fade-down" className="product__card">
                      <div className="image__container">
                        <img className="img" alt="product" src={prods.ImageName[0]}/>
                      </div>

                    <div className="product__detail">
                      <p className="prod__name">{prods.PName}</p>
                      <p className="prod__price">Price: {prods.PPrice}</p>
                      <p className="prod__color">Color: {prods.Color}</p>  
                      <div className="buttons__cont">
                    <button className="open__product">Open Product</button>
                    <button onClick={()=>Delete(prods)} className="remove__product">Remove</button>
                    </div>                    
                    </div> 
                   

                  </div>
                  <br></br>
                </Col>
                  ) : <div data-aos="fade-up" className="wishlist__empty" style={{textAlign: "center"}}><h1 className="empty__message">Your wishlist is empty!</h1></div>}
                
              </Row>
        </div>
    );
}

export default Wishlist;