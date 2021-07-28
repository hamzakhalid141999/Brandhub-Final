import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './SBTRes.css'
import { Button } from 'antd';
import { Layout } from 'antd';
import Header from "../Components/HeaderComponent";
import { Row, Col } from 'antd';
import { Breadcrumb } from 'antd';
import {UserOutlined, HomeOutlined, SearchOutlined } from '@ant-design/icons';
import {Link } from "react-router-dom";
import '../App.css';
import { Input } from 'antd';
import axios from 'axios'
import { Image } from 'antd';
import { Spin } from 'antd';
import {sortBy} from 'lodash';
import { message } from 'antd';



const {Footer, Sider, Content } = Layout;
const { Search } = Input;

var load;

const api = axios.create({
  baseURL: 'http://127.0.0.1:5001'
})

const urlConvert = function (url) {
  var URLArray;
  var id;
  var newURL;
  URLArray = url.split('/');
  //console.log(URLArray[5]);
  id = URLArray[5];
  // console.log(id);
  newURL = "https://drive.google.com/thumbnail?id=" + id;

  return newURL;
}
class SBTRes extends Component {

  wishlist = (prods)=>{
    console.log(prods);
    let wishlistItems = JSON.parse(localStorage.getItem("wishlistItems")) || [];

    if (wishlistItems.some((wishlistItems)=>wishlistItems.PId===prods.PId)){
      message.error({
        content:'Item deleted from Wishlist!', 
        duration: 1,
        style:{
          marginTop: '85vh',
          marginLeft: '170vh'
        }});
      wishlistItems = wishlistItems.filter((wishlistItems)=>wishlistItems.PId!==prods.PId);
    }
    else {
      message.success({
        content:'Item added to Wishlist!', 
        duration: 1,
        style:{
          marginTop: '85vh',
          marginLeft: '170vh'
        }});
      wishlistItems = [...wishlistItems, prods];
    }
    localStorage.setItem('wishlistItems', JSON.stringify(wishlistItems));


    console.log(JSON.parse(localStorage.getItem("wishlistItems")));
  }

 


  sortByPrice = ()=>{
    const {products} = this.state;
    // for (var i=0; i<products.length-1; i++){
    //   for (var j=0; j<products.length-i-1; j++){
    //     if (products[j]>products[j])
    //   }
    // }
    this.setState({products: sortBy(products, ['PPrice'])})
  };

  state = {
    products: [],
    isResEmpty: false
  }  
  
  constructor() {
    super();

    load = 1;

    var inputGender = localStorage.getItem("gender")
    var range = localStorage.getItem("range");
   

    if (inputGender === "M") {
      var apiURL = '/sbt/' + localStorage.getItem("inputString") + '/M';
    }
    if (inputGender === "F") {
      var apiURL = '/sbt/' + localStorage.getItem("inputString") + '/F';
    }

   console.log("RANGE"+range);
   console.log(inputGender);
   console.log(apiURL);

    api.get(apiURL).then(res => {

      load = 0;

      for (let prod of Object.keys(res.data)) {
        var prods = res.data[prod];
        prods.ImageName[0] = urlConvert(prods.ImageName[0])

        if (range === "no" || range === "Select Price Range"){
          this.setState({ products: [...this.state.products, prods] })
        }

        if (range === ">=1000"){
          if (prods.PPrice>="Rs.1,000" && prods.PPrice<="Rs.2,000"){
            this.setState({ products: [...this.state.products, prods] })
          }
        }
        if (range === ">=2000"){
          if (prods.PPrice>="Rs.2,000" && prods.PPrice<="Rs.3,000"){
            this.setState({ products: [...this.state.products, prods] })
          }
        }
        if (range === ">=3000"){
          if (prods.PPrice>="Rs.3,000" && prods.PPrice<="Rs.4,000"){
            this.setState({ products: [...this.state.products, prods] })
          }
        }
        if (range === ">=4000"){
          if (prods.PPrice>="Rs.4,000"){
            this.setState({ products: [...this.state.products, prods] })
          }
        }

      }
    })
}

  render() {

    return (
      <div className="SBTRes">
          <Header/>
          <div id="wishlist__enter" className="wishlistEnter">
            <p className="enter__message">Item added in wishlist!</p>
          </div>
              <div className="container-breadcrumbs">
                <Breadcrumb separator=">">
                  <Breadcrumb.Item>
                    <HomeOutlined />
                    <span><Link to="/"><a>Dashboard</a></Link></span>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item>
                    <SearchOutlined />
                    <span><Link to="/search"><a>Search By Image/Text</a></Link></span>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item>Search Results</Breadcrumb.Item>
                </Breadcrumb>
              </div>
              <Row>
                <Col span={24}>
                  <p className="pageHeading">Search Results for "{localStorage.getItem("inputString")}"</p>
                </Col>
              </Row>

              <div className="filter__btns">
                <button className="sortByPrice" onClick={this.sortByPrice}>Filter by price</button>
            </div>


              {load === 1 ? <div className="loading"> <Spin style={{ marginLeft: "25px" }} size="large" /><h3>Please wait...</h3></div> :


                this.state.products.map(products =>
                  <div className="itemContainer" key={products.PId}>

                    <Row>
                      <Col span={3}>
                        <Image
                          width={120}
                          src={products.ImageName[0]} />

                      </Col>
                      <Col span={18}>

                        <p className="productTitle">Name: {products.PName} </p>
                        <p className="productDetail">Price: {products.PPrice} </p>
                        <p className="productDetail">Fabric {products.Fabric} </p>
                        <p className="productDetail">Color: {products.Color} </p>

                      </Col>
                      <Col span={3}>
                        <div className="buttons">
                        <div className="openProductbtn">
                          <Button><a href={products.Link} target="blank">Open Product!</a></Button>
                        </div>
                        <button onClick={()=>this.wishlist(products)} className="wishlistit__btn">Wishlist it!</button>
                        </div>
                        
                      </Col>
                      <Col span={1}>
                      </Col>
                    </Row>
                  </div>
                )
              }
      </div>
    );
  }
}

export default SBTRes;